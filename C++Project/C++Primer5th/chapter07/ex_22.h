#ifndef CHA7_EX_9_H
#define CHA7_EX_9_H
struct Person;
std::istream &read(std::istream &is, Person &item);

struct Person{
friend std::istream &read(std::istream &is, Person &item);     // 友元声明，为了访问类的非公有成员
friend std::ostream &print(std::ostream &os, const Person &item);

public:
    Person() = default;
    Person(const std::string &sname, const std::string &saddress) : name(sname), address(saddress){ }
    Person(std::istream &is){read(is, *this);}

    std::string &getName() const {return name;}  // 成员函数，返回引用类型，避免对字符串的 copy 
    std::string &getAddress() const {return address;}
private:
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