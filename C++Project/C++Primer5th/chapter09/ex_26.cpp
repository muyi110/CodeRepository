#include <iostream>
#include <list>
#include <vector>
#include <iterator>

int main(int argc, char *argv[]){
    int ia[] = {0, 1, 1, 2, 3, 5, 8, 13, 21, 55, 89};

    std::vector<int> vec(std::begin(ia), std::end(ia));
    std::list<int> lst(std::begin(ia), std::end(ia));

    for(auto it = lst.cbegin(); it != lst.cend();){
        if(*it % 2) 
            it = lst.erase(it);
        else 
            ++it;
    }
    for(auto it = vec.cbegin(); it != vec.cend();){
        if(!(*it % 2))
            it = vec.erase(it);
        else
            ++it;
    }
    std::cout << "list without odd: " << std::endl;
    for(auto i : lst){
        std::cout << i << " ";
    }
    std::cout << std::endl;
    std::cout << "vector without even: " << std::endl;
    for(auto i : vec){
        std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
