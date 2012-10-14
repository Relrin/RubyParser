#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Класс анализа кода для метрики точек пересечения
"""
import re

class BoundaryValues:
    
  def __init__(self,code,cnt,flag,after_op):
      self._code  = code
      self._cnt   = cnt
      self._flag  = flag
      self._after = after_op

  @property
  def findSequence(self):
        """ Возвращает операторы в виде словаря, указанного в строке self._code """
        lst_ops=[]
        dictionary=dict_={}
        # шаблон поиска
        ignore =["=>"] 
        phrases=[".eql?","equal?","=>"]
        pattern=["**","==","+=","-=","*=","/=","**=","%=","===","!=",">=","<=","<=>",
                ".eql?","equal?",">>","<<","^","!","~","<",">","=","+","-","*","/","%"]
        patternCycle="(\s+not\s+)|(\s+and\s+)|(\s+or\s+)|(&&)|([|]+)"
        
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
        if indexSharp in [0,1,2,3,4]:
            return dictionary
        # поиск в строке операторов если нет разделителей в циклах и условиях
        else:
            lst=re.findall(patternCycle,self._code)
            for i in lst:
                if len(i)!=0:
                    for j in i:
                        # проверим, чтобы оператор, как результат поиск не являлся ""
                        if len(j)!=0:
                            string=j
                            string=string.replace(" ","")
                            string=string.replace("=","")
                            dictionary[self._cnt]=[string,self._after]
                            self._cnt+=1
                            lst_ops.append(j)
            # удаляем символы, которые не являются строками
            for i in ignore:
                while(self._code.find(i)!=-1):
                    index=self._code.find(i)
                    self._code=self._code[:index]+self._code[index+len(i):]
            # формирируем выходной словарь
            patterns=pattern
            while(patterns!=[]):
                # проициниализируем данные
                operator=patterns[0]
                # проверим, не является ли оператор набором букв и символом?
                if operator in phrases: PhraseInOp=True
                else: PhraseInOp=False
                block=self._code[:]
                cntOp=block.count(operator)
                if cntOp!=0:
                    lst_ops.append(operator)
                # запишем в список данные о кавычках, если они есть
                quote = [i for (i, c) in enumerate(block) if c in '\'"']
                # затем проанализируем операторы, находящиеся у нас в строке
                while(cntOp!=0):
                    NeedWrite=False
                    index=block.find(operator)
                    # считаем кавычки идущие после оператора
                    quotesCnt=0
                    for j in quote:
                        if j<index:
                            quotesCnt+=1
                    # затем рассматриваем как идет оператор с кавычками
                    if quotesCnt==0 or quotesCnt%2==0: NeedWrite=True # до/после кавычек
                    if quotesCnt%2==1: NeedWrite=False                # в кавычках
                    # ищем конец для строки с оператором
                    end=0;
                    string="";
                    if not PhraseInOp:
                        for i in range(index,len(block),1):
                            if(block[i].isalpha() or block[i].isdecimal() or block[i]=="_" or block[i]==" "):
                                end=i;
                                break;
                            else: string+=block[i]
                    if PhraseInOp:
                        for i in range(index,len(block),1):
                            if(block[i]=="_" or block[i]==" "):
                                end=i;
                                break;
                            else: string+=block[i]
                    # сравниваем полученные строки
                    if operator!=string: NeedWrite=False
                    # вырезаем этот символ из исходной строки
                    block=block[:index]+block[end:]
                    self._code=block
                    # запись данных в словарь
                    if NeedWrite:
                        dictionary[self._cnt]=[operator,self._after]
                        self._cnt+=1
                    # корректируем список с индексами кавычек
                    tmp=[]
                    for j in quote:
                        tmp.append(j-len(string))
                    quote=tmp
                    cntOp-=1
                patterns.remove(operator)
            # формируем список предыдущий операторов в строке
        self._after=lst_ops
        return dictionary


    