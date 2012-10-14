#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Класс: Поиск в коде объявленных классов
"""

class RubyClasses:
  
  def __init__(self,code,cnt):
      self._code  = code + '\n'
      self._cnt   = cnt
      
  @property
  def classDefine(self):
      """ Возвращает имена классов в виде словаря, указанного в строке self._code """
      dictionary={}
      flag=0
      string=""
      # разбор имени класса
      index=self._code.find("class")
      indexSharp=self._code.find("#")
      if index!=-1 and (indexSharp==-1 or indexSharp>index):
          for i in range(len(self._code)):
              if((self._code[i].isalpha() or self._code[i].isdecimal() or self._code[i]=="_")):
                string+=str(self._code[i])
              # если встретили символ '<', значит у нас есть родительский класс
              if self._code[i]=='<':
                flag=1
                break
          fixed_str=string.replace("class","")
          dictionary[self._cnt]=fixed_str
          self._cnt+=1
          # выщемливаем родителей данного класса, если есть
          if(flag==1):
              index=self._code.find("<")
              fixed_str=str(self._code[index+1:])
              fixed_str=fixed_str.replace(" ","")
              fixed_str=fixed_str.replace("\n","")
              dictionary[self._cnt]=fixed_str
              self._cnt+=1
      return dictionary

