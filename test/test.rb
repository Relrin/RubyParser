#!/usr/bin/env ruby
#require "rubygems"
#require "active_record"
#require 'active_support'
require 'tk' # импортируем библиотеку
#require 'mathn'

app = TkRoot.new { # создаём окно
     title "Hello Tk!"; padx 50; pady 15 # с нужными нам свойствами
}

lbl = TkLabel.new(app) { # создаём надпись
     text "Something wasn't clicked yet..." # с таким вот текстом
     pack { padx 100; pady 100; side "left" } # с такими координатами
}
java_clicked = Proc.new { # ловим клик "Java" в меню
     lbl.text "Java was liked..."
}
sc_clicked = Proc.new { # ловим клик "Scala" в меню
     lbl.text "Scala was liked..."
}
cpp_clicked = Proc.new { # ловим клик "C" в меню
     lbl.text "C was liked..."
}
py_clicked = Proc.new { # ловим клик "Python" в меню
     lbl.text "Python was liked..."
}
rb_clicked = Proc.new { # ловим клик "Ruby" в меню
     lbl.text "Ruby was liked..."
}
=begin
=end
menu = TkMenu.new(app)# создаём меню 
menu.add('command', 'label' => "Java", 'command' => java_clicked) # создаём кнопку "Java"
menu.add('command', 'label' => "Scala", 'command' => sc_clicked) # создаём кнопку "Scala"
menu.add('separator') # создаём разделитель
menu.add('command', 'label' => "C", 'command' => cpp_clicked) # создаём кнопку "C"
menu.add('separator') # создаём разделитель
menu.add('command', 'label' => "Python", 'command' => py_clicked) # создаём кнопку "Python"
menu.add('command', 'label' => "Ruby", 'command' => rb_clicked) # создаём кнопку "Ruby"
bar = TkMenu.new # создаём бар для нашего меню
bar.add('cascade', 'menu' => menu, 'label' => "Click me, I want you!") # добавляем меню в бар
app.menu(bar) # указываем приложению на бар нашего меню
Tk.mainloop # и запускаем приложение, а почему бы и нет?



