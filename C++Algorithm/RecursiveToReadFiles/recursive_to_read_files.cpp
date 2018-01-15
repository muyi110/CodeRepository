/*********************************************************************************************/
/*
此程序目的：通过递归调用算法，实现读取文件（文件可能嵌套）；模拟实现#include file功能
Author: YangLiuqing
Date: 2017-12-21
*/
/*********************************************************************************************/
#include <iostream>
#include <fstream>
#include <set>
#include <string>
#include <sstream>

using namespace std;
void ProcessFile(const char *FileName);

set<string> fileNameSet; //此容器保存文件名字
void ProcessFile(const char *FileName)
{
    ifstream input(FileName);
    if(!input)
    {
        cerr << "error: ubable to open input file: " << FileName << endl;
	return;
    }
    fileNameSet.emplace(FileName); //将文件名插入到容器中
    cout << FileName << endl;
    string text;
    while(getline(input, text))
    {
        istringstream stream(text);
	string word;
	bool firstword = true;     //控制是否打印空格
	while(stream >> word)
	{
	    if(word == "#include")
	    {
	        if(stream >> word)   //获取include包含的文件名
		{
		    if(fileNameSet.count(word) == 0)
	 	    {
		        ProcessFile(word.c_str());   //递归调用(核心）
		    }
		    else
		    {
		        cerr << "Self-referential includes is detected: " << word << endl;
                        return;
		    }
		}
		else
		{
		    cerr << "there is no file behind the #include." << endl;
		    return;
		}
	    }
	    else
	    {    
	        if(firstword) firstword = false;
	        else cout << " ";
		cout << word;
            }
	}
        cout << endl; //在每次递归调用会被执行两次
    }
    input.close();
}

int main(int argc, char **argv)
{
    if(argc != 2)
    {
        cout << "Input the file to read." << endl;
	return 0;
    }
    ProcessFile(argv[1]);
    return 0;
}
