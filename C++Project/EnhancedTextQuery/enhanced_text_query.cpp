/**************************************************************************/
/*
此程序是一个高级文本查询程序，作为抽象数据（15章）内容学习的总结
程序功能：允许用户在给定的文件中查询单词，查询结果是单词在文件中出现的次数
          以及所在行的列表，如果一个单词在一行出现多次，此行只列出一次，行
	  会按照升序输出；查询方式可以是：单文本，与或非查询（例如：set,
          或is & not |set等方式查询。
参考：C++Primer 中文5th，15章最后例子
作者：YangLiuqing
时间：2018-1-8
*/
/**************************************************************************/
#include "enhanced_text_query.h"
#include <fstream>
#include <sstream>
#include <algorithm>
/**************************************************************************/
/*
TextQuery类的构造函数，逐行读取输入文件，并建立单词到行号的映射
*/
/**************************************************************************/
TextQuery::TextQuery(ifstream &is):file(new vector<string>)
{
    string text;
    while(getline(is, text))   //读取文件中的每一行
    {
        file->push_back(text); //保存此行文本到vector中
	int n = file->size() - 1; //当前的行号
	istringstream line(text); //当前行转为字符流，便于文本分解
	string word;
	while(line >> word)       //提取行中的每个单词
	{
	    auto &lines = wm[word]; //若word不在wm中，以此下标添加一项
	//map的下标操作返回mapped_type类型（关键字关联的类型），接引用一个map
        //迭代器，返回value_type类型，此例中lines是shared_ptr类型
	    if(!lines)
	    {
	        lines.reset(new set<line_no>); //分配一个新的set
	    }
	    lines->insert(n);                  //将此行号插入到set中
	}
    }
}
QueryResult TextQuery::query(const string &sought) const
{
    //如果未找到sought,返回一个此set，空的行号
    static shared_ptr<set<line_no>> nodata(new set<line_no>);
    //使用find而不是下表查找单词，避免将新单词插入
    auto loc = wm.find(sought);
    if(loc == wm.end())
    {
        return QueryResult(sought, nodata, file); //未找到
    }
    else
        return QueryResult(sought, loc->second, file);
}
/*************************************************************************/
/*
   接收string的Query类构造函数
*/
/*************************************************************************/
inline Query::Query(const std::string &s): q(new WordQuery(s)){ }
/*************************************************************************/
/*
    重载取反运算符(~)
*/
/*************************************************************************/
inline Query operator ~(const Query &operand)
{
    return std::shared_ptr<Query_base>(new NotQuery(operand));
}
/*************************************************************************/
/*
    重载运算符与(&)
*/
/*************************************************************************/
inline Query operator &(const Query &lhs, const Query &rhs)
{
    return std::shared_ptr<Query_base>(new AndQuery(lhs, rhs));
}
/*************************************************************************/
/*
    重载运算符或(|)
*/
/*************************************************************************/
inline Query operator |(const Query &lhs, const Query &rhs)
{
    return std::shared_ptr<Query_base>(new OrQuery(lhs, rhs));
}
/*************************************************************************/
/*
    或对象(OrQuery)的eval函数定义
*/
/*************************************************************************/
QueryResult OrQuery::eval(const TextQuery &text) const
{
    auto right = rhs.eval(text), left = lhs.eval(text);
    //将左侧运算对象的行号拷贝到set中
    auto ret_lines = make_shared<set<line_no>>(left.begin(), left.end());
    //插入右侧运算对象所得行号
    ret_lines->insert(right.begin(), right.end());
    //返回新的QueryResult，表示lhs与rhs的并集
    return QueryResult(rep(), ret_lines, left.get_file());
}
/*************************************************************************/
/*
    与对象(AndQuery)的eval函数定义
*/
/*************************************************************************/
QueryResult AndQuery::eval(const TextQuery &text) const
{
    auto left = lhs.eval(text), right = rhs.eval(text);
    //保存left与right交集的set
    auto ret_lines = make_shared<set<line_no>>();
    //将两个范围交集写入目的迭代器
    set_intersection(left.begin(), left.end(), right.begin(), right.end(),
                     inserter(*ret_lines, ret_lines->begin()));
    return QueryResult(rep(), ret_lines, left.get_file());
}
/*************************************************************************/
/*
    取反(非)对象(NotQuery)的eval函数定义
*/
/*************************************************************************/
QueryResult NotQuery::eval(const TextQuery &text) const
{
    auto result = query.eval(text);
    //开始时结果set为空
    auto ret_lines = make_shared<set<line_no>>();
    auto beg = result.begin(), end = result.end();
    //对于输入中的每一行，如果该行不在result中，则将其添加到ret_lines
    auto sz = result.get_file()->size();
    for(size_t n = 0; n != sz; ++n)
    {
        if(beg == end || *beg != n)
	{
	    ret_lines->insert(n);
	}
	else if(beg != end)
	    ++beg;
    }
    return QueryResult(rep(), ret_lines, result.get_file());
}
/**************************************************************************/
/*
    此函数用于打印结果
*/
/**************************************************************************/
ostream &print(ostream &os, const QueryResult &qr)
{
    os << qr.sought << " occurs " << qr.lines->size() << " " << make_plural(qr.lines->size(),"time", "s") << endl;
    for(auto num : *qr.lines)
    {
        os << "\t(line " << num + 1 << ")" << *(qr.file->begin() + num) << endl;
    }
    return os;
}
string make_plural(size_t ctr, const string &word, const string &ending)
{
    return (ctr > 1) ? word + ending : word;
}
/*************************************************************************/
/*
    主函数main()
*/
/*************************************************************************/
int main(int argc, char **argv)
{
    if(argc == 2)
    {
        ifstream file(argv[1]);
        TextQuery tq(file);
	while(true)
	{
	    cout << "enter word to look for,or 'q' to quit" << endl;
	    string s;
	    if(!getline(cin, s) || s == "q") break;
	    istringstream line(s);
	    string word;
	    Query q;
	    while(line >> word)
	    {
	        if(word == "~")
                {
		    line >> word;
		    q = ~Query(word);
                }
		else if(word == "|")
		{
		    line >> word;
		    q = q | Query(word);
                }
		else if(word == "&")
		{
		    line >> word;
		    q = q & Query(word);
                }
		else
		    q = Query(word);
	    }
	    print(cout, q.eval(tq)) << endl;
	}
    }
    else
        cout << "Please input the file queried!" << endl;
    return 0;
}
