#include <iostream>
#include <vector>

int main(){
    std::vector<int> ivec;
    for(int i; std::cin >> i; ivec.push_back(i)){;}
    if(ivec.empty()){
        std::cout << "input at least one integer." << std::endl;
        return -1;
    }
    if(ivec.size() == 1){
        std::cout << "only one integer " << ivec[0] << std::endl;
        return -1;
    }
    auto size = ivec.size();
    std::vector<int>::size_type begin = 0;
    auto end = size - 1;
    while(begin <= end){
        if(begin != end)
            std::cout << ivec[begin++] + ivec[end--] << " ";
        else
            std::cout << ivec[begin++] << " ";
    }
    std::cout << std::endl;
    return 0;
}
