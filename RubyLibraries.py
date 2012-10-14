#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Класс: Поиск в коде подключенных библиотек
"""
class RubyLibraries:
    
    def __init__(self,code,cnt):
        self._code = code
        self._cnt  = cnt
        
    @property
    def library(self):
        """ Возвращает подключенные библиотеки, указанные в self._code, в виде словаря """
        dictionary={}
        cntSign=canParse=0;
        string=""
        # находя вхождение, записываем данные в словарь
        index=self._code.find("require")
        indexSharp=self._code.find("#")
        if index!=-1 and (indexSharp==-1 or indexSharp>index):
            block=self._code[index:]
            for i in range(len(block)):
                if((self._code[i]=='\'' or self._code[i]=='\"') and cntSign!=2):
                    canParse=1
                    cntSign+=1
                    continue
                if cntSign==2:
                    break
                if((self._code[i].isalpha() or self._code[i].isdecimal() or self._code[i]=="_" or self._code[i]==".") and canParse==1):
                    string+=str(self._code[i])
                # файлы библиотек, разделенные '/' как правило указывают на использование *.so файлов
                # которые не могут быть проанализированы
                if self._code[i]=='/':
                    return {}
            fixed_str=string.replace(".rb","")
            dictionary[self._cnt]=fixed_str
        # и затем запишем все в словарь
        return dictionary
