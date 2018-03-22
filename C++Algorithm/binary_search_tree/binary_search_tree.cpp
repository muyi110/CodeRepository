#include "binary_search_tree.h"
#include <iostream>
#include <stdlib.h>

//<<数据结构与算法分析>> P74

//建立一颗空树
searchTree MakeEmpty(searchTree T)
{
    if(T != NULL)
    {
        MakeEmpty(T->left);
        MakeEmpty(T->right);
        free(T);
    }
    return NULL;
}

//二叉树查找实现
position Find(int x, searchTree T)
{
    //下面是递归算法实现
    if(T == NULL)
        return NULL;
    if(x < T->element)
        return Find(x, T->left);
    else
    {
        if(x > T->element)
            return Find(x, T->right);
        else
            return T;
    }
    /*
    //下面是循环实现
    while(T != NULL)
    {
        if(x < T->element)
            T = T->left;
        else
        {
            if(x > T->element)
                T = T->right;
            else
                return T;
        }
    }
    return NULL
    */
}

//查找最小值和最大值
position FindMin(searchTree T)
{
    //下面是递归算法实现
    if(T != NULL)
    {
        if(T->left == NULL)
            return T;
        else
            return FindMin(T->left);
    }
    else
        return NULL;
    /*
    //下面是非递归实现
    if(T != NULL)
    {
        while(T->left != NULL)
        {
            T = T->left;
        }
    }
    return T;
    */
}
position FindMax(searchTree T)
{    
    //下面是递归算法实现
    if(T != NULL)
    {
        if(T->right == NULL)
            return T;
        else
            return FindMax(T->right);
    }
    else
        return NULL;
    /*
    //下面是非递归实现
    if(T != NULL)
    {
        while(T->right != NULL)
        {
            T = T->right;
        }
    }
    return T;
    */
}

//插入程序实现
searchTree Insert(int x, searchTree T)
{
    if(T == NULL)
    {
        T = (searchTree)malloc(sizeof(struct TreeNode));
        if(T == NULL)
        {
            std::cout << "Out of space" << std::endl;
            return NULL;
        }
        else
        {
            T->element = x;
            T->left = NULL;
            T->right = NULL;
        }
    }
    else
    {
        if(x < T->element)
            T->left = Insert(x, T->left);
        else if(x > T->element)
            T->right = Insert(x, T->right);
    }
    return T;
}

//删除算法实现
searchTree Delete(int x, searchTree T)
{
    position tmpCell;
    if(T == NULL)
    {
        std::cout << "Element is not found" << std::endl;
    }
    else
    {
        if(x < T->element)
            T->left = Delete(x, T->left);
        else
        {
            if(x > T->element)
                T->right = Delete(x, T->right);
            else
            {
                if(T->left && T->right)  //左右两个孩子都存在情况
                {
                    tmpCell = FindMin(T->right);
                    T->element = tmpCell->element;
                    T->right = Delete(T->element, T->right);
                }
                else    //只有一个孩子或没有孩子情况
                {
                    tmpCell = T;
                    if(T->left == NULL)
                        T = T->right;
                    else if(T->right == NULL)
                        T = T->left;
                    free(tmpCell);
                }
            }
        }
    }
    return T;
}

//下面是main函数测试
int main(int argc, char **argv)
{
    searchTree T = NULL;
    position pos = NULL;
    T = MakeEmpty(T);
    T = Insert(6, T);
    Insert(8, T);
    Insert(2, T);
    Insert(1, T);
    Insert(5, T);
    Insert(3, T);
    Insert(4, T);
    pos = FindMin(T);
    std::cout << "min: " << pos->element << std::endl;
    std::cout << "Max: " << FindMax(T)->element << std::endl;
    return 0;
}
