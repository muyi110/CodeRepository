#include <iostream>
#include <sstream>
#include <string>

std::istream &func(std::istream &is){
     std::string buf;
     while(is >> buf){
         std::cout << buf << std::endl;
     }
     is.clear();
     return is;
}

int main(int argc, char *argv[]){
    std::istringstream iss("hello world");
    func(iss);
    return 0;
}
