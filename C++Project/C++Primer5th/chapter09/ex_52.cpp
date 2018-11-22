#include <iostream>
#include <stack>
#include <string>

int main(int argc, char *argv[]){
    std::string expression("This is (pezy)!");
    bool bSeen = false;
    std::stack<char> charStack;

    for(const auto &s : expression){
        if(s == '('){
            bSeen = true;
            continue;
        }
        else if(s == ')') {
            bSeen = false;
        }
        if(bSeen)
            charStack.push(s);
    }
    std::string repstr;
    while(!charStack.empty()){
        // repstr.append(charStack.top());
        repstr += charStack.top();
        charStack.pop();
    }
    expression.replace(expression.find("(")+1, repstr.size(), repstr);
    std::cout << expression << std::endl;
    return 0;
}
