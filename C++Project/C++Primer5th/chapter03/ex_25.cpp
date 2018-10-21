#include <iostream>
#include <vector>

int main(){
    std::vector<unsigned int> scores(11, 0);
    unsigned int grade;
    auto begin = scores.begin();
    while(std::cin >> grade){
        if(grade <= 100){
            auto it = begin + grade / 10;
            ++(*it);
        }
    }
    for(auto g : scores){
        std::cout << g << " ";
    }
    std::cout << std::endl;
    return 0;
}
