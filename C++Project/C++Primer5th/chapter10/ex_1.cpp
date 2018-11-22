#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <list>

int main(int argc, char *argv[]){
    std::vector<int> vec{1, 2, 3, 4, 2, 1, 2, 2, 3, 4, 7, 9, 2, 1, 2, 4, 4, 2, 5};
    int value = 2;
    auto value_count = std::count(vec.cbegin(), vec.cend(), value);
    std::cout << "value " << value << " occures " << value_count << " times" << std::endl;

    std::list<std::string> lst{"yang", "liu", "qing", "good", "good", "study"};
    std::string value_string = "good";
    auto value_string_count = std::count(lst.cbegin(), lst.cend(), value_string);
    std::cout << "value " << value_string << " occures " << value_string_count << " times" << std::endl;
    return 0;
}
