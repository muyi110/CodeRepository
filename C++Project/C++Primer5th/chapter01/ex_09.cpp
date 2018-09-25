#include <iostream>
/*********************************************************
P11: 1.9
使用 while 循环将 50 到 100 的整数相加
*********************************************************/
int sum(int lo, int hi){
    int result;
    while(lo <= hi){
        result += lo;
        ++lo; 
    }
    return result; 
}

int main(void){
    std::cout << "sum of 50 to 100 is: " << sum(50, 100) << std::endl;
    return 0;
}
