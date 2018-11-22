#include <iostream>
#include <vector>

int main(int argc, char *argv[]){
    std::vector<int> vec1{1, 2, 3, 4, 5};
    std::vector<int> vec2{1, 2, 3, 4, 5};
    std::vector<int> vec3{1, 2, 3, 4};

    std::cout << "vec1 == vec2 ? " << (vec1 == vec2 ? "true" : "false") << std::endl;
    std::cout << "vec1 == vec3 ? " << (vec1 == vec3 ? "true" : "false") << std::endl;
    return 0;
}
