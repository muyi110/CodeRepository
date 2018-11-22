#include <iostream>
#include <deque>
#include <string>

int main(int argc, char *argv[]){
    std::string word;
    std::deque<std::string> deq;
    while(std::cin >> word){
        deq.emplace_back(word);
    }
    std::cout << "-------------------------------" << std::endl;
    for(auto first = deq.cbegin(), last = deq.cend(); first != last; ++first){
        std::cout << *first << " ";
    }
    std::cout << std::endl;
    return 0;
}
