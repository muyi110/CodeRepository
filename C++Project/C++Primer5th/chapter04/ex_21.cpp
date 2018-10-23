#include <iostream>
#include <vector>

int main(){
    std::vector<int> ivec{1, 2, 3, 4, 5, 6, 7};
    for(auto &c : ivec){
        std::cout << ((c % 2 != 0) ? (c *= 2) : c) << " ";
    }
    std::cout << std::endl;
    return 0;
}
