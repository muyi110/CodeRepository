#!/usr/bin/env python3
#! -*- coding:UTF-8 -*-
import tensorflow as tf
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.exceptions import NotFittedError
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV

def load_data(path="./mnist.npz"):
    f = np.load(path)
    X_train, y_train = f['x_train'], f['y_train']
    X_test, y_test = f['x_test'], f['y_test']
    f.close()
    return (X_train, y_train), (X_test, y_test)
# 创建 He initializer 节点，适用于 ReLU 及其变体激活函数
he_init = tf.contrib.layers.variance_scaling_initializer()
# 创建 leaky_relu 激活函数
def leaky_relu(alpha=0.01):
    def parametrized_leaky_relu(z, name=None):
        return tf.maximum(alpha*z, z, name=name)
    return parametrized_leaky_relu

#创建 DNNClassifier 类，为了兼容 scikit-learn 的 RandomizedSearchCV 类，实现超参数搜索调整
class DNNClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, n_hidden_layers=5, 
                 n_neurons=100,
                 optimizer_class=tf.train.AdamOptimizer,
                 learning_rate=0.01, 
                 batch_size=20, 
                 activation=tf.nn.elu, 
                 initializer=he_init, 
                 batch_norm_momentum=None, 
                 dropout_rate=None, 
                 random_state=None
                 ):
        self.n_hidden_layers = n_hidden_layers
        self.n_neurons = n_neurons
        self.optimizer_class = optimizer_class
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.activation = activation
        self.initializer = initializer
        self.batch_norm_momentum = batch_norm_momentum
        self.dropout_rate = dropout_rate
        self.random_state = random_state
        self._session = None
    def _dnn(self, inputs):
        '''构建隐含层，支持 batch normalization 和 dropout'''
        #每一层的 batch normalization 和 dropout 都一样
        for layer in range(self.n_hidden_layers):
            if self.dropout_rate:
                inputs = tf.layers.dropout(inputs, self.dropout_rate, training=self._training)
            # tf.layers.dense 默认没有激活函数，输出是线性的
            inputs = tf.layers.dense(inputs, self.n_neurons, 
                                     kernel_initializer=self.initializer,
                                     name="hidden%d" % (layer+1))
            if self.batch_norm_momentum:
                inputs = tf.layers.batch_normalization(inputs, momentum=self.batch_norm_momentum, 
                                                      training=self._training)
            inputs = self.activation(inputs, name="hidden%d_out" % (layer+1))
        return inputs
    def _build_graph(self, n_inputs, n_outputs):
        '''构建模型'''
        if self.random_state is not None:
            tf.set_random_seed(self.random_state)
            np.random.seed(self.random_state)
        X = tf.placeholder(tf.float32, shape=(None, n_inputs), name="X")
        y = tf.placeholder(tf.int32, shape=(None), name="y")
        # 如果需要 BN 或者 dropout 需要指示是在训练阶段还是其他阶段
        if self.batch_norm_momentum or self.dropout_rate:
            self._training = tf.placeholder_with_default(False, shape=(), name="training")
        else:
            self._training=None
        dnn_outputs = self._dnn(X) # 构建模型，获取最后隐藏层的输出
        logits = tf.layers.dense(dnn_outputs, n_outputs, kernel_initializer=he_init, name="logits")
        Y_proba = tf.nn.softmax(logits, name="Y_proba")
        # 计算交叉熵
        xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
        loss = tf.reduce_mean(xentropy, name="loss")
        # 构建优化器节点
        optimizer = self.optimizer_class(learning_rate=self.learning_rate)
        training_op = optimizer.minimize(loss)
        # 构建计算准确率节点
        correct = tf.nn.in_top_k(logits, y, 1)
        accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name="accuracy")
        # 构建全局初始化节点和模型保存节点
        init = tf.global_variables_initializer()
        saver = tf.train.Saver()
        
        self._X, self._y = X, y
        self._Y_proba, self._loss = Y_proba, loss
        self._training_op, self._accuracy = training_op, accuracy
        self._init, self._saver = init, saver
    def close_session(self):
        if self._session:
            self._session.close()
    def _get_model_params(self):
        '''获取所有变量值，用于 early stopping ,faster than saving to disk'''
        with self._graph.as_default():
            gvars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)# 获取一个 list 包含所有的变量
        return {gvar.op.name: value for gvar, value in zip(gvars, self._session.run(gvars))}
    def _restore_model_params(self, model_params):
        gvar_names = list(model_params.keys())
        # 获取被给名字的操作(op)
        assign_ops = {gvar_name: self._graph.get_operation_by_name(gvar_name + "/Assign") for gvar_name in gvar_names}
        # inputs 是tf.Operation 的属性. The list of Tensor objects representing the data inputs of this op
        init_values = {gvar_name: assign_op.inputs[1] for gvar_name, assign_op in assign_ops.items()}
        # 由于 key 是 tensor ，所以 value 会替换为 key 对应的 tensor. 具体参考官网 tf.Session.run
        feed_dict = {init_values[gvar_name]: model_params[gvar_name] for gvar_name in gvar_names}
        self._session.run(assign_ops, feed_dict=feed_dict)
    def fit(self, X, y, n_epochs=100, X_valid=None, y_valid=None, X_test=None, y_test=None):
        '''Fit the model to the training set. If X_valid and y_valid are provided, use early stopping'''
        self.close_session()
        # 获取 n_inputs 和 n_outputs
        n_inputs = X.shape[1]  # 可以理解为获取特征数
        self.classes_ = np.unique(y) # 获取有几个类别, 返回是一个有序的对象（升序）
        n_outputs = len(self.classes_)
        # 将 labels vector 转为类索引。例如：y=[8,8,9,5,7,6,6,6] 得到有序的类标签是 [5,6,7,8,9] 
        # label vector 将会转化为 [3,3,4,0,2,1,1,1]
        self.class_to_index_ = {label: index for index, label in enumerate(self.classes_)}
        y = np.array([self.class_to_index_[label] for label in y], dtype=np.int32)
        self._graph = tf.Graph()
        with self._graph.as_default():
            self._build_graph(n_inputs, n_outputs) # 调用构建模型方法
            # 用于 BN 操作的 moving_mean 和 moving_variance 更新(training 期间) 参考 tf.layers.batch_normalization
            extra_update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        # 下面的几个变量用于 early stopping
        max_checks_without_progress = 20
        checks_without_progress = 0
        best_loss = np.infty
        best_params = None
        # 开始训练阶段
        self._session = tf.Session(graph=self._graph)
        with self._session.as_default() as sess:
            sess.run(self._init)
            for epoch in range(n_epochs):
                rnd_idx = np.random.permutation(len(X))# 返回 np.array 结果是将输入打乱。 len(X) 获取实例个数
                for rnd_indices in np.array_split(rnd_idx, len(X)//self.batch_size):
                    X_batch, y_batch = X[rnd_indices], y[rnd_indices]
                    feed_dict = {self._X: X_batch, self._y: y_batch}
                    if self._training is not None:
                        feed_dict[self._training] = True
                    sess.run(self._training_op, feed_dict=feed_dict)
                    # 针对 BN 操作
                    if extra_update_ops:
                        sess.run(extra_update_ops, feed_dict=feed_dict)
                # X_valid 和 y_valid 验证集用于早停算法
                if X_valid is not None and y_valid is not None:
                    loss_val, acc_val = sess.run([self._loss, self._accuracy], 
                                                 feed_dict={self._X: X_valid, self._y: y_valid})
                    if loss_val < best_loss:
                        best_params = self._get_model_params()
                        best_loss = loss_val
                        checks_without_progress = 0
                    else:
                        checks_without_progress += 1
                    print("{}\tValidation loss: {:.6f}\tBest loss: {:.6f}\tAccuracy: {:.2f}%".format(epoch, 
                          loss_val, best_loss, acc_val*100))
                    if checks_without_progress >= max_checks_without_progress:
                        print("Early stopping")
                        break
                else:
                    loss_test, acc_test = sess.run([self._loss, self._accuracy], 
                                                     feed_dict={self._X: X_test, self._y: y_test})
                    print("{}\tTest loss: {:.6f}\tAccuracy: {:.2f}%".format(epoch, 
                          loss_test, acc_test*100))
            if best_params:
                self._restore_model_params(best_params)
            return self
    def predict_proba(self, X):
        if not self._session:
            raise NotFittedError("This %s instance is not fitted yet" % self.__class__.__name__)
        with self._session.as_default() as sess:
            return self._Y_proba.eval(feed_dict={self._X: X})
    def predict(self, X):
        class_indices = np.argmax(self.predict_proba(X), axis=1)
        return np.array([[self.classes_[class_index]] for class_index in class_indices], np.int32)
    def save(self, path):
        self._saver.save(self._session, path)
if __name__=="__main__":
    datas = np.load("./data_set/datas_train.npy")
    labels = np.load("./data_set/label_train.npy")

    #datas = datas.transpose((0,2,1))
    datas = datas.reshape(-1, 15*128)
    labels = np.array(labels).reshape(-1)

    datas_test = np.load("./data_set/datas_test.npy")
    labels_test = np.load("./data_set/label_test.npy")
    #datas_test = datas_test.transpose((0,2,1))
    datas_test = datas_test.reshape(-1, 15*128)
    labels_test = np.array(labels_test).reshape(-1)
    del datas_list
    # dnn_clf = DNNClassifier(random_state=42)
    # dnn_clf.fit(X_train1, y_train1, n_epochs=1000, X_valid=X_valid1, y_valid=y_valid1)
    # y_pred = dnn_clf.predict(X_test1)
    # print(accuracy_score(y_test1, y_pred))
    # # 使用 scikit-learn 的 RandomizedSearchCV 类搜索更好的超参数
    # param_distribs={
    #                 "n_neurons":[10, 30, 50, 70, 90, 100, 120, 140, 160],
    #                 "batch_size":[10, 50, 100, 500],
    #                 "learning_rate":[0.01, 0.02, 0.05, 0.1],
    #                 "activation":[tf.nn.relu, tf.nn.elu, leaky_relu(alpha=0.01), leaky_relu(alpha=0.1)]}
    # rnd_search = RandomizedSearchCV(DNNClassifier(random_state=42), param_distribs, 
    #                                 n_iter=50, random_state=42, verbose=2)
    # rnd_search.fit(X_train1, y_train1, X_valid=X_valid1, y_valid=y_valid1, n_epochs=1000)
    # print("rnd_search best params: ", rnd_search.best_params_)
    # y_pred = rnd_search.predict(X_test1)
    # print(accuracy_score(y_test1, y_pred))
    # rnd_search.best_estimator_.save("./trained_model/my_best_mnist_model_without_BN_dropout_0_to_4.ckpt")
    # 经过上述的随机搜索得到的最好超参数为：learning_rate=0.01  
    #                                       activation_fn=relu  
    #                                       n_neurons=50 
    #                                       batch_size=500
    # 最好的测试准确率：98.988%
    # dnn_clf = DNNClassifier(activation=tf.nn.relu, learning_rate=0.01, n_neurons=50, batch_size=500, random_state=42)
    # dnn_clf.fit(X_train1, y_train1, n_epochs=1000, X_valid=X_valid1, y_valid=y_valid1)
    # y_pred = dnn_clf.predict(X_test1)
    # print(accuracy_score(y_test1, y_pred))
    # # 添加 BN
    # dnn_clf_bn = DNNClassifier(activation=tf.nn.relu, learning_rate=0.01, 
    #                         n_neurons=50, batch_size=500, random_state=42, batch_norm_momentum=0.99)
    # dnn_clf_bn.fit(X_train1, y_train1, n_epochs=1000, X_valid=X_valid1, y_valid=y_valid1)
    # y_pred = dnn_clf_bn.predict(X_test1)
    # print(accuracy_score(y_test1, y_pred))
    # # 添加 BN ，随机搜索更好的超参数
    # param_distribs={
    #                 "n_neurons":[10, 30, 50, 70, 90, 100, 120, 140, 160],
    #                 "batch_size":[10, 50, 100, 500],
    #                 "learning_rate":[0.01, 0.02, 0.05, 0.1],
    #                 "activation":[tf.nn.relu, tf.nn.elu, leaky_relu(alpha=0.01), leaky_relu(alpha=0.1)],
    #                 "batch_norm_momentum":[0.9, 0.95, 0.98, 0.99, 0.999]}
    # rnd_search = RandomizedSearchCV(DNNClassifier(random_state=42), param_distribs, 
    #                                 n_iter=50, random_state=42, verbose=2)
    # rnd_search.fit(X_train1, y_train1, X_valid=X_valid1, y_valid=y_valid1, n_epochs=1000)
    # print("rnd_search best params: ", rnd_search.best_params_)
    # y_pred = rnd_search.predict(X_test1)
    # print(accuracy_score(y_test1, y_pred))
    # 经过上面搜索，带有 BN 的最好超参数为：learning_rate=0.01
    #                                       n_neurons=160
    #                                       activation=leaky_relu
    #                                       batch_size=100
    #                                       batch_norm_momentum=0.99
    # 最好的识别准确率为：99.338%
    dnn_clf_bn = DNNClassifier(activation=leaky_relu(alpha=0.01), learning_rate=0.001, 
                            n_neurons=80, batch_size=64, random_state=42, batch_norm_momentum=0.99)
    dnn_clf_bn.fit(datas, labels-1, n_epochs=200, X_valid=None, y_valid=None, X_test=datas_test, y_test=labels_test-1)
    y_pred = dnn_clf_bn.predict(datas_test)
    print(accuracy_score(labels_test, y_pred))
