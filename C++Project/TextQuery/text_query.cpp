/**************************************************************************/
/*
此程序是一个文本查询程序，作为标准库内容学习的总结
程序功能：允许用户在给定的文件中查询单词，查询结果是单词在文件中出现的次数
          以及所在行的列表，如果一个单词在一行出现多次，此行只列出一次，行
	  会按照升序输出；
参考：C++Primer 中文5th，P430
作者：YangLiuqing
时间：2017-12-09
*/
/**************************************************************************/
#include "text_query.h"
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
/**************************************************************************/
/*
此函数用于打印结果
*/
/**************************************************************************/
ostream &print(ostream &os, const QueryResult &qr)
{
    os << qr.sought << "occurs " << qr.lines->size() << " " << make_plural(qr.lines->size(),"time", "s") << endl;
    for(auto num : *qr.lines)
    {
        os << "\t(line" << num + 1 << ")" << *(qr.file->begin() + num) << endl;
    }
    return os;
}
string make_plural(size_t ctr, const string &word, const string &ending)
{
    return (ctr > 1) ? word + ending : word;
}
/**************************************************************************/
/*
此函数用于运行程序目的，调用上述类；此函数在main函数中被调用
*/
/**************************************************************************/
void runQueries(ifstream &infile)
{
    TextQuery tq(infile);   //保存文件并建立查询map
    while(true)
    {
        cout << "enter word to look for,or 'q' to quit" << endl;
	string s;
        if(!(cin >> s) || s == "q") break;
	print(cout ,tq.query(s)) << endl;
    }
}
int main(int argc, char **argv)
{
    if(argc == 2)
    {
        ifstream infile(argv[1]);
        //ifstream infile;
	//infile.open(argv[1]);
        runQueries(infile);   
    }
    else
        cout << "please input the file" << endl;
    return 0;
}
