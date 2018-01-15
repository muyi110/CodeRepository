#ifndef PRINT_REAL_NUMBER_H
#define PRINT_REAL_NUMBER_H
#include <cstdio>

int IntPart(double N); //获取输入数据的整数部分

double DecPart(double N); //获取输入数据的小数部分

void PrintReal(double N, int DecPlaces); //打印double值，第二个参数为打印小数点位数

void PrintFractionPart(double FractionPart, int DecPlaces); //打印小数部分

double RoundUp(double N, int DecPlaces); //实现四舍五入

void PrintOut(unsigned int number);

void PrintDigit(unsigned int number);  //打印单个整数

#endif
