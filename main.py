#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__  = "Relrin & IGP"
__version__ = "0.0.1.0"
__credits__ = "Анализ кода Ruby"

def WriteAtConsole(comments,libraries,class_var,functions,variables,global_var,operators,separator):
    """
        Вывод содержимого переменных в консоль
        Входные данные:
            comments  - количество комментариев в коде
            libraries - словарь с подключенными библиотеками
            class_var - словарь с реализованными классами
            functions - словарь с реализованными функциями и методами класса
            variables - словарь с описанными переменными в коде
            operators - словарь с встречающимися в коде операторами
            separator - словарь с разделителями в коде
    """
    if comments!=0: print("Комментариев в файле: %d"%(comments))
    if len(libraries)!=0:
        print("Подключенные библиотеки: \n\t",end='')
        for key in libraries.keys():
            print(libraries[key],end="\n\t ")
    if len(class_var)!=0:
        print("\nЗадействованные классы: \n\t",end='')
        for key in class_var.keys():
            print(class_var[key][0]," использовался ",class_var[key][1]," раз(а)",end='\n\t')
    if len(functions)!=0:
        print("\nОписанные функции/процедуры/методы класса: ",end='\n\t')
        for key in functions.keys():
            print(functions[key][0]," использовался ",functions[key][1]," раз(а)",end='\n\t')
    if len(variables)!=0:
        print("\nЗайдествованные переменные в коде: \n\t",end='\n\t')
        for key in variables.keys():
            print(variables[key][0]," использовался ",variables[key][1]," раз(а)",end='\n\t')
    if len(global_var)!=0:
        print("\nКлассовые переменные в коде: \n\t",end='\n\t')
        for key in global_var.keys():  
            print(global_var[key][0]," использовался ",global_var[key][1]," раз(а)",end='\n\t')    
    if len(operators)!=0:
        print("\nНайденные операторы в коде: \n\t",end='\n\t')
        for key in operators.keys():
            print(operators[key][0]," встречался ",operators[key][1]," раз(а)",end='\n\t')
    if len(separator)!=0:
        print("\nНайденные разделители в коде: \n\t",end='\n\t')
        for key in separator.keys():
            print("\"",separator[key][0],"\""," встречался ",separator[key][1]," раз(а)",end='\n\t') 

def WriteAtFile(path,comments,libraries,class_var,functions,variables,global_var,operators,separator):
    """
        Вывод содержимого переменных в файл
        Входные данные:
            path      - путь к файлу, в который происходит запись
            comments  - количество комментариев в коде
            libraries - словарь с подключенными библиотеками
            class_var - словарь с реализованными классами
            functions - словарь с реализованными функциями и методами класса
            variables - словарь с описанными переменными в коде
            operators - словарь с встречающимися в коде операторами
            separator - словарь с разделителями в коде
    """
    file = open(path, 'w+')
    file.write("Комментариев в файле: %d\n"%(comments))
    if len(libraries)!=0:
        file.write("Подключенные библиотеки: \n\t")
        for key in libraries.keys():
            file.write("%s\n\t "%(libraries[key]))
    if len(class_var)!=0:
        file.write("\nЗадействованные классы: \n\t")
        for key in class_var.keys():
            file.write("%s использовался %d раз(а)\n\t"%(class_var[key][0],class_var[key][1])) 
    if len(functions)!=0:
        file.write("\nОписанные функции/процедуры/методы класса: \n\t")
        for key in functions.keys():
            file.write("%s использовался %d раз(а)\n\t"%(functions[key][0],functions[key][1]))
    if len(variables)!=0:
        file.write("\nЗайдествованные переменные в коде: \n\t")
        for key in variables.keys():
            file.write("%s использовался %d раз(а)\n\t"%(variables[key][0],variables[key][1]))
    if len(global_var)!=0:
        file.write("\nКлассовые переменные в коде: \n\t")
        for key in global_var.keys():
            file.write("%s использовался %d раз(а)\n\t"%(global_var[key][0],global_var[key][1]))
    if len(operators)!=0:
        file.write("\nНайденные операторы в коде: \n\t")
        for key in operators.keys():
            file.write("%s встречался %d раз(а)\n\t"%(operators[key][0],operators[key][1]))
    if len(separator)!=0:
        file.write("\nНайденные разделители в коде: \n\t")
        for key in separator.keys():
            file.write("\"%s\" встречался %d раз(а)\n\t"%(separator[key][0],separator[key][1]))
    file.close()
    
def CorrectDict(buf):
    """
        Корректируем словарь до вида КЛЮЧ:["объект","кол-во повторов"] без повторов
        Входные данные:
            buf        - данные присланные от обработчиков строк в виде словаря
    """
    base={}
    ListInDict={}
    for key_b in buf.keys():
        cnt=0
        # считаем количество повторов
        for key in buf.keys():
            if buf[key_b]==buf[key]: cnt+=1
        # запись в словарь
        ListInDict[key_b]=[buf[key_b],cnt]
    
    keys=values=[]
    for key in buf.keys():
        temp={}
        if (key not in keys) and (ListInDict[key] not in values):
            temp[key]=ListInDict[key]
            base.update(temp)
            keys.append(key)
            values.append(ListInDict[key])
    return base

def GetRealDict(buf):
    """
        Корректируем словарь до вида {КЛЮЧ:["оператор",["список_операторов_предков"]]}, удаляя при этом повторы
        Входные данные:
            buf - неотсортированный словарь с данными
    """
    WithoutNumericKeys={}
    # берем ключ
    for key in buf.keys():
        lst_ancestry=[]
        # второй раз проходим, чтобы найти все вхождения ключа
        for key_s in buf.keys():
            # если нашли, то запишем в список все операторы, которые были связаны с ним
            if buf[key][0]==buf[key_s][0]:
                ancestrys=buf[key_s][1]
                # перебор всех операторов, связанные с "ключом"
                for op in ancestrys:
                    if op not in lst_ancestry:
                       if op!=" ":
                        op=op.replace(" ","")
                        lst_ancestry.append(op)
        WithoutNumericKeys[buf[key][0]]=lst_ancestry
    
    base={}
    # формируем словарь с номерами
    for key in WithoutNumericKeys.keys():
        lst=[]
        int_key=0
        # перевод ключа в число
        for index in range(len(key)):
            int_key+=ord(key[index])
        # перевод значений, в виде операторов, в значения
        for op in WithoutNumericKeys[key]:
            letter=0
            for j in range(len(op)):
                letter+=ord(op[j])
            lst.append(letter)
        base[int_key]=lst
    return WithoutNumericKeys,base

def BoundaryValuesFind(buf):
    """
        Корректируем словарь с данными и возвращает данные: кол-во вершин, абсолютную граничную сложность и граф 
        Входные данные:
            buf - неотсортированный словарь с данными
    """
    first=buf[1][0]
    last =buf[len(buf)][0]
    base,numeric_base=GetRealDict(buf)
    resultOperKeys,numeric_base=GetRealDict(buf)
    
    # перевод графа в ориентированный
    for key in base.keys():
        # если это начало графа
        if key==first:
           base[key]=[[" "],"s"]
        # если это конец графа
        elif key==last:
           lst=base[key]
           base[key]=[lst,"e"]
        # любая другая вершина
        else:
           lst=base[key]
           base[key]=[lst,"p"]
    
    Sa=len(base)
    v=len(base)
    # нахождение абсолютная граничной сложности программы
    for key in base.keys():
        # проверим, чтобы в списке вершин, приведших к key_1 не было пустых мест
        if base[key][0]!=[] and base[key][0]!=" ":
            # выбираем вершины, которые привели к оператору key_1
            for key_op in base[key][0]:
                lst_path=[]
                # осматриваем каждую из вершин, так, чтобы у него не менее 2ух выходных вершин
                # выберем вершину
                if key_op in base.keys():
                    lst_path.append(key_op)
                    lst=base[key_op][0]
                    # ищем подграфы с данной вершиной
                    while(lst!=[]):
                        operator=lst[0]
                        if operator in base.keys():
                            lst_path.append(operator)
                        lst.remove(operator)
                if len(lst_path)>=2: Write_Sa=True
                else: Write_Sa=False
                if Write_Sa: Sa+=len(lst_path)-1
    
    S0=1-((v-1)/Sa)
    # вывод в консоль
    print("\nМетрика граничных значений:")
    print("\tграничная сложность программы: ",S0)
    # шапка таблицы
    string_1="\t+"
    string_2="\t|to \ fr"
    for i in range(len(resultOperKeys)+1):
        string_1+="-------+"
    print(string_1)
    for i in base.keys():
        string_2+=("|%6s "%(i))
    string_2+="|"
    print(string_2)
    print(string_1)
    # заполнение таблицы по колонкам
    for key in resultOperKeys.keys():
        if key==first: string_2="\t|%4s st|"%(key)
        elif key==last: string_2="\t|%4s en|"%(key) 
        else: string_2="\t|%6s |"%(key)
        for j in resultOperKeys.keys():
            if j in resultOperKeys[key]:
                string_2+=" %4d  |"%(1)
            else: string_2+=" %4d  |"%(0)
        print(string_2)
        print(string_1)
        
    # вывод в файл
    file=open("review.txt","a")
    file.write("\n\nМетрика граничных значений:")
    file.write("\n\tточек пересечения: %.4f"%(S0))
    # шапка таблицы
    string_1="\n\t+"
    string_2="\n\t|to \ fr"
    for i in range(len(resultOperKeys)+1):
        string_1+="-------+"
    file.write("\t%s"%(string_1))
    for i in resultOperKeys.keys():
        string_2+="|%6s "%(i)
    string_2+="|"
    file.write(string_2)
    file.write(string_1)
    # заполнение таблицы по колонкам
    for key in resultOperKeys.keys():
        if key==first: string_2="\n\t|%4s st|"%(key)
        elif key==last: string_2="\n\t|%4s en|"%(key) 
        else: string_2="\n\t|%6s |"%(key)
        for j in resultOperKeys.keys():
            if j in resultOperKeys[key]:
                string_2+=" %4d  |"%(1)
            else: string_2+=" %4d  |"%(0)
        file.write(string_2)
        file.write(string_1)
    file.close()
    
    return v,Sa,base,first,last

def FindAll(buf,path):
    """
        Функция: поиск всех вхождений значений из словаря в тексте кода
        Входные данные:
            buf  - словарь с данными
            path - путь к файлу
    """
    import re
    
    cnt=1
    newDict={}
    file=open(path,"r")
    ignore="[^'*\"*.*\w*=*-*+*>*<*|*&*%*?*)*}*,*]"
    patternStdOp="[*-=%\/]"
    values=[]
    for key in buf.keys():
        file.seek(0)
        # учитываем элементы так, чтобы не совершать повторые запросы поиска
        if buf[key] not in values:
            values.append(buf[key])
            # шаблон поиска переменной в виде регульярного выражения
            pattern="^\s*(" +buf[key]+ ")\s*[.]*[=]*|" +ignore+ "\s*(" +patternStdOp+ "*" +buf[key]+ ")\s*"
            for line in file.readlines():
                #if line.find("#")
                lst=re.findall(pattern,line)
                for i in lst:
                    string=str(i)
                    if len(string)!=0:
                        # обрезка ненужных частей кода
                        string=string.replace(" ","");
                        string=string.replace(",","");
                        string=string.replace(";","");
                        string=string.replace("=","");
                        string=string.replace("-","");
                        string=string.replace("+","");
                        string=string.replace("*","");
                        string=string.replace("/","");
                        string=string.replace("%","");
                        string=string.replace("}","");
                        string=string.replace("{","");
                        string=string.replace("(","");
                        string=string.replace(")","");
                        string=string.replace("\'","");
                        string=string.replace(":","");
                        newDict[cnt]=string
                        cnt+=1
    file.close()
    return newDict
    
    
def Holsted(variables,global_var,operators,functions,separator):
    """
        Анализ кода метрикой Холстеда
        Входные данные:
            variables - словарь с описанными переменными в коде
            global_var- словарь с глобальными переменными в коде
            operators - словарь с встречающимися в коде операторами
            functions - словарь с реализованными функциями и методами класса
            separator - словарь с разделителями в коде
    """
    import math
    n1=n2=N1=N2=N=V=0
    
    # учет n1,n2
    n1=len(operators)+len(functions)+len(separator)
    n2=len(variables)+len(global_var)
    
    # учет N1
    for key in operators.keys():
        N1+=operators[key][1]
    for key in functions.keys():
        N1+=functions[key][1]
    for key in separator.keys():
        N1+=separator[key][1]
    # учет N2
    for key in variables.keys():
        N2+=variables[key][1]
    for key in global_var.keys():
        N2+=global_var[key][1]
    # считаем длину программы
    N=N1+N2
    # считаем объем программы
    V=N*math.log(N,2)
    
    # ДОРАБОТКА 1: теоретическая длины программы
    N_Len_Theory = n1*math.log(n1,2)+n2*math.log(n2,2)
    # ДОРАБОТКА 2: уровень качества программирования L(уровень программы)
    V_=(n1+n2)*math.log((n1+n2),2)
    L=V_/V;
    # ДОРАБОТКА 3,4: уровень программы без оценки теор. объема / интеллектуальное содержание
    L_=2*n2/(n1*N2)
    # ДОРАБОТКА 5: оценка необходимых интеллектуальных усилий по написанию программы
    E=N_Len_Theory*math.log(((n1+n2)/L),2)
    
    # вывод в консоль
    print("\nМетрика Холстеда: ")
    print("\t+------------------+----------+")
    print("\t| Уник. операторов | %9d|"%(n1))
    print("\t| Уник. операндов  | %9d|"%(n2))
    print("\t| Число операторов | %9d|"%(N1))
    print("\t| Число операндов  | %9d|"%(N2))
    print("\t+------------------+----------+")
    print("\t| Длина программы: | %9d|"%(N))
    print("\t| Объем программы: | %9d|"%(V))
    print("\t+------------------+----------+")
    print("\t| Теор. длина    : | %9d|"%(N_Len_Theory))
    print("\t| Уровень про-ы 1: | %9f|"%(L))
    print("\t| Уровень про-ы 2: | %9f|"%(L_))
    print("\t| I              : | %9d|"%(V_))
    print("\t| E              : | %9d|"%(E))
    print("\t+------------------+----------+")
    # вывод в файл
    file=open("review.txt","a")
    file.write("\nМетрика Холстеда:")
    file.write("\n\t+------------------+----------+")
    file.write("\n\t| Уник. операторов | %9d|"%(n1))
    file.write("\n\t| Уник. операндов  | %9d|"%(n2))
    file.write("\n\t| Число операторов | %9d|"%(N1))
    file.write("\n\t| Число операндов  | %9d|"%(N2))
    file.write("\n\t+------------------+----------+")
    file.write("\n\t| Длина программы: | %9d|"%(N))
    file.write("\n\t| Объем программы: | %9d|"%(V))
    file.write("\n\t+------------------+----------+")
    file.write("\n\t| Теор. длина    : | %9d|"%(N_Len_Theory))
    file.write("\n\t| Уровень про-ы 1: | %9f|"%(L))
    file.write("\n\t| Уровень про-ы 2: | %9f|"%(L_))
    file.write("\n\t| I              : | %9d|"%(V_))
    file.write("\n\t| E              : | %9d|"%(E))
    file.write("\n\t+------------------+----------+")
    file.close()    
    
def PointIntersectionMetrics(file_path):
    """
        Анализ кода метрикой "точек пересечения"
        Входные данные:
            file_path - путь к выходному файлу
    """
    from PointIntersection import PointIntersection
    
    file=open(file_path,"r")
    # найдем все последовательности операторов
    cnt=1
    buf={}
    after=" "
    flag=False
    file.seek(0)
    for line in file.readlines():
        string=line.replace('\n',' ')
        seqInRuby=PointIntersection(string,cnt,flag,after)
        #проверяем полученные данные
        buf.update(seqInRuby.findSequence)
        if seqInRuby._after!=[]:
            after=seqInRuby._after
        cnt=seqInRuby._cnt
        flag=seqInRuby._flag
    file.close()
    resultOperKeys,resultNumericKeys=GetRealDict(buf)
    del buf

    PointIntersection=0
    for key in resultNumericKeys.keys():
        if resultNumericKeys[key]!=[]:
            # выбираем первую вершину (а)
            a=key
            # выбираем вторую вершину (b)
            for op in resultNumericKeys[key]:
                b=op
                # выбираем третью вершину (p)
                if b in resultNumericKeys.keys():
                    if resultNumericKeys[b]!=[]:
                        p=b
                        # выбираем четвертую вершину (q)
                        for op_2 in resultNumericKeys[p]:
                            q=op_2
                        # анализируем на наличие точки пересечения
                        if min(a,b) < min(p,q) < max(a,b) & max(p,q) > max(a,b) | min(a,b) < max(p,q) < max(a,b) & min(p,q) < min(a,b):
                            PointIntersection+=1
                else: continue  
    
    # выведем данные в консоль
    print("\nМетрика точек пересечения: ")
    print("\tточек песечения:",PointIntersection)
    # шапка таблицы
    string_1="\t+"
    string_2="\t|     "
    for i in range(len(resultOperKeys)+1):
        string_1+="-----+"
    print(string_1)
    for i in resultOperKeys.keys():
        string_2+="|%4s "%(i)
    string_2+="|"
    print(string_2)
    print(string_1)
    # заполнение таблицы по колонкам
    for key in resultOperKeys.keys():
        string_2="\t|%4s |"%(key)
        for j in resultOperKeys.keys():
            if j in resultOperKeys[key]:
                string_2+=" %2d  |"%(1)
            else: string_2+=" %2d  |"%(0)
        print(string_2)
        print(string_1)

    # запишем данные в файл
    file=open("review.txt","a")
    file.write("\n\nМетрика точек пересечения:")
    file.write("\n\tточек пересечения: %d"%(PointIntersection))
    # шапка таблицы
    string_1="\n\t+"
    string_2="\n\t|     "
    for i in range(len(resultOperKeys)+1):
        string_1+="-----+"
    file.write("\t%s"%(string_1))
    for i in resultOperKeys.keys():
        string_2+="|%4s "%(i)
    string_2+="|"
    file.write(string_2)
    file.write(string_1)
    # заполнение таблицы по колонкам
    for key in resultOperKeys.keys():
        string_2="\n\t|%4s |"%(key)
        for j in resultOperKeys.keys():
            if j in resultOperKeys[key]:
                string_2+=" %2d  |"%(1)
            else: string_2+=" %2d  |"%(0)
        file.write(string_2)
        file.write(string_1)
    file.close()
    
def BoundaryValuesMetrics(file_path):
    """
        Анализ кода метрикой "граничных значений"
        Входные данные:
            file_path - путь к выходному файлу
    """
    from BoundaryValues import BoundaryValues

    file=open(file_path,"r")
    # найдем все последовательности операторов
    cnt=1
    buf={}
    after=" "
    flag=False
    file.seek(0)
    for line in file.readlines():
        string=line.replace('\n',' ')
        seqInRuby=BoundaryValues(string,cnt,flag,after)
        #проверяем полученные данные
        buf.update(seqInRuby.findSequence)
        if seqInRuby._after!=[]:
            after=seqInRuby._after
        cnt=seqInRuby._cnt
        flag=seqInRuby._flag
    file.close()
    BoundaryValuesFind(buf)
    del buf
    
def ParseByLines(file_path):
    """
        Чтение и анализ содержимого файла
        Входные данные:
            file_path - путь к файлу
    """
    # подключаем библиотеки
    from RubyComments   import RubyComments
    from RubyLibraries  import RubyLibraries
    from RubyClasses    import RubyClasses
    from RubyFunctions  import RubyFunctions
    from RubyVariables  import RubyVariables
    from RubyOperations import RubyOperations
    from RubySeparators import RubySeparators
    from RubyGlobalVariables import RubyGlobalVariables
    
    # словари с библиотеками, идентификатора, операторами и т.д.
    libraries={}
    operators={}
    variables={}
    global_var={}
    class_var={}
    functions={}
    separator={}
    comments =0
    
    file=open(file_path,"r")
    
    # 1. Поиск комментариев
    # однострочных типа "#"
    comInRuby=RubyComments(file.read())
    comments+=comInRuby.comment_lines_count;
    # многострочных типа =begin ... =end
    file.seek(0)
    cntLines=findBegin=0
    for line in file.readlines():
        string=line.replace('\n','')
        # начало многострочного коммента
        if string[0:6]=="=begin":
            findBegin=1
            comments+=1
        # конец многострочного коммента
        if string=="=end":
            findBegin=0
            comments+=1
        # если в блоке многострочного комментария
        if findBegin==1:
            if(('#' in string)==0):
                comments+=1;
    comments-=1

    # 2. Поиск подключенных библиотек
    cnt=1;
    file.seek(0)
    for line in file.readlines():
        string=line.replace('\n','')
        libInRuby=RubyLibraries(string,cnt)
        if libInRuby.library.keys!={}:
            libraries.update(libInRuby.library)
        cnt+=1
    del cnt
    
    # 3. Поиск классов
    cnt=1
    buf={}
    file.seek(0)
    for line in file.readlines():
        string=line.replace('\n','')
        clsInRuby=RubyClasses(string,cnt)
        if clsInRuby.classDefine!={}:
            buf.update(clsInRuby.classDefine)
            cnt=clsInRuby._cnt
    class_var=CorrectDict(buf)
    del buf
    del cnt
    
    # 4. Функции/методы классов
    cnt=1
    buf={}
    file.seek(0)
    for line in file.readlines():
        string=line.replace('\n','')
        fncInRuby=RubyFunctions(string,cnt)
        # если полученный словарь не пустой, то просмотрим его
        if fncInRuby.funcDefine!={}:
            buf.update(fncInRuby.funcDefine)
            cnt=fncInRuby._cnt
    functions=CorrectDict(buf)   
    del buf
    del cnt
    
    # 5. Переменные
    cnt=1
    buf={}
    file.seek(0)
    for line in file.readlines():
        string=line.replace('\n','')
        varInRuby=RubyVariables(string,cnt)
        # если полученный словарь не пустой, то просмотрим его
        if varInRuby.findVariables!={}:
            buf.update(varInRuby.findVariables)
            cnt=varInRuby._cnt
    buf=FindAll(buf,file_path)
    variables=CorrectDict(buf)  
    del buf
    del cnt
    
    # 6. Глобальные переменные
    cnt=1
    buf={}
    file.seek(0)
    for line in file.readlines():
        string=line.replace('\n','')
        glbInRuby=RubyGlobalVariables(string,cnt)
        # если полученный словарь не пустой, то просмотрим его
        if glbInRuby.findVariables!={}:
            buf.update(glbInRuby.findVariables)
            cnt=glbInRuby._cnt
    buf=FindAll(buf,file_path)
    global_var=CorrectDict(buf)  
    del buf
    del cnt
    
    # 7. Операторы
    cnt=1
    buf={}
    flag=False
    file.seek(0)
    for line in file.readlines():
        string=line.replace('\n','')
        opsInRuby=RubyOperations(string,cnt,flag)
        # если полученный словарь не пустой, то просмотрим его
        if opsInRuby.findOperators!={}:
            buf.update(opsInRuby.findOperators)
            cnt=opsInRuby._cnt
        flag=opsInRuby._flag
    operators=CorrectDict(buf)
    del buf
    del cnt
    
    # 8. Разделители
    cnt=1
    buf={}
    flag=False
    file.seek(0)
    for line in file.readlines():
        string=line.replace('\n','')
        sepInRuby=RubySeparators(string,cnt,flag)
        # если полученный словарь не пустой, то просмотрим его
        if sepInRuby.findSeparators!={}:
            buf.update(sepInRuby.findSeparators)
            cnt=sepInRuby._cnt
        flag=sepInRuby._flag
    separator=CorrectDict(buf)
    del buf
    del cnt
      
    file.close()
    
    # выводим данные и удаляем переменные
    WriteAtConsole(comments,libraries,class_var,functions,variables,global_var,operators,separator)      
    # вывод в файл
    WriteAtFile("review.txt",comments,libraries,class_var,functions,variables,global_var,operators,separator)
    
    # рассчет метрик
    Holsted(variables,global_var,operators,functions,separator)
    PointIntersectionMetrics(file_path)
    BoundaryValuesMetrics(file_path)
    
    # удаление объектов, связанных со своим классом
    del comInRuby
    del libInRuby
    del clsInRuby
    del fncInRuby
    del varInRuby
    del glbInRuby
    del opsInRuby
    del sepInRuby
    
if __name__ == '__main__':
    """
        Основная часть программы:
            - открывает исходные файлы с кодом на Ruby
            - анализирует файлы с кодом:
                а) метрикой Холстеда
                б) метрикой точек пересечения
                в) метрикой граничных значений
            - выводит результаты анализа в виде таблицы, в консоль
    """
    import os
    # чтение файлов из каталога
    #directory = "C:\\Code\\Python\\test\\"
    #files = os.listdir(directory);
    #for file in files:
    #    file=open(...)
    #    print(line,end='')
    #    ...
    #    file.close()
    
    ParseByLines("C:\\Code\\Python\\test\\test2.rb")
    