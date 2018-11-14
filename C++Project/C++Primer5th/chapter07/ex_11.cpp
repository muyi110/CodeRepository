#include <iostream>
#include <string>
#include "ex_21.h"

int main(int argc, char **argv){
    Sales_data item1;
    print(std::cout, item1) << std::endl;
    Sales_data item2("yangliuqing");
    print(std::cout, item2) << std::endl;
    Sales_data item3("yangliuqing", 6, 20);
    print(std::cout, item3) << std::endl;
    Sales_data item4(std::cin);
    print(std::cout, item4) << std::endl;
}
