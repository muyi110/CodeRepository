#include <iostream>
#include <vector>
#include <cstddef>

int main(){
    std::vector<int> ivec;
    int arr[10];
    size_t t = 0;
    for(int i = 0; i < 10; ++i){
        ivec.push_back(i);
    }
    for(std::vector<int>::size_type index = 0; index < ivec.size(); ++index){
        arr[t++] = ivec[index];
    }
    for(auto e : arr){
        std::cout << e << " ";
    }
    std::cout << std::endl;
    return 0;
}
