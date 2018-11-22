#include <iostream>
#include <vector>

int main(int argc, char *argv[]){
    std::vector<char> vec{'y', 'a', 'n', 'g'};
    // string 是顺序容器，因此可以用下面的初始化方法
    std::string str(vec.cbegin(), vec.cend());
    std::cout << str << std::endl;
    return 0;
}
