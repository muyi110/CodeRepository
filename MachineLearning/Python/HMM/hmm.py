# -*- coding=UTF-8 -*-
import numpy as np

class HMM():
    def __init__(self, A, B, pi):
        '''
        A: numpy.ndarray
            状态转移矩阵
        B: numpy.ndarray
            观测矩阵
        pi: numpy.ndarray
            初始状态向量
        '''
        self.A = A
        self.B = B
        self.pi = pi
    def _forward(self, obs_seq):
        '''
        前向算法
        obs_seq: 观测的 list (list of int)
        '''
        N = self.A.shape[0] # 状态的个数
        T = len(obs_seq) # 观测序列长度

        # F 表示保存的前向概率计算矩阵
        F = np.zeros((N, T))
        F[:, 0] = self.pi * self.B[:,obs_seq[0]] # 初始值
        for t in range(1, T):
            for n in range(N):
                F[n, t] = np.dot(F[:, t-1], self.A[:, n]) * self.B[n, obs_seq[t]]
        return F
    def _backward(self, obs_seq):
        '''
        后向算法
        '''
        N = self.A.shape[0] # 状态的个数
        T = len(obs_seq) # 观测序列长度

        # X 表示保存的后向概率矩阵
        X = np.zeros((N, T))
        X[:, -1] = 1 # 初始值
        for t in reversed(range(T-1)):
            for n in range(N):
                X[n, t] = np.sum(X[:, t+1] * self.A[n, :] * self.B[:, obs_seq[t+1]])
        return X
    def observation_prob(self, obs_seq):
        '''
        计算概率
        '''
        return np.sum(self._forward(obs_seq)[:,-1])
    def state_path(self, obs_seq):
        '''
        回溯最优状态路径
        '''
        V, prev = self.viterbi(obs_seq)
        last_state = np.argmax(V[:,-1])
        path = list(self.build_viterbi_path(prev, last_state))
        return V[last_state, -1], reversed(path)
    def viterbi(self, obs_seq):
        '''
        Viterbi 算法
        '''
        N = self.A.shape[0] # 状态的个数
        T = len(obs_seq) # 观测序列的长度
        prev = np.zeros((T-1, N), dtype=np.int32) # 指向最大化 t 时刻对应某一状态的概率的 t-1 时刻状态
        # V 表示动态规划矩阵，包含被给时刻的最大似然函数（概率）
        V = np.zeros((N, T))
        # 初始化
        V[:,0] = self.pi * self.B[:, obs_seq[0]]

        for t in range(1, T):
            for n in range(N):
                seq_probs = V[:, t-1] * self.A[:, n] * self.B[n, obs_seq[t]]
                prev[t-1, n] = np.argmax(seq_probs)
                V[n, t] = np.max(seq_probs)
        return V, prev
    def build_viterbi_path(self, prev, last_state):
        T = len(prev)
        yield (last_state)
        for i in range(T-1, -1, -1):
            yield(prev[i, last_state])
            last_state = prev[i, last_state]
    def baum_welch(self, observations, criterion=1e-5):
        '''
        HMM 中的 EM 算法实现
        criterion: 迭代终止条件
        '''
        n_states = self.A.shape[0]
        n_samples = len(observations)

        iteration_flag = True # 是否迭代的标志
        # 开始进行迭代
        while iteration_flag:
            # 前向传播算法求 alpha 的值
            alpha = self._forward(observations)
            # 后向传播算法求 beta 的值
            beta = self._backward(observations)
            # 求 xi(i, j)
            xi = np.zeros((n_states, n_states, n_samples-1))
            for t in range(n_samples - 1):
                # 求分母部分
                denominator = np.dot(np.dot(alpha[:,t].T, self.A) * self.B[:, observations[t+1]].T, beta[:,t+1])
                for i in range(n_states):
                    # 求分子部分
                    numerator = alpha[i,t] * self.A[i,:] * self.B[:,observations[t+1]].T * beta[:, t+1].T
                    xi[i,:,t] = numerator / denominator
            # 求 gamma
            gamma = np.sum(xi, axis=1) # 对 xi 求边缘概率
            # 计算 t=T 时刻
            prod = (alpha[:, n_samples-1] * beta[:, n_samples-1]).reshape((-1, 1))
            gamma = np.hstack((gamma, prod/np.sum(prod)))
            # 开始更新模型参数
            pi_new = gamma[:,0]
            A_new = np.sum(xi, axis=2) / np.sum(gamma[:,:-1], axis=1).reshape((-1,1))
            B_new = np.copy(self.B)
            num_levels = self.B.shape[1] # 获取观测的状态个数
            sumgamma = np.sum(gamma, axis=1)
            for lev in range(num_levels):
                mask = observations == lev
                B_new[:,lev] = np.sum(gamma[:,mask], axis=1) / sumgamma
            # 判断是否满足停止迭代条件
            if np.max(abs(self.pi-pi_new)) < criterion and np.max(abs(self.A-A_new)) < criterion and np.max(abs(self.B-B_new)) < criterion:
                iteration_flag = False # 迭代终止
            self.A[:], self.B[:], self.pi[:] = A_new, B_new, pi_new
        return A_new, B_new, pi_new
