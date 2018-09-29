#include<iostream>
#include "Sales_item.h"

/***************************************************
P20: 1.22
  读取多条具有相同 ISBN 的销售记录，输出所有记录的和 
***************************************************/
int main(void){
    Sales_item total;
    if(std::cin >> total){
        Sales_item trans;
        while(std::cin >> trans){
            if(total.isbn() == trans.isbn()){
                total += trans;
            }
            else{
                std::cout << total << std::endl;
                total = trans;
            }
        }
        std::cout << total << std::endl;
    }
}
