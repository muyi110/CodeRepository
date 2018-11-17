#include <iostream>
#include <string>

std::istream & func(std::istream &is){
    std::string buf;
    while(is >> buf){
        std::cout << buf << std::endl;
    }
    is.clear(); // 对流进行复位，使其处于有效状态
    return is;
}

int main(int argc, char *argv[]){
    std::istream &is = func(std::cin);
    std::cout << is.rdstate() << std::endl;
    return 0;
}
