#include <iostream>
#include "ex_42.h"

int main(){
    Sales_data book;
    double price;
    std::cin >> book.bookNo >> book.units_sold >> price;
    book.calc_revenue(price);
    book.print();
    return 0;
}
