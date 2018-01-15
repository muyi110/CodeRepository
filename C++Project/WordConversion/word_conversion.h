#ifndef WORD_CONVERSION_H
#define WORD_CONVERSION_H

#include <fstream>
#include <map>
#include <string>
#include <sstream>
#include <stdexcept>
using namespace std;
//单词转换管理函数声明
void word_transform(ifstream &map_file, ifstream &input);
//单词转换规则建立函数声明
map<string, string> buildMap(ifstream &map_file);
//单词转换执行函数声明
const string &transform(const string &s, const map<string, string> &m);

#endif
