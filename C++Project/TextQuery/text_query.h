#ifndef TEXT_QUERY_H
#define TEXT_QUERY_H
#include <vector>
#include <string>
#include <memory>
#include <map>
#include <set>
#include <fstream>
#include <sstream>
#include <iostream>
using namespace std;
class QueryResult;//为了定义query函数的返回类型，需要先声明
using line_no = vector<string>::size_type; //类型别名，用来表示行号类型
/*************************************************************************/
/*
此类是文本查询类，定义此类的目的是提供一个抽象的解决方案
有两个数据成员：指向vector的shared_ptr：保存输入的文件
                map: 将每个单词关联到动态分配的set上
一个成员函数query：接受一个string返回一个QueryResult结果
*/
/*************************************************************************/
class TextQuery
{
public:
    TextQuery(ifstream &);
    QueryResult query(const string &) const;
private:
    shared_ptr<vector<string>> file;
    map<string, shared_ptr<set<line_no>>> wm;
};
/*************************************************************************/
/*
此类保存查询的结果，利用shared_ptr和TextQuery类共享数据
有三个数据成员：string: 保存查询的单词
                指向set的shared_ptr：指向保存单词出现行号的set
		指向vector的shared_ptr：指向保存输入文件的vector
一个成员函数是构造函数，用来初始化数据成员
*/
/*************************************************************************/
class QueryResult
{
friend ostream & print(ostream &, const QueryResult &);
public:
    QueryResult(string s, shared_ptr<set<line_no>> p, shared_ptr<vector<string>> f): sought(s), lines(p), file(f){}
private:
    string sought;
    shared_ptr<set<line_no>> lines;
    shared_ptr<vector<string>> file;
};
string make_plural(size_t ctr, const string &, const string &);
void runQueries(ifstream &);
#endif
