#include <iostream>
#include <vector>

int main(){
    std::vector<int> ivec;
    for(std::vector<int>::size_type number = 0; number < 10; ++number){
        ivec.push_back(number);
    }
    for(auto it = ivec.begin(); it != ivec.end(); ++it){
        *it *= 2;
    }
    for(auto element : ivec){
        std::cout << element << " ";
    }
    std::cout << std::endl;
    return 0;
}
