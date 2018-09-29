#include<iostream>
#include "Sales_item.h"

/********************************************************
P20: 1.21
  读取两个 ISBN 相同的 Sales_item 对象， 输出其和
********************************************************/
int main(void){
    Sales_item item1, item2;
    std::cin >> item1 >> item2;
    //检查 item1 与 item2 是否表示相同的书
    if(item1.isbn() == item2.isbn()){
        std::cout << item1 + item2 << std::endl;
        return 0;
    }
    else{
        std::cerr << "Data must refer to same ISBN" << std::endl;
        return -1;
    }
}
