#ifndef CHA7_EX_2_H
#define CHA7_EX_2_H
struct Sales_data{
    std::string isbn() const {return bookNo;}
    Sales_data &combine(const Sales_data &);
    double avg_price() const{return revenue / units_sold;}

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
    os << item.isbn() << " " << item.units_sold << " " << item.revenue << " " << item.avg_price();
    return os;
}
Sales_data add(const Sales_data &lhs, const Sales_data &rhs){
    Sales_data sum = lhs;
    sum.combine(rhs);
    return lhs;
}
#endif
