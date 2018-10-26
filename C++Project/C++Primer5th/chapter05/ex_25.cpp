#include <iostream>
#include <stdexcept>

int main(){
    int i = 0, j = 0;
    while(std::cin >> i >> j){
        try{
            if(j == 0){
                throw std::runtime_error("divisor is 0");
            }
            std::cout << i / j << std::endl;
        }
        catch(std::runtime_error error){
            std::cout << error.what() << "\nTry again? Enter y or n" << std::endl;
            char c;
            std::cin >> c;
            if(!std::cin || c == 'n'){  // 首先对输入的有效性判断
                break;
            }
        }
    }
    return 0;
}
