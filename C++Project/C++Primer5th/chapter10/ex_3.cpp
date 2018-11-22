#include <iostream>
#include <algorithm>
#include <vector>

int main(int argc, char *argv[]){
    std::vector<int> vec{1, 2, 3, 4, 5, 6, 7, 8, 9};
    int sum = std::accumulate(vec.cbegin(), vec.cend(), 0);
    std::cout << sum << std::endl;
    return 0;
}
