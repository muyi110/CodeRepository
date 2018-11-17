#include <iostream>
#include <vector>
#include <sstream>
#include <string>

struct PersonInfo {
    std::string name;
    std::vector<std::string> phones;
};

int main(int argc, char *argv[]){
    std::string line, word;
    std::vector<PersonInfo> people;
    std::istringstream record;
    while(std::getline(std::cin, line)){
        PersonInfo info;
        record.clear(); // 类比不能打开已经打开的文件一样，需要复位
        record.str(line);
        record >> info.name;
        while(record >> word){
            info.phones.push_back(word);
        }
        people.push_back(info);
    }
    for(const auto &p : people){
        std::cout << p.name << " ";
        for(const auto &s : p.phones){
            std::cout << s << " ";
        }
        std::cout << std::endl;
    }
    return 0;
}
