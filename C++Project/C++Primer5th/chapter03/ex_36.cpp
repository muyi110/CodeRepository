#include <iostream>
#include <cstddef>
#include <vector>
#include <iterator>

bool compare(const int *const pb1, const int *const pe1, const int *const pb2, const int *const pe2);
int main(){
    int arr1[3] = {0, 1, 2};
    int arr2[3] = {0, 1, 2};
    if(compare(std::begin(arr1), std::end(arr1), std::begin(arr2), std::end(arr2))){
        std::cout << "equal" << std::endl;
    }
    else{
        std::cout << "not equal" << std::endl;
    }
    std::cout << "=========================================" << std::endl;
    std::vector<int> ivec1{0, 1, 2};
    std::vector<int> ivec2{0, 1, 3};
    if(ivec1 == ivec2){
        std::cout << "equal" << std::endl;
    }
    else{
        std::cout << "not equal" << std::endl;
    }
    return 0;
}

bool compare(const int *const pb1, const int *const pe1, const int *const pb2, const int *const pe2){
    if(pe1 - pb1 != pe2 - pb2){
        return false;
    }
    else{
        for(auto i = pb1, j = pb2; (i != pe1 && j != pe2); ++i, ++j){
            if(*i != *j)
                return false;
        }
    }
    return true;
}
