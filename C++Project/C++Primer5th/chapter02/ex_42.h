#ifndef CH02_EX42_H_
#define CH02_EX42_H_
#include <iostream>
#include <string>
/********************************************************
 * 重写 sales_data.h 文件
********************************************************/
struct Sales_data{
    std::string bookNo;
    unsigned units_sold = 0;
    double revenue = 0.0;

    void calc_revenue(double price);
    double calc_average_price();
    void set_data(Sales_data data);
    void add_data(Sales_data data);
    void print();
};
void Sales_data::calc_revenue(double price){
    revenue = units_sold * price;
}
double Sales_data::calc_average_price(){
    if(units_sold != 0){
        return revenue / units_sold;
    }
    else{
        return 0.0;
    }
}
void Sales_data::set_data(Sales_data data){
    bookNo = data.bookNo;
    units_sold = data.units_sold;
    revenue = data.revenue;
}
void Sales_data::add_data(Sales_data data){
    if(bookNo != data.bookNo) return;
    units_sold += data.units_sold;
    revenue += data.revenue;
}
void Sales_data::print(){
    std::cout << bookNo << " " << units_sold << " " << revenue << " ";
    double average_price = calc_average_price();
    if (average_price != 0.0){
        std::cout << average_price << std::endl;
    }
    else{
        std::cout << "no sales" << std::endl;
    }
}
#endif
