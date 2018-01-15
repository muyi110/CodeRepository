#ifndef ENHANCED_TEXT_QUERY_H
#define ENHANCED_TEXT_QUERY_H
#include <string>
#include <memory>
#include <iostream>
#include <map>
#include <set>
#include <vector>
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
    using resultIter = set<line_no>::iterator;
    QueryResult(string s, shared_ptr<set<line_no>> p, shared_ptr<vector<string>> f): sought(s), lines(p), file(f){}
    auto begin() const -> resultIter { return lines->begin(); }
    auto end() const -> resultIter { return lines->end(); }
    auto get_file() const -> shared_ptr<vector<string>> { return file; }
private:
    string sought;
    shared_ptr<set<line_no>> lines;
    shared_ptr<vector<string>> file;
};
/*************************************************************************/
/*
    这是一个抽象基类，具体的查询类型从中派生，所有成员都是private的
*/
/*************************************************************************/
class Query_base
{
    friend class Query;
protected:
    //using line_no = TextQuery::line_no;  //用于eval函数
    virtual ~Query_base() = default;
private:
    virtual QueryResult eval(const TextQuery &) const = 0;
    virtual std::string rep() const = 0;
};
/*************************************************************************/
/*
    这是一个管理Query_base继承体系的接口类
*/
/*************************************************************************/
class Query
{
    //这些运算符需要访问接收shared_ptr的构造函数，而改构造函数是私有的
    friend Query operator ~(const Query &);
    friend Query operator |(const Query &, const Query &);
    friend Query operator &(const Query &, const Query &);
public:
    Query(const std::string &);
    Query() = default;
    //接口函数：调用对应的Query_base操作
    QueryResult eval(const TextQuery &t) const { return q->eval(t); }
    std::string rep() const { return q->rep(); }
private:
    Query(std::shared_ptr<Query_base> query):q(query) { }
    std::shared_ptr<Query_base> q;
};
/*************************************************************************/
/*
    Query的输出运算符重载
*/
/*************************************************************************/
std::ostream & operator <<(std::ostream &os, const Query &query)
{
    //Query::rep()通过它的Query_base指针对rep()进行虚调用
    return os << query.rep();
}
/*************************************************************************/
/*
    派生类，WordQuery类：查找一个给定的string，是在给定的TextQuery对象上
                         执行查询的唯一一个操作
*/
/*************************************************************************/
class WordQuery : public Query_base
{
    friend class Query;
    WordQuery(const std::string &s): query_word(s) { }
    QueryResult eval(const TextQuery &t) const { 
                     return t.query(query_word); }
    std::string rep() const { return query_word; }
    std::string query_word;    //查找的单词
};
/*************************************************************************/
/*
    派生类，NotQuery类
*/
/*************************************************************************/
class NotQuery: public Query_base
{
    friend Query operator ~(const Query &);
    NotQuery(const Query &q): query(q) { }
    std::string rep() const { return "~(" + query.rep() + ")"; }
    QueryResult eval(const TextQuery &) const;
    Query query;
};
/*************************************************************************/
/*
    抽象基类BinaryQuery，保存操作两个运算对象的查询类型所需要数据
*/
/*************************************************************************/
class BinaryQuery: public Query_base
{
protected:
    BinaryQuery(const Query &l, const Query &r, std::string s): lhs(l),
             rhs(r), opSym(s) { }
    //抽象类：BinaryQuery不定义eval
    std::string rep() const 
    {
        return "(" + lhs.rep() + " " + opSym + " " + rhs.rep() + ")";
    }
    Query lhs, rhs;    //左侧和右侧运算对象
    std::string opSym; //运算符的名字
};
/*************************************************************************/
/*
    派生类，AndQuery类
*/
/*************************************************************************/
class AndQuery: public BinaryQuery
{
    friend Query operator &(const Query &, const Query &);
    AndQuery(const Query &left, const Query &right): 
            BinaryQuery(left, right, "&") { } 
    QueryResult eval(const TextQuery &) const;
};
/*************************************************************************/
/*
    派生类，OrQuery类
*/
/*************************************************************************/
class OrQuery: public BinaryQuery
{
    friend Query operator |(const Query &, const Query &);
    OrQuery(const Query &left, const Query &right):
           BinaryQuery(left, right, "|") { } 
    QueryResult eval(const TextQuery &) const;
};
string make_plural(size_t ctr, const string &, const string &);
#endif
