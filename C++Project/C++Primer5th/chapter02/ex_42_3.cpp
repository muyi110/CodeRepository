#include <iostream>
#include "ex_42.h"

int main(){
    Sales_data total;
    double total_price;
    if(std::cin >> total.bookNo >> total.units_sold >> total_price){
        total.calc_revenue(total_price);
        Sales_data trans;
        double trans_price;
        while(std::cin >> trans.bookNo >> trans.units_sold >> trans_price){
            trans.calc_revenue(trans_price);
            if(total.bookNo == trans.bookNo){
                total.add_data(trans);
            }
            else{
                total.print();
                total.set_data(trans);
            }
        }
        total.print();
        return 0;
    }
    else{
        std::cerr << "No data!" << std::endl;
        return -1;
    }
}
