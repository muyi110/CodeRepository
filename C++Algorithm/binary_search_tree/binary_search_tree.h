#ifndef TREE_H
#define TREE_H

struct TreeNode;
typedef struct TreeNode *searchTree;
typedef struct TreeNode *position;

//二叉树结构
struct TreeNode
{
    int element;        //关键字
    searchTree left;   //指向左儿子
    searchTree right;  //指向右儿子
};

searchTree MakeEmpty(searchTree T);
position Find(int x, searchTree T);
position FindMin(searchTree T);
position FindMax(searchTree T);
searchTree Insert(int x, searchTree T);
searchTree Delete(int x, searchTree T);

#endif
