#include <iostream>
#include <vector>

int main(int argc, char *argv[]){
    std::vector<std::string> vec;
    for(std::string buff; std::cin >> buff; vec.emplace_back(buff)){
        std::cout << vec.capacity() << std::endl;
    }
    return 0;
}
