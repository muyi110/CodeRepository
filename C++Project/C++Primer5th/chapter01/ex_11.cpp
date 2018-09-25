#include <iostream>
/******************************************************
P11: 1.11
  提示用户输入两个整数，并打印所指定范围内的所有整数
******************************************************/

void print(int lo, int hi){
    while(lo <= hi){
        std::cout << lo << std::endl;
        ++lo;
    }
}

int main(void){
    int lo, hi;
    std::cout << "Please input two integers: " << std::endl;
    std::cin >> lo >> hi;
    if(lo <= hi){
        print(lo, hi);
    }
    else{
        print(hi, lo);
    }
    return 0;
}
