#include<iostream>
#include "Sales_item.h"

/******************************************************
P20: 1.20
  读取一组书籍的销售记录，将每条记录打印到标准输出上
******************************************************/
int main(void){
    for(Sales_item item1; std::cin >> item1; std::cout << item1 << std::endl);
    return 0;
}
