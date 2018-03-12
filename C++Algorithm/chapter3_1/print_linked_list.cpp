#include "print_linked_list.h"
#include <stdlib.h>
#include <stdio.h>
/* Return true if L is empty */
int IsEmpty(List L)
{
    return L->Next == NULL;
}
/* Return true if P is the last position in list L. Parameter L is unused in this implementation */
int IsLast(Position P, List L)
{
    return P->Next == NULL;
}
/* Return Position of X in L; NULL if not found */
Position Find(int X, List L)
{
    //从第一个元素开始找
    Position p;

    p = L->Next;
    while((p != NULL) && (p->element != X))
        p = p->Next;
    
    return p;
}
/* Delete first occurrence of X from a list; Assume use of a header node */
void Delete(int X, List L)
{
    Position p, temCell;

    p = FindPrevious(X, L);
    if(!IsLast(p, L))
    {
        temCell = p->Next;
    	p->Next = temCell->Next;
    	free(temCell);
    }
}
/* If X is not found, then Next field of returned Position is NULL.*/
Position FindPrevious(int X, List L)
{
    Position p;

    p = L;
    while((p->Next != NULL) && (p->Next->element != X))
        p = p->Next;
    
    return p;
}
/* Insert (after legal position p) */
void Insert(int X, List L, Position P)
{
    Position temCell;

    temCell = (Position)malloc(sizeof(struct Node));
    if(temCell == NULL)
    {
	    printf("Out of space");
	    return;
    }
    temCell->element = X;
    temCell->Next = P->Next;
    P->Next = temCell;
}
/* DeleteList algorithm */
void DeleteList(List L)
{
    Position p, temCell;

    p = L->Next;
    L->Next = NULL;
    while(p != NULL)
    {
        temCell = p->Next; //释放之前，保留下一个元素位置
	    free(p);
	    p = temCell;
    }
}
/* 清空一个链表 */
List MakeEmpty(List L)
{
    List temL;
    temL = L;
    DeleteList(L);
    return temL;
}
/* 返回一个链表的头节点 */
Position Header(List L)
{
    return L;
}
/* 返回一个链表第一个元素 */
Position First(List L)
{
    return L->Next;
}
/* 主函数 main */
int main(int argc, char **argv)
{
    List L = (List)malloc(sizeof(struct Node));
    if(L == NULL)
    {
        printf("Out of space(main)");
	    return 0;
    }
    L->Next = NULL;
    L->element = 0;
    Position p = L;
    for(int i = 1; i <= 100; ++i)
    {
        Insert(i, L, p);
	    p = p->Next;
    }
    if(!IsEmpty(L))
    {
        p = L->Next;
	    while(p != NULL)
        {
	        printf("%d  ", p->element);
	        p = p->Next;
	    }
        printf("\n");
    }
    else
        printf("the list is NULL");

    return 0;
}