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

bool is_shorter(const std::string &s1, const std::string &s2){
    return s1.size() < s2.size();
 }

int main(int argc, char *argv[]){
    std::vector<std::string> words{"the", "quick", "red", "fox", "jumps", "over", "the", "slow", "red", "turtle"};
    elimDups(words);
    std::cout << "erase: " << std::endl;
    for(auto &s : words){
        std::cout << s << " ";
    }
    std::cout << std::endl;
    std::stable_sort(words.begin(), words.end(), is_shorter);
    std::cout << "stable sort: " << std::endl;
    for(auto &s : words){
        std::cout << s << " ";
    }
    std::cout << std::endl;
    return 0;
}
