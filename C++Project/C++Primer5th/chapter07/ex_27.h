#ifndef CHA7_EX_23_24_H
#define CHA7_EX_23_24_H
#include <string>
#include <iostream>

class Screen{
public: 
    typedef std::string::size_type pos; // 类型成员，先定义后使用
    Screen() = default;
    Screen(pos ht, pos wd) : height(ht), width(wd), contents(ht * wd, ' '){ }
    Screen(pos ht, pos wd, char c) : height(ht), width(wd), contents(ht * wd, c){ }

    char get() const {return contents[cursor];}
    char get(pos ht, pos wd) const {return contents[ht * width + wd];} // 都是隐式内联
    Screen &move(pos r, pos c);
    Screen &set(char);
    Screen &set(pos, pos, char);
    Screen &display(std::ostream &os) {do_display(os); return *this;}
    const Screen &display(std::ostream &os) const {do_display(os); return *this;}
private:
    void do_display(std::ostream &os) const {os << contents;}
    pos cursor = 0;
    pos height = 0, width = 0;
    std::string contents;
};

inline Screen &Screen::move(pos r, pos c){
    pos row = r * width;
    cursor = row + c;
    return *this;
}

inline Screen &Screen::set(char c){
    contents[cursor] = c;
    return *this;
}

inline Screen &Screen::set(pos r, pos col, char ch){
    contents[r * width + col] = ch;
    return *this;
}
#endif
