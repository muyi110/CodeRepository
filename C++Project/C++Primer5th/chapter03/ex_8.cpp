#include <iostream>
#include <string>

int main(){
    std::string str("a sample example.");
    decltype(str.size()) index;
    //for
    for(index = 0; index < str.size(); ++index){
        str[index] = 'X';
    }
    std::cout << str << std::endl;
    //while
    while(index < str.size()){
        str[index] = 'X';
        ++index;
    }
    std::cout << str << std::endl;
    return 0;
}
