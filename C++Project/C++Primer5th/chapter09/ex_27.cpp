#include <iostream>
#include <forward_list>

int main(int argc, char *argv[]){
    std::forward_list<int> flst{0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

    auto prev = flst.cbefore_begin();
    auto curr = flst.cbegin();

    while(curr != flst.cend()){
        if(*curr % 2){
            curr = flst.erase_after(prev);
        }
        else {
            prev = curr;
            ++curr;
        }
    }
    for(auto i : flst){
        std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
