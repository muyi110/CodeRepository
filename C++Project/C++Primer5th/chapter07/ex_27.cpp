#include <iostream>
#include "ex_27.h"

int main(int argc, char *argv[]){
    Screen myScreen(5, 5, 'X');
    myScreen.move(4, 0).set('#').display(std::cout);
    std::cout << "\n";
    myScreen.display(std::cout);
    std::cout << "\n";
    return 0;
}
