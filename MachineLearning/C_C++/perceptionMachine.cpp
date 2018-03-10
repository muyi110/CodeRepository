#include <iostream>
#include "perceptionMachine.h"
#include <fstream>
//《统计学习方法》P29感知机例题

const int num = 10; //数据集大小（估计）
int realDataCount = 0; //数据集大小（实际）
bool flag = true; // 误分类标志

//数据集的数据结构(二维数据集)
struct DataSet
{
    double x1;
    double x2;
    double y;
}dataSet[num];

//初始化分离超平面参数w, b与学习步长eta
double eta = 1.0;
double w[2] = {0.0, 0.0};
double b = 0.0;

//读取数据
void readData(void)
{
    std::ifstream file("inputdata.txt");
    int i = 0;
    while(file >> dataSet[i].x1 >> dataSet[i].x2 >> dataSet[i].y)
    {
        ++i;
        ++realDataCount;
    }
    file.close();
}

int main(int argc, char **argv)
{
    int k = 0; //迭代次数
    readData(); //读入数据

    //输出数据集
    std::cout << "The data set has "<< realDataCount << " is: " << std::endl;
    for(int i = 0; i < realDataCount; ++i)
    {
        std::cout << dataSet[i].x1 << "  " << dataSet[i].x2 << "  " <<dataSet[i].y << std::endl;
    }

    while(flag)
    {
        for(int i = 0; i < realDataCount; ++i)
        {
            flag = false;
            if(dataSet[i].y * (w[0] * dataSet[i].x1 + w[1] * dataSet[i].x2 + b) <= 0)
            {
                flag = true;
                w[0] += eta * dataSet[i].y * dataSet[i].x1;
                w[1] += eta * dataSet[i].y * dataSet[i].x2;
                b += eta * dataSet[i].y;
                ++k;
                break;
            }
        }
    }
    
    std::cout << std::endl;
    std::cout << "result: " << std::endl;
    std::cout << "w = " << "(" << w[0] << "," << w[1] << ")" << std::endl;
    std::cout << "b = " << b << std::endl;
    std::cout << "迭代次数: " << k << std::endl;

    return 0;
}










