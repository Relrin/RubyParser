#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Класс: Поиск в коде объявленных методов в классе и функций в коде
"""

class RubyFunctions:
    
    def __init__(self,code,cnt):
        self._code = code
        self._cnt  = cnt
    
    @property
    def funcDefine(self):
        """ Возвращает определенные функции и процедуры, указанные в self._code """
        nameFunc={}
        index=self._code.find("def")
        if index!=-1:
            string=""
            for i in range(len(self._code)):
                if self._code[i]=="(":
                    break;
                if self._code[i].isalpha() or self._code[i].isdecimal() or self._code[i]=="_":
                    string+=str(self._code[i])
            fixed_str=string.replace("def","")
            fixed_str=fixed_str.replace(" ","")
            fixed_str=fixed_str.replace("\n","")
            nameFunc[self._cnt]=fixed_str
        else:
            # распарсивание методов класса и стандартных библиотек
            string=self._code[:]
            while(1):
                indexDot=string.find(".")
                indexBracketOpen=string.find("(")
                indexBracketClose=string.find(")")
                if (indexDot!=-1 and indexBracketOpen!=-1) or indexBracketOpen!=-1:
                    result=fixed_str=""
                    block=string[:indexBracketOpen]
                    for i in reversed(range(len(block))):
                        if block[i]=="." or block[i]==" ":
                            break
                        if block[i].isalpha() or block[i].isdecimal() or block[i]=="_":
                            result+=str(block[i])
                    string=string.replace(string[:indexBracketClose],"")
                    fixed_str=result.replace(".","")
                    fixed_str=fixed_str.replace(" ","")
                    fixed_str=fixed_str.replace("\n","")
                    nameFunc[self._cnt]=fixed_str[::-1]
                    self._cnt+=1
                else:
                    break
        return nameFunc
