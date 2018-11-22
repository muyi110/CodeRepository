#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

void elimDups(std::vector<std::string> &words){
    std::sort(words.begin(), words.end());
    std::cout << "sort: " << std::endl;
    for(auto &s : words){
        std::cout << s << " ";
    }
    std::cout << std::endl;
    auto end_unique = std::unique(words.begin(), words.end());
    std::cout << "unique: " << std::endl;
    for(auto &s : words){
        std::cout << s << " ";
    }
    std::cout << std::endl;
    words.erase(end_unique, words.end());
}

int main(int argc, char *argv[]){
    std::vector<std::string> words{"the", "quick", "red", "fox", "jumps", "over", "the", "slow", "red", "turtle"};
    elimDups(words);
    std::cout << "erase: " << std::endl;
    for(auto &s : words){
        std::cout << s << " ";
    }
    std::cout << std::endl;
    return 0;
}
