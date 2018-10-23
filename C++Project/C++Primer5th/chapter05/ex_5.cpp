#include <iostream>
#include <vector>
#include <string>

int main(){
    const std::vector<std::string> scores = {"F", "D", "C", "B", "A", "A++"};
    std::string lettergrade;
    for(int grade = 0; std::cin >> grade;){
        if(grade < 60){
            lettergrade = scores[0];
        }
        else{
            lettergrade = scores[(grade - 50) / 10];
            if(grade != 100){
                lettergrade += (grade % 10) > 7 ? "+" : ((grade % 10) < 3) ? "-" : "";
            }
        }
        std::cout << lettergrade << std::endl;
    }
    return 0;
}
