#ifndef EX_41_H
#define EX_41_H
#include <string>
#include <iostream>

class Sales_data{
    friend std::istream &read(std::istream &is, Sales_data &item);
    friend std::ostream &print(std::ostream &os, const Sales_data &item);
    friend Sales_data add(const Sales_data &lhs, const Sales_data &rhs);
public:
    Sales_data(const std::string &s, unsigned n, double p):bookNo(s), units_sold(n), revenue(n*p){std::cout << "Sales_data(const std::string &, unsigned, double)" << std::endl;}
    Sales_data():Sales_data("", 0, 0.0f){std::cout << "Sales_data()" << std::endl;}
    Sales_data(const std::string &s):Sales_data(s, 0, 0.0f){std::cout << "Sales_data(const std::string &)" << std::endl;}
    Sales_data(std::istream &is);

    std::string isbn() const{return bookNo;}
    Sales_data &combine(const Sales_data&);
private:
    inline double avg_price() const;
    std::string bookNo;
    unsigned units_sold = 0;
    double revenue = 0.0;
};
std::istream &read(std::istream &is, Sales_data &item);
Sales_data::Sales_data(std::istream &is):Sales_data(){
    std::cout << "Sales_data(std::istream &is)" << std::endl;
    read(is, *this);
}

Sales_data &Sales_data::combine(const Sales_data &rhs){
    units_sold += rhs.units_sold;
    revenue += rhs.revenue;
    return *this;
}

inline double Sales_data::avg_price() const{
    return units_sold ? revenue / units_sold : 0;
}

std::istream &read(std::istream &is, Sales_data &item){
    double price = 0;
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
    return sum;
}
#endif
