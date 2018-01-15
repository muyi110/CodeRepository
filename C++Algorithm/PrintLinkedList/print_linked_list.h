#ifndef _LIST_H
#define _LIST_H
struct Node;
typedef struct Node *PtrToNode;
typedef PtrToNode List;
typedef PtrToNode Position;

List MakeEmpty(List L);

int IsEmpty(List L);

int IsLast(Position p, List L);

Position Find(int X, List L);

void Delete(int X, List L);

Position FindPrevious(int X, List L);

void Insert(int X, List L, Position P);

void DeleteList(List L);

Position Header(List L);

Position First(List L);

struct Node
{
    int element;
    Position Next;
};
#endif
