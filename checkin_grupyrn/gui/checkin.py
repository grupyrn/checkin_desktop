# coding=utf-8
import sys
from threading import Timer

import checkin_grupyrn.gui
import urllib, cStringIO
from hashlib import md5

import checkin_grupyrn.gui
from checkin_grupyrn import config, api

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *

from PIL import ImageTk, Image


class CheckinFrame(Frame):

    _url = 'https://www.gravatar.com/avatar/{}?s=200&d={}'
    _bg = 'white'

    def __init__(self, master, data, check):
        Frame.__init__(self, master)

        self.data = data
        self.check = check

        self.text = Label(self, text=_('Loading...'), bg=self._bg)
        self.show_text(font=("Courier", 40))

        self.load()

    def show_text(self, **kwargs):
        self.text.pack_forget()
        self.text.configure(**kwargs)
        self.text.pack(ipady=500)

    def hide_text(self):
        self.text.pack_forget()

    def load(self):
        ok, response = api.event_check(member_data=self.data, event=self.master.get('event'), check=self.check)
        if ok:
            self.hide_text()
            self.show_info()
        else:
            self.show_text(text=_(response['message']), fg='red')
            Timer(3.0, lambda: self.master.replace_frame(checkin_grupyrn.gui.IntroFrame)).start()

    def show_info(self):
        url = self._url.format(md5(self.data.get('email')).hexdigest(), urllib.quote(config.get('fallback_avatar')))
        imagefile = cStringIO.StringIO(urllib.urlopen(url).read())
        img = ImageTk.PhotoImage(Image.open(imagefile))
        panel = Label(self, image=img)
        panel.image = img

        if self.check:
            greeting = _(u'Welcome, {}!')
        else:
            greeting = _(u'Thank you, {}!')

        first_name = self.data.get('name').split()[0]
        text = Label(self, text=greeting.format(first_name), bg=self._bg)
        text.config(font=("Courier", 40))

        panel.pack(expand=1, fill=Y, pady=(80, 40))
        text.pack(pady=(0, 40))

        Timer(2.0, lambda: self.master.replace_frame(checkin_grupyrn.gui.IntroFrame)).start()
