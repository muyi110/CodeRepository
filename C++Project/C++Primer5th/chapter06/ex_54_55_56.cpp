#include <iostream>
#include <vector>

inline int f(const int, const int);
typedef decltype(f) fp;

inline int numAdd(const int n1, const int n2){return n1 + n2;}
inline int numSub(const int n1, const int n2){return n1 - n2;}
inline int numMul(const int n1, const int n2){return n1 * n2;}
inline int numDiv(const int n1, const int n2){return n1 / n2;}

int main(int argc, char *argv[]){
    std::vector<fp *> pvec{numAdd, numSub, numMul, numDiv};
    for(auto f : pvec){
        std::cout << f(2, 2) << std::endl;
    }
    return 0;
}
