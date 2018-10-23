#include <iostream>
#include <string>

int main(){
    std::string duplicate_word, temp_word;
    unsigned int count = 1;     // 重复字符的次数
    bool duplicate_word_flag = false;
    std::cin >> duplicate_word; // 读取第一个单词
    while(std::cin >> temp_word){
        if(temp_word == duplicate_word){
            ++count;
            duplicate_word_flag = true;
        }
        else{
            if(count > 1){
                std::cout << duplicate_word << ": occurs " << count << " times" << std::endl;
            }
            duplicate_word = temp_word;
            count = 1;
        }
    }
    if(!duplicate_word_flag){
        std::cout << "No duplicate" << std::endl;
    }
    if(count > 1){
        std::cout << duplicate_word << ": occurs " << count << " times" << std::endl;
    }
    return 0;
}
