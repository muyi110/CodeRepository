#include <iostream>
#include <list>
#include <vector>

int main(int argc, char *argv[]){
    std::list<int> ilst{1, 2, 3, 4, 5};
    std::vector<int> vec1{1, 2, 3, 4, 5};
    std::vector<int> vec2{1, 2, 3, 4};

    std::cout << "list element == vec1 ? " << (std::vector<int>(ilst.cbegin(), ilst.cend()) == vec1 ? "true" : "false") << std::endl;
    std::cout << "list element == vec2 ? " << (std::vector<int>(ilst.cbegin(), ilst.cend()) == vec2 ? "true" : "false") << std::endl;
    return 0;
}
