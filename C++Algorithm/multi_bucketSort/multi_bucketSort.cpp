#include <iostream>
#include <list>
#include <vector>
using namespace std;
//《数据结构与算法分析》P41例题
//由于需要排序的最大数是3位的，程序设计为3趟桶式排序
//其中每一个桶是一个链表
void multi_bucketSort(const int data[], const int N, std::vector<list<int>> &result)
{
    int i;
    int index;  //桶的下标
    std::vector<list<int>> sortTemp_1(10), sortTemp_2(10);
    std::list<int>::const_iterator begin, end;
    //开始第一趟桶式排序（最低位）
    for(i = 0; i < N; ++i)
    {
        index = data[i] % 10;
        sortTemp_1[index].push_back(data[i]);
    }
    //开始第二趟桶式排序(第一趟排序结果作为输入)
    for(i = 0; i < 10; ++i) //因为最多有10个桶
    {
        if(!sortTemp_1[i].empty())
        {
            begin = sortTemp_1[i].cbegin();
            end = sortTemp_1[i].cend();
            auto it = begin;
            while(it != end)
            {
                index = ((*it) / 10) % 10;  //获取次高位
                sortTemp_2[index].push_back(*it);
                ++it;
            }
        }
    }
    //开始第3趟桶式排序
    for(i = 0; i < 10; ++i)
    {
        if(!sortTemp_2[i].empty())
        {
            begin = sortTemp_2[i].cbegin();
            end = sortTemp_2[i].cend();
            auto it = begin;
            while(it != end)
            {
                index = (*it) / 100;
                result[index].push_back(*it);
                ++it;
            }
        }
    }
}
int main(int argc, char **argv)
{
    std::vector<list<int>> result(10);
    const int data[15] = {24, 27, 64, 8, 8, 216, 512, 888, 27, 729, 0, 1, 343, 125, 343};
    
    //输出排序前结果
    std::cout << "原始数据: " << std::endl;
    for(int i = 0; i < 15; ++i)
    {
        std::cout << data[i] << " ";
    }
    std::cout << std::endl;
    multi_bucketSort(data, 15, result);
    //输出排序后的结果
    std::cout << "排序后结果: " << std::endl;
    for(int i = 0; i < 10; ++i)
    {
        if(!result[i].empty())
        {
            auto it = result[i].cbegin();
            while(it != result[i].cend())
            {
                std::cout << *it << " ";
                ++it;
            }
        }
    }
    std::cout << std::endl;
    
    return 0;
}
