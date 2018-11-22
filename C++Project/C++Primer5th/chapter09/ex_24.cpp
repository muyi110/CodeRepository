#include <iostream>
#include <vector>

int main(int argc, char *argv[]){
    std::vector<int> vec{1, 2, 3};
    std::cout << "[]: " << vec[0] << std::endl;
    std::cout << "at: " << vec.at(0) << std::endl;
    std::cout << "front: " << vec.front() << std::endl;
    std::cout << "begin: " << *vec.begin() << std::endl;
    return 0;
}
