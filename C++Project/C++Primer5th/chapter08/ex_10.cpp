#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>

int main(int argc, char *argv[]){
    std::ifstream ifs("./ex_4.txt");
    if(!ifs){ // 判断文件是否打开成功
        std::cerr << "No data?" << std::endl;
        return -1;
    }
    std::vector<std::string> vecline;
    std::string line;
    while(std::getline(ifs, line)){
        vecline.push_back(line);
    }
    for(const auto &s : vecline){
        std::istringstream iss(s);// 将 string 转为流对象，可以使用 IO操作
        std::string word;
        while(iss >> word){
            std::cout << word << std::endl;
        }
    }
    return 0;
}
