#include <iostream>
#include <list>
#include <deque>

int main(int argc, char *argv[]){
    std::deque<int> even;
    std::deque<int> odd;
    std::list<int> lst{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    for(const auto i : lst){
        (i & 0x01 ? odd : even).emplace_back(i);
    }
    std::cout << "odd number:" << std::endl;
    for(const auto i : odd){
        std::cout << i << " ";
    }
    std::cout << std::endl;
    std::cout << "even number:" << std::endl;
    for(const auto i : even){
        std::cout << i << " ";
    }
    std::cout << std::endl;
}
