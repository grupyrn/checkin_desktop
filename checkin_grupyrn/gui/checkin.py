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


class CheckinFrame(Frame):

    _url = 'https://www.gravatar.com/avatar/{}?s=200'

    def __init__(self, master, data, check):
        Frame.__init__(self, master)

        _bg = 'white'

        url = self._url.format(md5(data.get('email')).hexdigest())
        imagefile = cStringIO.StringIO(urllib.urlopen(url).read())
        img = ImageTk.PhotoImage(Image.open(imagefile))
        panel = Label(self, image=img)
        panel.image = img

        if check:
            greeting = _(u'Welcome, {}!')
        else:
            greeting = _(u'Thank you, {}!')

        first_name = data.get('name').split()[0]
        text = Label(self, text=greeting.format(first_name), bg=_bg)
        text.config(font=("Courier", 40))

        panel.pack(expand=1, fill=Y, pady=(80, 40))
        text.pack(pady=(0, 40))

        Timer(3.0, lambda: master.replace_frame(checkin_grupyrn.gui.IntroFrame)).start()
