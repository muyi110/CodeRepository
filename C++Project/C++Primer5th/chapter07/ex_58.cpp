#include <iostream>
#include <vector>

class Example {
public:
    static constexpr double rate = 6.5;
    static const int vecSize = 20;
    static int a;
    static std::vector<double> vec;
};
constexpr double Example::rate;
const int Example::vecSize;
int Example::a = 2;
std::vector<double> Example::vec(20);

int main(int argc, char *argv[]){
    std::cout << "Hello World" << std::endl;
    std::cout << Example::vecSize << " " << Example::rate << " " << Example::a << std::endl;
    return 0;
}
