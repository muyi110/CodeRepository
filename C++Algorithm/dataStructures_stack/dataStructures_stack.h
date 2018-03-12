#ifndef STACK_H
#define STACK_H
//定义栈的结构
struct StackRecord
{
    int capacity; //栈的容量
    int top;      //栈顶元素
    int *array;   //栈的数组指针，指向栈的内存地址
};
typedef struct StackRecord* stack;
//下面是栈的相关操作
int IsEmpty(stack S);
int IsFull(stack S);
stack CreateStack(int maxElements);
void DisposeStack(stack S);
void MakeEmpty(stack S);
void Push(int x, stack S);
int Top(stack S);
void Pop(stack S);
int TopAndPop(stack S);

#define EmptyTOS (-1)
#define MinStackSize (5)




#endif
