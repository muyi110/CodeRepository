#ifndef CHA7_EX_23_24_H
#define CHA7_EX_23_24_H
#include <string>

class Screen{
public: 
    typedef std::string::size_type pos; // 类型成员，先定义后使用
    Screen() = default;
    Screen(pos ht, pos wd) : height(ht), width(wd), contents(ht * wd, ' '){ }
    Screen(pos ht, pos wd, char c) : height(ht), width(wd), contents(ht * wd, c){ }

    char get() const {return contents[cursor];}
    char get(pos ht, pos wd) const {return contents[ht * width + wd];} // 都是隐式内联
private:
    pos cursor = 0;
    pos height = 0, width = 0;
    std::string contents;
};

#endif
