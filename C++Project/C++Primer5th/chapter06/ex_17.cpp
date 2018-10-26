#include <iostream>
#include <string>
#include <cctype>

bool any_capital(const std::string &s){
    for(auto &c : s){
        if(isupper(c))
            return true;
    }
    return false;
}

void to_lowercase(std::string &s){
    for(auto &c : s){
        c = tolower(c);
    }
}

int main(){
    std::string str("YangLiuqing");
    std::cout << any_capital(str) << std::endl;
    to_lowercase(str);
    std::cout << str << std::endl;
    return 0;
}
