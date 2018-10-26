#include <iostream>
#include <vector>
//#define NDEBUG
typedef std::vector<int>::const_iterator iterator;
void print(iterator begin, iterator end){
#ifndef NDEBUG
    std::cout << end - begin << std::endl;
#endif
    if(begin != end){
        std::cout << *begin << " ";
        ++begin;
        print(begin, end);
    }
    return;
}

int main(int argc, char *argv[]){
    std::vector<int> ivec{1, 2, 3, 4, 5};
    print(ivec.begin(), ivec.end());
    std::cout << std::endl;
    return 0;
}
