#include <iostream>
#include <initializer_list>

int sum(std::initializer_list<int> params){
    int sum = 0;
    for(const int &para : params){
        sum += para;
    }
    return sum;
}
int main(int argc, char *argv[]){
    std::cout << sum({1,2,3,4}) << std::endl;
    return 0;
}
