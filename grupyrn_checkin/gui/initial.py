# coding=utf-8
import sys
import threading
from threading import Timer

import pkg_resources

import grupyrn_checkin.gui

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *

from PIL import ImageTk, Image
from grupyrn_checkin import config, api


# __name__ in case you're within the package
# - otherwise it would be 'lidtk' in this example as it is the package name

class InitialFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master)

        _bg = 'white'

        self.text = Label(self, text=kwargs.get('text', _('Synchronizing...')), bg=_bg)
        self.text.config(font=("Courier", 40))
        self.text.pack(ipady=500)

        self.call_server()

    def show_error(self, text):
        self.text.config(fg='red', text=text)

    def call_server(self):
        ok, data = api.current_events()
        if ok:
            if not data:
                Timer(0.5, lambda: self.show_error(_('There is no event active.'))).start()

            else:
                self.master.put(event=data[0])
                Timer(0.5, lambda: self.master.replace_frame(
                    grupyrn_checkin.gui.IntroFrame
                )).start()
