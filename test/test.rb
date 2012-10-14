#!/usr/bin/env ruby
#require "rubygems"
#require "active_record"
#require 'active_support'
require 'tk' # ����������� ����������
#require 'mathn'

app = TkRoot.new { # ������ ����
     title "Hello Tk!"; padx 50; pady 15 # � ������� ��� ����������
}

lbl = TkLabel.new(app) { # ������ �������
     text "Something wasn't clicked yet..." # � ����� ��� �������
     pack { padx 100; pady 100; side "left" } # � ������ ������������
}
java_clicked = Proc.new { # ����� ���� "Java" � ����
     lbl.text "Java was liked..."
}
sc_clicked = Proc.new { # ����� ���� "Scala" � ����
     lbl.text "Scala was liked..."
}
cpp_clicked = Proc.new { # ����� ���� "C" � ����
     lbl.text "C was liked..."
}
py_clicked = Proc.new { # ����� ���� "Python" � ����
     lbl.text "Python was liked..."
}
rb_clicked = Proc.new { # ����� ���� "Ruby" � ����
     lbl.text "Ruby was liked..."
}
=begin
=end
menu = TkMenu.new(app)# ������ ���� 
menu.add('command', 'label' => "Java", 'command' => java_clicked) # ������ ������ "Java"
menu.add('command', 'label' => "Scala", 'command' => sc_clicked) # ������ ������ "Scala"
menu.add('separator') # ������ �����������
menu.add('command', 'label' => "C", 'command' => cpp_clicked) # ������ ������ "C"
menu.add('separator') # ������ �����������
menu.add('command', 'label' => "Python", 'command' => py_clicked) # ������ ������ "Python"
menu.add('command', 'label' => "Ruby", 'command' => rb_clicked) # ������ ������ "Ruby"
bar = TkMenu.new # ������ ��� ��� ������ ����
bar.add('cascade', 'menu' => menu, 'label' => "Click me, I want you!") # ��������� ���� � ���
app.menu(bar) # ��������� ���������� �� ��� ������ ����
Tk.mainloop # � ��������� ����������, � ������ �� � ���?



