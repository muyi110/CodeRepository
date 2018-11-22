#include <iostream>
#include <forward_list>
#include <string>

auto find_and_insert(std::forward_list<std::string> &flst, const std::string &s1, const std::string &s2) -> std::forward_list<std::string> & {
    auto prev = flst.cbefore_begin();
    auto curr = flst.cbegin();
    while(curr != flst.cend()){
        if(*curr == s1){
            flst.emplace_after(prev, s2);
            return flst;
        }
        else{
            prev = curr;
            ++curr;
        }
    }
    flst.emplace_after(prev, s2);
    return flst;
}

int main(int argc, char *argv[]){
    std::forward_list<std::string> flst{"yang", "liu", "qing", "hello", "world"};
    std::string s1("qing"), s2("study");
    auto result = find_and_insert(flst, s1, s2);
    for(auto &s : result){
        std::cout << s << " ";
    }
    std::cout << std::endl;
    return 0;
}
