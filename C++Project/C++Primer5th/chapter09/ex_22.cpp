#include <iostream>
#include <vector>

void insert(std::vector<int> &v, int value){
    auto mid = [&]{return v.begin() + v.size() / 2;}; // lambda 表达式，第 10 章有介绍
    for(auto curr = v.begin(); curr <= mid(); ++curr){ //每次都获取新的迭代器, 避免每次插入后迭代器失效
        if(*curr == value){
            ++(curr = v.insert(curr, 2 * value));
        }
    }
}

int main(int argc, char *argv[]){
    std::vector<int> v{1, 2, 3, 4, 5, 6};
    insert(v, 1);
    for(auto i : v){
        std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
