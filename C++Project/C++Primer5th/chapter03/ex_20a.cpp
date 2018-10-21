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
    for(decltype(ivec.size())i = 0; i < ivec.size() - 1; ++i){
        std::cout << ivec[i] + ivec[i+1] << " ";
    }
    std::cout << std::endl;
    return 0;
}
