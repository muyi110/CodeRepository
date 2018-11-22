#include <iostream>
#include <algorithm>
#include <vector>

int main(int argc, char *argv[]){
    std::vector<int> vec;
    vec.reserve(10); // 分配至少可以容纳 10 个元素的空间（vec.size() = 0 ）
    // vec.resize(10); // 将容器元素个数改为 10 个( vec.size() = 10 )
    std::cout << "vec size: " << vec.size() << std::endl;
    // std::fill_n(vec.begin(), 10, 1); // 标准库算法不会改变容器大小
    std::fill_n(std::back_inserter(vec), 10, 1);
    for(auto i : vec){
        std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
