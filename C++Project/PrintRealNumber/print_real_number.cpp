/************************************************************************/
/*
程序目的：打印任意实数（包括负数），解决四舍五入问题
Author: YangLiuqing
Date: 2017-12-21
*/
/************************************************************************/
#include "print_real_number.h"
#include <iostream>
#define LINUX_H
using namespace std;

int main(int argc, char **argv)
{
    if(argc != 3)
    {
        cout << "error: Input the realNumber to show and the number of decimal places" << endl;
        return 0;
    }
    double value = atof(argv[1]);
    unsigned int decPlaces = (unsigned int)atoi(argv[2]);
    PrintReal(value, decPlaces);
    #ifdef LINUX_H
    cout << '\n';
    #endif
    #ifdef WINDOWS_H
    cout << "\r\n";
    #endif
    return 0;
}
/***********************************************************************/
/*
功能：此函数实现四舍五入
入口参数：N：需要打印的实数
          DecPlaces：打印的小数点位数
说明：先将四舍五入的后的数字计算出来，后打印
*/
/***********************************************************************/
double RoundUp(double N, int DecPlaces)
{
    int i = 0;
    double amountToAdd = 0.5;

    for(i = 0; i < DecPlaces; ++i)
    {
        amountToAdd /= 10;
    }
    return N + amountToAdd;
}

/***********************************************************************/
/*
功能：此函数打印小数部分
入口参数：FractionPart：需要打印的小数
          DecPlaces：打印的小数点位数
*/
/***********************************************************************/
void PrintFractionPart(double FractionPart, int DecPlaces)
{
    int i, ADigit;

    for(i = 0; i < DecPlaces; ++i)
    {
        FractionPart *= 10;
	ADigit = IntPart(FractionPart);
	PrintDigit(ADigit);
	FractionPart = DecPart(FractionPart);
    }
}
/***********************************************************************/
/*
功能：此函数打印实数
入口参数：N：需要打印的实数
          DecPlaces：打印的小数点位数
*/
/***********************************************************************/
void PrintReal(double N, int DecPlaces)
{
    int intergerPart;
    double fractionPart;

    if(N < 0)
    {
        cout << '-';
	N = -N;
    }
    N = RoundUp(N, DecPlaces);
    intergerPart = IntPart(N);
    fractionPart = DecPart(N);
    PrintOut(intergerPart);

    if(DecPlaces > 0)
        cout << '.';
    PrintFractionPart(fractionPart, DecPlaces);
}
/***********************************************************************/
/*
功能：此函数实现提取实数整数部分
入口参数：N：需要打印的实数
*/
/***********************************************************************/
int IntPart(double N)
{
    return (int)N;
}
/***********************************************************************/
/*
功能：此函数实现提取实数的小数部分
入口参数：N：需要打印的实数
*/
/***********************************************************************/
double DecPart(double N)
{
    return N - IntPart(N);
}
/***********************************************************************/
/*
功能：此函数打印整数
入口参数：number：需要打印的整数
说明：函数通过递归调用，打印单个整数函数
*/
/***********************************************************************/
void PrintOut(unsigned int number)
{
    if(number >= 10)
        PrintOut(number / 10);

    PrintDigit(number % 10);
}
/***********************************************************************/
/*
功能：此函数打印单个整数
入口参数：digit: 打印的单个整数
*/
/***********************************************************************/
void PrintDigit(unsigned int digit)
{
    cout << digit;
}


