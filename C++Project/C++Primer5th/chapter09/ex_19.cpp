#include <iostream>
#include <list>
#include <string>

int main(int argc, char *argv[]){
    std::string word;
    std::list<std::string> lst;
    while(std::cin >> word){
        lst.emplace_back(word);
    }
    std::cout << "-------------------------------" << std::endl;
    for(auto first = lst.cbegin(), last = lst.cend(); first != last; ++first){
        std::cout << *first << " ";
    }
    std::cout << std::endl;
    return 0;
}
