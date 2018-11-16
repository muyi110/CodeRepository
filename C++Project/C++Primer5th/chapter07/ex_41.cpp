#include "ex_41.h"

int main(int argc, char *argv[]){
    std::cout << "1. default way: " << std::endl;
    std::cout << "----------------" << std::endl;
    Sales_data s1;   
    
    std::cout << "\n2. use std::string as parameter: " << std::endl;
    std::cout << "----------------" << std::endl;
    Sales_data s2("CPP-Primer-5th");
    
    std::cout << "\n3. complete parameters: " << std::endl;
    std::cout << "----------------" << std::endl;
    Sales_data s3("CPP-Primer-5th", 3, 25.8);
    
    std::cout << "\n4. use istream as parameter: " << std::endl;
    std::cout << "----------------" << std::endl;
    Sales_data s4(std::cin);
    
    return 0;
}
