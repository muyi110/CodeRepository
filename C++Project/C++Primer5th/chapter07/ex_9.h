#ifndef CHA7_EX_9_H
#define CHA7_EX_9_H
struct Person{
    std::string &getName() const {return name;}  // 成员函数，返回引用类型，避免对字符串的 copy 
    std::string &getAddress() const {return address;}

    std::string name;
    std::string address;
};

// 非成员函数
std::istream &read(std::istream &is, Person &item){
    is >> item.name >> item.address;
    return is
}
std::ostream &print(std::ostream &os, const Person &item){
    os << item.name << " " << item.address << " ";
    return os;
}
#endif
