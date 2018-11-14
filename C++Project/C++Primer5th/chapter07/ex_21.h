#ifndef CHA7_EX_2_H
#define CHA7_EX_2_H
class Sales_data{
friend std::istream &read(std::istream &is, Sales_data &item);
friend std::ostream &print(std::ostream &os, const Sales_data &item);
friend Sales_data add(const Sales_data &lhs, const Sales_data &rhs);

public:
    Sales_data() = default;
    Sales_data(const std::string &s) : bookNo(s) { }
    Sales_data(const std::string &s, unsigned int n, double p) : bookNo(s), units_sold(n), revenue(p){ }
    Sales_data(std::istream &);

    std::string isbn() const {return bookNo;}
    Sales_data &combine(const Sales_data &);
    // double avg_price() const{return revenue / units_sold;}
private:
    std::string bookNo;
    unsigned int units_sold = 0;
    double revenue = 0.0;
};
// 成员函数
Sales_data & Sales_data::combine(const Sales_data &rhs){
    units_sold += rhs.units_sold;
    revenue += rhs.revenue;
    return *this;
}
// 非成员函数
std::istream &read(std::istream &is, Sales_data &item){
    double price = 0; // 局部变量需要初始化
    is >> item.bookNo >> item.units_sold >> price;
    item.revenue = price * item.units_sold;
    return is;
}
std::ostream &print(std::ostream &os, const Sales_data &item){
    os << item.isbn() << " " << item.units_sold << " " << item.revenue;
    return os;
}
Sales_data add(const Sales_data &lhs, const Sales_data &rhs){
    Sales_data sum = lhs;
    sum.combine(rhs);
    return lhs;
}
// 构造函数
Sales_data::Sales_data(std::istream &is){
    read(is, *this);
}
#endif
