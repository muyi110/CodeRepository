#include <iostream>
#include <vector>
#include <cctype>

int main(){
    std::vector<std::string> text; // empty vector
    for(std::string word; getline(std::cin, word); text.push_back(word)){;}
    for(auto it = text.begin(); it != text.end() && !it->empty(); ++it){
        for(auto &c : *it){
            if(isalpha(c)){
                c = toupper(c);
            }
        }
        std::cout << *it << std::endl;
    }
    return 0;
}
