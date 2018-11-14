#ifndef CHA7_EX_2_H
#define CHA7_EX_2_H
struct Sales_data{
    std::string isbn() const {return bookNo;}
    Sales_data &combine(const Sales_data &);

    std::string bookNo;
    unsigned int units_sold = 0;
    double revenue = 0.0;
};

Sales_data & Sales_data::combine(const Sales_data &rhs){
    units_sold += rhs.units_sold;
    revenue += rhs.revenue;
    return *this;
}

#endif
