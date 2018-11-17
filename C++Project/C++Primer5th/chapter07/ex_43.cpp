#include <iostream>
#include <vector>

class NoDefault {
public:
    NoDefault(int i) { std::cout << "class NoDefault" << std::endl;}
};
// 类的初始化是通过构造函数完成，def(0) 会调用对应的构造函数进行初始化
class C {
public:
    C() : def(0) {std::cout << "class C" << std::endl;}
private:
    NoDefault def;
};

int main(int argc, char *argv[]){
    C c;
    std::vector<C> vec(10);
    return 0;
}
