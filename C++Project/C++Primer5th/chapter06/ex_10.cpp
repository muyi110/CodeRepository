#include <iostream>

void swap(int &lhs, int &rhs);
int main(){
    int l = 2, r = 4;
    std::cout << "l = " << l << " r = " << r << std::endl;
    swap(l, r);
    std::cout << "l = " << l << " r = " << r << std::endl;
    return 0;
}

void swap(int &lhs, int &rhs){
    int temp = lhs;
    lhs = rhs;
    rhs = temp;
}
