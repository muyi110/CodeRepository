#include <iostream>
#include <ctime>

/*
  Three methods for fib(n) = fib(n-1) + fib(b-2) 
*/

//Method_one: recursive method, time complexity is O(2^n).
//---------This method is bad.-------------
int fib_recursive_method(int n){
    return(n < 2) ? n : fib_recursive_method(n-1) + fib_recursive_method(n-2);
}

//Method_two: linear recursive method, time complexity is O(n).
//---------This method is better.----------
int fib_linear_recursive_method(int n, int *prev){
    if(0 == n){
        *prev = 1;
        return 0;
    }
    else{
        int prevPrev;
        *prev = fib_linear_recursive_method(n-1, &prevPrev);
        return prevPrev + (*prev);
    }
}

//Method_three: iteration method, time complexity is O(n).
//----------This method is best.------------
int fib_iteration_method(int n){
    int f = 1, g = 0;
    while(0 < n--){
        g += f;
        f = g - f;
    }
    return g;
}

//------------------------main function-------------------------
int main(int argc, char *argv[]){
    clock_t startTime, endTime;
    int result;
    int n = 45;
    int prev;
    std::cout << "---------iteration method--------------\n" << std::endl;
    startTime = clock();
    result = fib_iteration_method(n);
    endTime = clock();
    std::cout << "Result: " << result << "\n" << std::endl;
    std::cout << "Cost time: " << (endTime - startTime) << "ms\n" << std::endl;
    std::cout << "---------linear recursive  method--------------\n" << std::endl;
    startTime = clock();
    result = fib_linear_recursive_method(n, &prev);
    endTime = clock();
    std::cout << "Result: " << result << "\n" << std::endl;
    std::cout << "Cost time: " << (endTime - startTime) << "ms\n" << std::endl;
    std::cout << "---------recursive method--------------\n" << std::endl;
    startTime = clock();
    result = fib_recursive_method(n);
    endTime = clock();
    std::cout << "Result: " << result << "\n" << std::endl;
    std::cout << "Cost time: " << (endTime - startTime) << "ms\n" << std::endl;
}
