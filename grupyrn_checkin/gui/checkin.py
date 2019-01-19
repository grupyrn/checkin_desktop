# coding=utf-8
import sys
import urllib
from hashlib import md5
from threading import Timer

import grupyrn_checkin.gui
import grupyrn_checkin.gui
from grupyrn_checkin import config, api

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
    from urllib import quote, urlopen  # Python 2.X
    from cStringIO import StringIO
else:
    from tkinter import *
    from urllib.parse import quote  # Python 3+
    from urllib.request import urlopen  # Python 3+
    from io import StringIO, BytesIO


from PIL import ImageTk, Image


class CheckinFrame(Frame):
    _url = 'https://www.gravatar.com/avatar/{}?s=200&d={}'
    _bg = 'white'

    def __init__(self, master, data, check, **kwargs):
        Frame.__init__(self, master, bg=self._bg)

        self.subevents = kwargs.get('subevents', False)

        self.data = data
        self.check = check
        self.response = None

        self.text = Label(self, text=_('Loading...'), wraplength=350, bg=self._bg)
        self.show_text(font=("Courier", 40))

        self.load()

    def show_text(self, **kwargs):
        self.text.pack_forget()
        self.text.configure(**kwargs)
        self.text.pack(ipady=500)

    def hide_text(self):
        self.text.pack_forget()

    def load(self):
        if not self.subevents:
            ok, self.response = api.event_check(uuid=self.data, check=self.check)
        else:
            ok, self.response = api.subevent_checkout(uuid=self.data)
        if ok:
            self.hide_text()
            self.show_info()
        else:
            self.show_text(text=_(self.response['message']), fg='red')
            Timer(3.0, lambda: self.master.replace_frame(grupyrn_checkin.gui.IntroFrame)).start()

    def show_info(self):
        url = self._url.format(md5(self.response.get('attendee').get('email').encode('utf-8')).hexdigest(),
                               quote(config.get('fallback_avatar')))

        if sys.version_info[0] == 2:
            imagefile = StringIO(urlopen(url).read())
        else:
            imagefile = BytesIO(urlopen(url).read())

        img = ImageTk.PhotoImage(Image.open(imagefile))
        panel = Label(self, image=img, bg=self._bg)
        panel.image = img

        if self.check:
            greeting = _(u'Welcome, {}!')
        else:
            greeting = _(u'Thank you, {}!')

        first_name = self.response.get('attendee').get('name').split()[0]

        if sys.version_info[0] == 2:
            greeting = unicode(greeting)

        text = Label(self, text=greeting.format(first_name), bg=self._bg)
        text.config(font=("Courier", 40))

        panel.pack(expand=1, fill=Y, pady=(80, 40))
        text.pack(pady=(0, 40))

        Timer(2.0, lambda: self.master.replace_frame(grupyrn_checkin.gui.IntroFrame)).start()

