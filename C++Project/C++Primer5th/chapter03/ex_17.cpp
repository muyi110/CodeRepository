#include <iostream>
#include <vector>
#include <string>
#include <cctype>

int main(){
    std::string word;
    std::vector<std::string> words;
    getline(std::cin, word);
    for(auto &w : word){
        w = toupper(w);
    }
    words.push_back(word);
    for(auto wo : words){
        std::cout << wo << std::endl;
    }
    return 0;
}
