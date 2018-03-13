#include "dataStructures_queue.h"
#include <iostream>
#include <stdio.h>
//队列的结构设计参考<<算法导论>> P130

//判断队列是否为空
int IsEmpty(queue Q)
{
    return Q->head == Q->tail;
}

//判断队列是否是满的
int IsFull(queue Q)
{
    if(Q->tail - Q->head == Q->length)
        return 1;
    else
        return Q->head == (Q->tail + 1);
}

//初始化一个队列
void MakeEmpty(queue Q)
{
    Q->tail = 0;
    Q->head = 0;
}

//创建一个新的队列
queue CreateQueue(int maxElements)
{
    queue Q;

    if(maxElements < MinQueueSize)
    {
        std::cout << "Queue size is too small" << std::endl;
        return 0;
    }
    Q = (queue)malloc(sizeof(struct QueueRecord));
    if(Q == NULL)
    {
        std::cout << "Out of space" << std::endl;
        return 0;
    }
    Q->array = (int *)malloc(sizeof(int) * (maxElements + 1));
    if(Q->array == NULL)
    {
        std::cout << "Out of space" << std::endl;
        return 0;
    }
    Q->length = maxElements;
    MakeEmpty(Q);

    return Q;
}

//释放一个队列
void DisposeQueue(queue Q)
{
    if(Q != NULL)
    {
        free(Q->array);
        free(Q);
    }
}

//入队函数实现
void Enqueue(int x, queue Q)
{
    if(IsFull(Q))
        std::cout << "Full Queue" << std::endl;
    else
    {
        Q->array[Q->tail] = x;
        if(Q->tail == Q->length)
            Q->tail = 0;
        else
            ++Q->tail;
    }
}

//出队函数实现
void Dequeue(queue Q)
{
    if(IsEmpty(Q))
        std::cout << "Queue Empty" << std::endl;
    else
    {
        if(Q->head == Q->length)
            Q->head = 0;
        else
            ++Q->head;
    }
}

//带返回值的出队函数
int FrontAndDequeue(queue Q)
{
    if(IsEmpty(Q))
        std::cout << "Queue Empty" << std::endl;
    else
    {
        int x = Q->array[Q->head];
        if(Q->head == Q->length)
            Q->head = 0;
        else
            ++Q->head;
        return x;
    }
    return 0;
}

//下面开始主函数实现
//输入0-10，测试
int main(int argc, char **argv)
{
    queue Q;
    int count;

    Q = CreateQueue(10);
    for(int i = 0; i < 10; ++i)
    {
        Enqueue(i, Q);
    }
    /*for(int i = Q->head; i < Q->tail; ++i)
    {
        count = Q->head;
        std::cout << "num" << count << ": " << FrontAndDequeue(Q) << std::endl;
    }*/
    for(int i = 0; i < 5; ++i)
        Dequeue(Q);
    std::cout << "head: " << Q->head << std::endl;
    Enqueue(10, Q);
    Enqueue(11, Q);
    while(!IsEmpty(Q))
    {
        count = Q->head;
        std::cout << "num" << count << ": " << FrontAndDequeue(Q) << std::endl;
    }
    DisposeQueue(Q);
    return 0;
}
