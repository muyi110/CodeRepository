#ifndef QUEUE_H
#define QUEUE_H
//队列的结构
struct QueueRecord
{
    int tail;  //队列的尾
    int head;  //队列的头
    int length;//队列的长度
    int *array;
};
typedef struct QueueRecord *queue;

int IsEmpty(queue Q);
int IsFull(queue Q);
queue CreateQueue(int maxElements);
void DisposeQueue(queue Q);
void MakeEmpty(queue Q);
void Enqueue(int x, queue Q);
void Dequeue(queue Q);
int FrontAndDequeue(queue Q);

#define MinQueueSize 5

#endif
