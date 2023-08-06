Brief Introduction
  Python-Extension is an extension of Python,
It is divided into pyextension and tkextension,
tkextension is particularly powerful. 


What’s New In Python-Extension 1.4
  Pyextension
    Pyextension
      1.Added open and save functions
    Math
      1.New functions such as fibo, arithmetic_sequence
    Word Bank
      1.Synchronized pyextension word_bank thesaurus
  Tkextension
    Tkextension
      1.Split the fastusefile function and move it to the pyextension module
      2.Removed library singlechoice
    BlackBoard
      1.
    Tix
      1.Added options width and height
        Example:
          # -*- coding=utf-8 -*-
          # Python 3.10.0rc2
          
          from tkinter import *
          import tkextension.tix as tix
          
          tk = Tk()
          
          AskAnswer(tk, msg=‘Python version: ’, width=50).pack()
          
          tk.mainloop()
      2.Removed library SingleChoice
      3.Removed argument ‘get’
      4.Merged tix and ttk and renamed ‘ttk’ to ‘filedialog’
      5.Option filetypes added to FileDialog
    System
      1.Fixed error of the module ‘turtle’


Pyextension
  Pyextension includes main modules
(open source function, computer information function),
mathematical function processing module, password encryption module,
English Thesaurus module and Microsoft Word document processing module.


Tkextension
  Tkextension includes dialog window,tix widget,
quick generation of Tkinter object,
quick document processing (open and save as),
tix module, ttk module,
open source module,
small blackboard module, turtle graphics drawing module and timer module