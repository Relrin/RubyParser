#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Класс: Поиск переменных в строке кода
"""
import re

class RubyVariables:
    
  def __init__(self,code,cnt):
      self._code  = code
      self._cnt   = cnt

  @property
  def findVariables(self):
        """ Возвращает имена переменных в виде словаря, указанного в строке self._code """
        dictionary={}
        flag=0
        # шаблон поиска
        pattern="^\s*(\w+)\s*="       # переменные объявленные через =, и обращения с ".метод"
        lst=re.findall(pattern,self._code)
        # записываем в список найденные строки
        for i in range(len(lst)):
            if len(lst[i])!=0:
                # обрезка ненужных частей кода
                string=lst[i]
                string=string.replace(" ","")
                string=string.replace("=","")
                # запись в словарь
                dictionary[self._cnt]=string
                self._cnt+=1
        return dictionary