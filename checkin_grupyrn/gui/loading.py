# coding=utf-8
import sys
from threading import Timer
import checkin_grupyrn.gui
import urllib, cStringIO
from hashlib import md5

import checkin_grupyrn.gui

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *

from PIL import ImageTk, Image


class LoadingFrame(Frame):
    def __init__(self, master, func, *args, **kwargs):
        Frame.__init__(self, master)

        text = Label(self, text=kwargs.get('text', _('Loading...')))
        text.config(font=("Courier", 40))

        text.pack(ipady=500)

        result = func(*args)
        redirect = kwargs.get('redirect', checkin_grupyrn.gui.IntroFrame)

        Timer(3.0, lambda: master.replace_frame(redirect)).start()
