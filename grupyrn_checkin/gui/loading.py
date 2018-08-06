# coding=utf-8
import sys
from threading import Timer
import grupyrn_checkin.gui
import urllib, cStringIO
from hashlib import md5

import grupyrn_checkin.gui

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *

from PIL import ImageTk, Image


class LoadingFrame(Frame):
    def __init__(self, master, func, *args, **kwargs):
        Frame.__init__(self, master)

        _bg = 'white'

        text = Label(self, text=kwargs.get('text', _('Loading...')), bg=_bg)
        text.config(font=("Courier", 40))

        text.pack(ipady=500)

        result = func(*args)
        redirect = kwargs.get('redirect', grupyrn_checkin.gui.IntroFrame)

        Timer(2.0, lambda: master.replace_frame(redirect)).start()
