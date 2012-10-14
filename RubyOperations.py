#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Класс: Поиск разделителей в строке кода
"""
import re

class RubyOperations:
    
  def __init__(self,code,cnt,flag):
      self._code  = code
      self._cnt   = cnt
      self._flag  = flag

  @property
  def findOperators(self):
        """ Возвращает операторы в виде словаря, указанного в строке self._code """
        dictionary={}
        # шаблон поиска
        ignore =["=>"] 
        phrases=[".eql?","equal?","=>"]
        pattern=["===","**","==","+=","-=","*=","/=","**=","%=","!=",">=","<=","<=>",
                ".eql?","equal?","||","&&",">>","<<","^","!","~","<",">","=","+","-","*","/","%"]
        patternCycle="(\s+not\s+)|(\s+and\s+)|(\s+or\s+)|(&&)|([|]+)|(\s*>\s*)"
        # смотрим, чтобы это не был многострочный комментарий
        if self._code.find("=begin")==0:
            self._flag=True
            return dictionary
        # если многострочный комментарий окончился, снимаем флаг и делаем срез
        if self._code.find("=end")==0 and self._flag:
            self._flag=False
            self._code=self._code[4:]
        # если однострочный и с начала строки - игноррируем ее
        indexSharp=self._code.find('#')
        if indexSharp==0:
            return dictionary
        else:
            # удаляем символы, которые не являются строками
            for i in ignore:
                while(self._code.find(i)!=-1):
                    index=self._code.find(i)
                    self._code=self._code[:index]+self._code[index+len(i):]
            # поиск логических операторов
            lst=re.findall(patternCycle,self._code)
            for i in lst:
                if len(i)!=0:
                    for j in i:
                        # проверим, чтобы оператор, как результат поиск не являлся ""
                        if len(j)!=0:
                            string=j
                            string=string.replace(" ","")
                            string=string.replace("=","")
                            dictionary[self._cnt]=string
                            self._cnt+=1
            # поиск любых других операторов
            for i in pattern:
                block=self._code[:]
                cntOp=block.count(i)
                # кавычки (одинарные и двойные имеют один и тот же смысл)
                quote = [i for (i, c) in enumerate(block) if c in '\'"']
                # проходим по строке, пока не выделим нужные операторы
                while(cntOp!=0):
                    NeedWrite=False
                    index=block.find(i)
                    # Анализ строки
                    # Шаг 1: проверим чтобы оператор не был в строке/кавычках
                    # считаем сколько кавычек до оператора
                    quotesCnt=0
                    for j in quote:
                        if j<index:
                            quotesCnt+=1
                    # затем рассматриваем как идет оператор с кавычками
                    if quotesCnt==0 or quotesCnt%2==0: NeedWrite=True # до/после кавычек
                    if quotesCnt%2==1: NeedWrite=False                # в кавычках
                    # Шаг 2: вырезаем из текста оператор, если соотв. условиям выборки
                    string=""
                    start=end=0
                    findOp=afterWord=False
                    for j in range(len(block)):
                        if block[j] in pattern:
                            if findOp==False:
                                findOp=afterWord=True
                                start=j
                            string+=block[j]
                        if (block[j].isalpha() or block[j].isdecimal() or block[j]=="_" or block[j]==" ") and afterWord:
                            end=j
                            break
                    if findOp:
                        if i!=string: NeedWrite=False
                    # Шаг 3: запись в словарь
                    if NeedWrite:      
                        dictionary[self._cnt]=i
                        self._cnt+=1
                    # Шаг 4: корректировка входных данных
                    # делаем срез, удаляя найденные элементы
                    block=block[:start]+block[end:]
                    # корректируем список с индексами
                    tmp=[]
                    for j in quote:
                        tmp.append(j-len(string))
                    quote=tmp
                    cntOp-=1
        return dictionary
    
if __name__ == '__main__':
    string="bar.add('cascade', ** 'menu' => += menu,'label=' === => hello)"
    obj=RubyOperations(string,0,0)
    print(obj.findOperators)
    