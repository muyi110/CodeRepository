#include <iostream>
#include "maxSubsequence.h"
#include <time.h>

//参考《数据结构与算法分析》P18-P21

//算法1--穷举法
int MaxSubsequenceSum_1(const int A[], int N)
{
    int thisSum, maxSum, i, j, k;

    maxSum = 0;
    for(i = 0; i < N; ++i)
    {
        for(j = i; j < N; ++j)
        {
            thisSum = 0;
            for(k = i; k <= j; ++k)
                thisSum += A[k];

            if(thisSum > maxSum)
                maxSum = thisSum;
        }
    }
    return maxSum;
}
//算法2--在算法1的基础上撤除最内层的for循环
int MaxSubsequenceSum_2(const int A[], int N)
{
    int thisSum, maxSum, i, j;

    maxSum = 0;
    for(i = 0; i < N; ++i)
    {
        thisSum = 0;
        for(j = i; j < N; ++j)
        {
            thisSum += A[j];
            if(thisSum > maxSum)
                maxSum = thisSum;
        }
    }
    return maxSum;
}
//算法3--分治算法（程序用递归算法实现）
int MaxSubSum(const int A[], int left, int right)
{
    int maxLeftSum, maxRightSum;
    int maxLeftBorderSum, maxRightBorderSum;
    int leftBorderSum, rightBorderSum;
    int center, i;

    if(left == right)
    {
        if(A[left] > 0)
            return A[left];
        else
            return 0;
    }
    center = (left + right) / 2;
    maxLeftSum = MaxSubSum(A, left, center);
    maxRightSum = MaxSubSum(A, center + 1, right);

    maxLeftBorderSum = 0;
    leftBorderSum = 0;

    for(i = center; i >= left; --i)
    {
        leftBorderSum += A[i];
        if(leftBorderSum > maxLeftBorderSum)
            maxLeftBorderSum = leftBorderSum;
    }

    maxRightBorderSum = 0;
    rightBorderSum = 0;

    for(i = center + 1; i <= right; ++i)
    {
        rightBorderSum += A[i];
        if(rightBorderSum > maxRightBorderSum)
            maxRightBorderSum = rightBorderSum;
    }
    return Max3(maxLeftSum, maxRightSum, maxLeftBorderSum + maxRightBorderSum);
}
int MaxSubsequenceSum_3(const int A[], int N)
{
    return MaxSubSum(A, 0, N-1);
}
int Max3(int maxLeftSum, int maxRightSum, int leftRightSum)
{
    int maxSum;
    maxSum = maxLeftSum;
    if(maxRightSum > maxSum)
        maxSum = maxRightSum;
    if(leftRightSum > maxSum)
        maxSum = leftRightSum;

    return maxSum;
}
//算法4--时间复杂度是线性的（最优的）
int MaxSubsequenceSum_4(const int A[], int N)
{
    int thisSum, maxSum , i;

    thisSum = maxSum = 0;
    for(i = 0; i < N; ++i)
    {
        thisSum += A[i];
        if(thisSum > maxSum)
            maxSum = thisSum;
        else if(thisSum < 0)
            thisSum = 0;
    }
    return maxSum;
}
//下面是主函数的实现
int main(int argc, char **argv)
{
    clock_t start, finish;
    double totaltime;
    int A[100] = {4, -3, 5, -2, -1, 2, 6, -2, 1, 2};
    for(int i = 10; i < 100; ++i)
        A[i] = (-1) * i;
    int result[4];

    std::cout << "Give the time of four Algorithm:" << std::endl;
    start = clock();
    result[0] = MaxSubsequenceSum_1(A, 100);
    finish = clock();
    totaltime = (double)(finish - start) / CLOCKS_PER_SEC;
    std::cout << "Algorithm one: result-- " << result[0] << "    time-- " << totaltime << std::endl;

    start = clock();
    result[1] = MaxSubsequenceSum_2(A, 100);
    finish = clock();
    totaltime = (double)(finish - start) / CLOCKS_PER_SEC;
    std::cout << "Algorithm two: result-- " << result[1] << "    time-- " << totaltime << std::endl;
    
    start = clock();
    result[2] = MaxSubsequenceSum_3(A, 100);
    finish = clock();
    totaltime = (double)(finish - start) / CLOCKS_PER_SEC;
    std::cout << "Algorithm three: result-- " << result[2] << "    time-- " << totaltime << std::endl;

    start = clock();
    result[3] = MaxSubsequenceSum_4(A, 100);
    finish = clock();
    totaltime = (double)(finish - start) / CLOCKS_PER_SEC;
    std::cout << "Algorithm four: result-- " << result[3] << "    time-- " << totaltime << std::endl;

    return 0;
}














