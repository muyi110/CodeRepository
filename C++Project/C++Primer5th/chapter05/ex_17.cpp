#include <iostream>
#include <vector>

bool is_prefix(std::vector<int> const &lhs, std::vector<int> const &rhs);
int main(){
    std::vector<int> ivec1 = {0, 1, 1, 2};
    std::vector<int> ivec2 = {0, 1, 1, 2, 3, 5, 8};
    
    bool result = is_prefix(ivec1, ivec2);
    std::cout << (result ? "yes" : "no") << std::endl;
    return 0;
}

bool is_prefix(const std::vector<int> &lhs, const std::vector<int> &rhs){
    if(lhs.size() > rhs.size()){
        return is_prefix(rhs, lhs);
    }
    for(decltype(lhs.size()) index = 0; index < lhs.size(); ++index){
        if(lhs[index] != rhs[index])
            return false;
    }
    return true;
}
