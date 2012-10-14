#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Класс: Поиск в коде однострочных комментариев вида '#' и многострочных  вида '=begin ... =end'
"""
import re

class RubyComments:
    
    def __init__(self,code):
        self._code  = code + '\n'
        self._lines = set()
    
    @property
    def comment_lines_count(self):
        """ Возвращает количество строк с '#' в self._code """
        # преобразуем результат соответствия регулярного выражения в множество позиций символов
        match_to_set = lambda m: set(range(*m.span()))
        # возвращаем итератор соответствий регулярного выражения в self._code
        re_iter      = lambda expr: re.finditer(expr, self._code)
        code = list(enumerate(match_to_set(m) for m in re_iter('.*\n')))
        for m in re_iter('#(.*\\\s*\n)+.*\n|#.*\n|/\*(\n|.)*?\*/'):
            self._lines |= set(s[0] for s in code if match_to_set(m) & s[1])
        return len(self._lines)
