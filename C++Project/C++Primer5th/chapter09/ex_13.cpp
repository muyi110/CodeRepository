#include <iostream>
#include <vector>
#include <list>

int main(int argc, char *argv[]){
    std::list<int> ilst(5, 4);
    std::vector<int> ivec(5, 5);

    std::vector<double> dvec(ilst.cbegin(), ilst.cend());
    for(auto &i : ilst){
        std::cout << i;
    }
    std::cout << std::endl;
    for(auto &i : dvec){
        std::cout << i;
    }
    std::cout << std::endl;

    std::vector<double> dvec_(ivec.cbegin(), ivec.cend());
    for(auto &i : ivec){
        std::cout << i;
    }
    std::cout << std::endl;
    for(auto &i : dvec_){
        std::cout << i;
    }
    std::cout << std::endl;
    return 0;
}
