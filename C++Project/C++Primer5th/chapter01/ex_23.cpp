#include <iostream>
#include "Sales_item.h"

/*******************************************************
* P21: 1.23
*   读取多条销售记录，并统计每个 ISBN (每本书) 有几条
*   销售记录。
*******************************************************/
int main(void){
    Sales_item item;
    int count = 0;
    if(std::cin >> item){
        Sales_item trans;
        count = 1;
        while(std::cin >> trans){
            if(item.isbn() == trans.isbn()){
                ++count;
            }
            else{
                std::cout << item << "\t" << count << std::endl;
                item = trans;
                count = 1;
            }
        }
        std::cout << item << "\t" << count << std::endl;
    }
    return 0;
}
