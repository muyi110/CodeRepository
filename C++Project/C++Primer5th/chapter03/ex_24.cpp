#include <iostream>
#include <vector>

int main(){
    std::vector<int> ivec;
    for(int i; std::cin >> i; ivec.push_back(i)){;}
    if(ivec.size() < 2){
        std::cout << "enter at least two integers." << std::endl;
        return -1;
    }
    for(auto it = ivec.cbegin(); it != ivec.cend() - 1; ++it){
        std::cout << *it + *(it+1) << " ";
    }
    std::cout << std::endl;
    for(auto begin = ivec.cbegin(), end = ivec.cend()-1; begin <= end; ++begin, --end){
        if(begin == end){
            std::cout << *begin << " ";
            continue;
        }
        std::cout << (*begin) + (*end) << " ";
    }
    std::cout << std::endl;
    return 0;
}
