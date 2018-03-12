#include "dataStructures_stack.h"
#include <iostream>
#include <stdlib.h>

//<<数据结构与算法分析>> P50 栈的数组实现

//判断栈是否为空
int IsEmpty(stack S)
{
    if(S->top == EmptyTOS)
        return 1;  //表示栈为空
    else
        return 0;  //表示栈不为空
}

//判断栈是否满
int IsFull(stack S)
{
    return S->capacity <= S->top;
}

//创建一个固定大小的空栈
stack CreateStack(int maxElements)
{
    stack S;

    if(maxElements < MinStackSize)
    {
        std::cout << "Stack size is too small" << std::endl;
        return 0;
    }
    S = (stack)malloc(sizeof(struct StackRecord));  //保证指针指向实际内存
    if(S == NULL)
    {
        std::cout << "Out of space" << std::endl;
        return 0;
    }

    S->array = (int *)malloc(sizeof(int) * maxElements); //分配固定大小栈空间
    if(S->array == NULL)
    {
        std::cout << "Out of space" << std::endl;
        return 0;
    }

    S->capacity = maxElements;
    MakeEmpty(S);

    return S;
}

//释放栈的内存
void DisposeStack(stack S)
{
    //先释放栈数组，最后释放栈结构   
    if(S != NULL)
    {
        free(S->array);
        free(S);
    }
}

//使栈为空
void MakeEmpty(stack S)
{
    S->top = EmptyTOS;
}

//入栈函数
void Push(int x, stack S)
{
    if(IsFull(S))
        std::cout << "Full stack" << std::endl;
    else
        S->array[++(S->top)] = x;
}

//出栈函数
void Pop(stack S)
{
    if(IsEmpty(S))
        std::cout << "Empty stack" << std::endl;
    else
        S->top--;
}

//获取栈顶元素
int Top(stack S)
{
    if(IsEmpty(S))
        std::cout << "Empty stack" << std::endl;
    else
        return S->array[S->top];
    return 0;
}

//带有返回值的出栈函数
int TopAndPop(stack S)
{
    if(IsEmpty(S))
        std::cout << "Empty stack" << std::endl;
    else
        return S->array[S->top--];
    return 0;
}

//下面开始主函数main实现
//实现往栈中输入1-10,看输出，进而验证
int main(int argc, char **argv)
{
    stack S;
    int count;

    S = CreateStack(10);
    for(int i = 0; i < 10; ++i)
    {
        Push(i, S);
    }

    for(int i = 0; i < 10; ++i)
    {
        count = S->top;
        std::cout << "num" << count << ": " << TopAndPop(S) << std::endl;
    }
    return 0;
}
