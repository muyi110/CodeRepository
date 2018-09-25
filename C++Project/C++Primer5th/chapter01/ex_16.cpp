#include <iostream>
/**************************************************************
P15: 1.16
  编写程序，从 cin 读取一组数，输出其和。
**************************************************************/
int main(void){
    int value = 0, sum = 0;
    //cin-->遇到文件结束符或无效输入时 istream 对象(cin) 无效
    //无效的 istream 对象使得条件为假。
    //cin 遇到空格、换行符跳过
    while(std::cin >> value){
        sum += value;
    }
    std::cout << sum << std::endl;
}
