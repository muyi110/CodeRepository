#include <fstream>
#include <vector>
#include <string>
#include <iostream>

void read_file_to_vector(const std::string &fileName, std::vector<std::string> &vec){
    std::ifstream ifs(fileName);
    if(ifs){ // 判断文件是否打开成功
        std::string buf;
        while(ifs >> buf){
            vec.push_back(buf);
        }
    }
}

int main(int argc, char *argv[]){
    std::vector<std::string> vec;
    read_file_to_vector("./ex_4.txt", vec);
    for(const auto &str : vec){
        std::cout << str << std::endl;
    }
    return 0;
}
