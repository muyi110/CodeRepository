#include <iostream>
#include <string>
#include "ex_6.h"

int main(int argc, char *argv[]){
    Sales_data total;
    if(read(std::cin, total)){
        Sales_data trans;
        while(read(std::cin, trans)){
            if(total.isbn() == trans.isbn()){
                total.combine(trans);
            }
            else{
                print(std::cout, total);
                std::cout << std::endl;
                total = trans; // 只是拷贝数据成员
            }
        }
        print(std::cout, total);
        std::cout << std::endl;
    }
    else{
        std::cerr << "No data?!" << std::endl;
    }
    return 0;
}
