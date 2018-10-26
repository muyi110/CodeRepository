#include <iostream>
#include <string>

int main(int argc, char *argv[]){
    std::string str;
    for(decltype(str.size()) index = 1; index != argc; ++index){
        // 用 C 风格字符串初始化 string 对象
        str += std::string(argv[index]) + " ";
    }
    std::cout << str << std::endl;
    return 0;
}
