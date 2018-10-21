#include <iostream>
#include <string>
#include <cctype>

int main(){
    std::string str; //empty string
    while(getline(std::cin, str)){
        if(str == "q"){
            break;
        }
        for(auto &c : str){
            if(ispunct(c)){
                continue;
            }
            std::cout << c;
        }
        std::cout << std::endl;
    }
    return 0;
}
