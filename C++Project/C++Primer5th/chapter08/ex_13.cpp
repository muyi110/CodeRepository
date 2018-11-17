#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

struct PersonInfo {
    std::string name;
    std::vector<std::string> phones;
};

bool valid(const std::string &str){
    return std::isdigit(str[0]);
}

std::string format(const std::string &str){
    return str.substr(0,3) + "-" + str.substr(3,3) + "-" + str.substr(6);
}

int main(int argc, char *argv[]){
    std::ifstream ifs("./phones.txt");
    if(!ifs){ // 对 IO 的操作需要判断其有效性
        std::cerr << "No phone number?" << std::endl;
        return -1;
    }
    std::string line, word;
    std::vector<PersonInfo> people;
    std::istringstream record;
    while(std::getline(ifs, line)){
        PersonInfo info;
        record.clear();
        record.str(line);
        record >> info.name;
        while(record >> word){
            info.phones.push_back(word);
        }
        people.push_back(info);
    }
    for(const auto &entry : people){
        std::ostringstream formatted, badNums;
        for(const auto &nums : entry.phones){
            if(!valid(nums)) badNums << " " << nums;
            else formatted << " " << format(nums);
        }
        if(badNums.str().empty()){
            std::cout << entry.name << " " << formatted.str() << std::endl;
        }
        else{
            std::cerr << "input error" << entry.name << "invalid number(s)" << badNums.str() << std::endl;
        }
    }
    return 0;
}
