#include <iostream>
#include <cstddef>
int main(){
    constexpr size_t rowCnt = 3, colCnt = 4;
    int ia[rowCnt][colCnt] = {{0, 1, 2, 3}, {4, 5, 6, 7}, {8, 9, 10, 11}};
    for(const int (&row)[colCnt] : ia){
        for(const int &col : row){
            std::cout << col << " ";
        }
        std::cout << std::endl;
    }
    std::cout << "====================================" << std::endl;
    // for loop
    for(size_t row  = 0; row < rowCnt; ++row){
        for(size_t col = 0; col < colCnt; ++col){
            std::cout << ia[row][col] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << "====================================" << std::endl;
    // for loop pointer
    for(const int (*p)[colCnt] = ia; p != ia + rowCnt; ++p){
        for(const int *q = *p; q != *p + colCnt; ++q){
            std::cout << *q << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
