#include <iostream>
#include <vector>
#include <iterator>

int main(){
    int arr[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    std::vector<int> ivec(std::begin(arr), std::end(arr));
    for(auto i : ivec){
        std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
