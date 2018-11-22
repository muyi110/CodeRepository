#include <iostream>
#include <list>
#include <forward_list>

std::list<int> &remove_even_and_double_odd(std::list<int> &lst){
    std::cout << "list: " << std::endl;
    auto iter = lst.cbegin();
    while(iter != lst.cend()){
        if(*iter % 2){
            iter = lst.emplace(iter, *iter);
            ++iter;
            ++iter;
        }
        else {
            iter = lst.erase(iter);
        }
    }
    return lst;
}
std::forward_list<int> &remove_even_and_double_odd(std::forward_list<int> &flst){
    std::cout << "forward_list: " << std::endl;
    auto prev = flst.cbefore_begin();
    auto iter = flst.cbegin();
    while(iter != flst.cend()){
        if(*iter % 2){
            iter = flst.emplace_after(prev, *iter);
            ++iter;
            prev = iter;
            ++iter;
        }
        else {
            iter = flst.erase_after(prev);
        }
    }
    return flst;
}

int main(int argc, char *argv[]){
    std::list<int> lst{0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    std::forward_list<int> flst{0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    remove_even_and_double_odd(lst);
    remove_even_and_double_odd(flst);
    for(auto i : lst){
        std::cout << i << " ";
    }
    std::cout << std::endl;
    for(auto i : flst){
        std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
