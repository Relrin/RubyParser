#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Класс: Поиск операторов в строке кода
"""

class RubySeparators:
    
  def __init__(self,code,cnt,flag):
      self._code  = code
      self._cnt   = cnt
      self._flag  = flag

  @property
  def findSeparators(self):
        """ Возвращает операторы в виде словаря, указанного в строке self._code """
        dictionary={}
        # шаблон поиска
        pattern=[" ",",",";","/"]
        
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
            for i in pattern:
                block=self._code[:]
                cntOp=block.count(i)
                # кавычки (одинарные и двойные имеют один и тот же смысл)
                quote=[];
                for j in range(len(block)):
                    if block[j]=="\'" or block[j]=="\"": quote.append(j)
                # проходим по строке, пока не выделим нужные операторы
                while(cntOp!=0):
                    NeedWrite=False
                    index=block.find(i)
                    indexSharp=self._code.find('#')
                    if index!=-1 and (indexSharp==-1 or indexSharp>index):
                        # Анализ строки.
                        # Шаг 1: проверим чтобы оператор не был в строке/кавычках
                        # считаем сколько кавычек до оператора
                        quotesCnt=0
                        for j in quote:
                            if j<index:
                                quotesCnt+=1
                        # затем рассматриваем как идет оператор с кавычками
                        if quotesCnt==0 or quotesCnt%2==0: NeedWrite=True # до/после кавычек
                        if quotesCnt%2==1: NeedWrite=False                # в кавычках
                        # Шаг 2: запись в словарь
                        if NeedWrite:      
                            dictionary[self._cnt]=i
                            self._cnt+=1
                        # Шаг 3: корректировка входных данных
                        # делаем срез, удаляя найденные элементы
                        block=block[:index]+block[index:]
                        # корректируем список с индексами
                        tmp=[]
                        for j in quote:
                            tmp.append(j-len(i))
                        quote=tmp
                    cntOp-=1    
        return dictionary
    
if __name__ == '__main__':
    string="bar.add('cascade', 'menu'; menu,'label=' hello)"
    obj=RubySeparators(string,0,0)
    print(obj.findSeparators)
    