#include <iostream>
#include <string>

int main(){
    unsigned int grade = 0;
    std::string finalgrade = "";
    std::cin >> grade;
    finalgrade = (grade > 90) ? "high pass" : (grade >= 60 && grade < 75) ? "low pass" : (grade < 60) ? "fail" : "pass";
    std::cout << finalgrade << std::endl;
    std::cout << "=====================================" << std::endl;
    if(grade > 90) finalgrade = "high pass";
    else if(grade < 60) finalgrade = "fail";
    else if(grade < 75) finalgrade = "low pass";
    else finalgrade = "pass";
    std::cout << finalgrade << std::endl;
    return 0;
}
