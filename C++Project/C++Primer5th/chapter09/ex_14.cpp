#include <iostream>
#include <list>
#include <vector>
#include <string>

int main(int argc, char *argv[]){
    std::list<const char *> clist{"hello", "world"}; // 字符串常量
    std::vector<std::string> svec;
    svec.assign(clist.cbegin(), clist.cend());
    for(auto &s : svec){
        std::cout << s << " ";
    }
    std::cout << std::endl;
    return 0;
}
