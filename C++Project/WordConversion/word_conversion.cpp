/************************************************************************/
/*
简介：此程序是单词转换程序，主要学习关联容器map的使用。程序的输入是两个
      文件，第一个文件保存转换规则，每条规则由两部分组成：一个可能出现
      在输入文件中单词和一个用来替换它的短语。第二个输入的文件是要转换的
      文本。
参考：C++Primer中文第5版P391；
作者：Yangliuqing
日期: 2017年12月5日
*/
/************************************************************************/
#include "word_conversion.h"
#include <iostream>
/***********************************************************************/
/*
                            主程序
*/
/***********************************************************************/
int main(int argc, char **argv)
{
    if(argc == 3)
    {
        ifstream map_file(argv[1]);
        ifstream input(argv[2]);
        word_transform(map_file, input);
    }
    else
        cout << "you must offer files." << endl;
    return 0;
}
/***********************************************************************/
/*
函数名：word_transform;
入口参数：map_file: 绑定的单词转换文件
          input: 绑定的要转换的文本
功能: 管理单词转换的整个过程
返回值: 无
*/
/***********************************************************************/
void word_transform(ifstream &map_file, ifstream &input)
{
    auto trans_map = buildMap(map_file);  //保存转换规则
    string text;
    while(getline(input, text))
    {
        istringstream stream(text);       //读取每个单词,输入字符流可以对
	                                  //string 进行读操作(>>)
	string word;
	bool firstword = true;            //控制是否打印空格
	while(stream >> word)
	{
	    if(firstword)  firstword = false;
	    else cout << " ";
	    cout << transform(word, trans_map);
	}
	cout << endl;
    }
}
/***********************************************************************/
/*
函数名：buildMap;
入口参数：map_file: 绑定的单词转换文件
          
功能: 建立单词转换映射
返回值: map<string, string>
*/
/***********************************************************************/
map<string, string> buildMap(ifstream &map_file)
{
    map<string, string> trans_map;       //保存转换规则
    string key;                          //要转换的单词（关键字）
    string value;                        //替换后的内容
    //读取第一个单词存放在key中，行中剩余的存在value中
    while(map_file >> key && getline(map_file, value))
    {
        if(value.size() > 1)             //检查是否有转换规则
	{
	    trans_map[key] = value.substr(1);   //跳过前面的一个空格
	}
	else
	{
	    throw runtime_error("no rule for " + key);
	}
    }
    return trans_map;
}
/***********************************************************************/
/*
函数名：transform;
入口参数：s: 需要转换的string
          m: 构建的转换规则map<string, string>
功能: 单词转换执行
返回值: const string&
*/
/***********************************************************************/
const string & transform(const string &s, const map<string, string> &m)
{
    //实际的转换工作，此部分是核心程序
    auto map_it = m.find(s);
    if(map_it != m.cend())
    {
        return map_it->second;
    }
    else
    {
        return s;
    }
}
