#include <iostream>
#include <cstddef>

int main(){
    constexpr size_t sz = 10;
    int arr[sz];
    for (size_t index = 0; index < sz; ++index){
        arr[index] = 0;
    }
    for(auto ele : arr){
        std::cout << ele << " ";
    }
    std::cout << std::endl;
    return 0;
}
