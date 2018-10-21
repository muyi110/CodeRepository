#include <iostream>
#include <string>

int main(){
    std::string str("a sample example.");
    for (auto &c : str){
        c = 'X';
    }
    std::cout << str << std::endl;
    return 0;
}
