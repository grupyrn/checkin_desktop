# coding=utf-8
import sys

import pkg_resources

import checkin_grupyrn.gui

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *

from PIL import ImageTk, Image
from checkin_grupyrn import config


# __name__ in case you're within the package
# - otherwise it would be 'lidtk' in this example as it is the package name

class IntroFrame(Frame):

    def __init__(self, master):
        bg = 'white'
        Frame.__init__(self, master, bg=bg)

        right_panel = Frame(self, bg=bg)

        path = '../assets/logo_flat.png'  # always use slash
        filepath = pkg_resources.resource_filename(__name__, path)

        img = ImageTk.PhotoImage(Image.open(filepath), format='png')
        logo = Label(self, image=img, bg=bg)
        logo.image = img

        title = Label(right_panel, text=config.get('title'), bg=bg)
        title.config(font=("Courier", 40))

        button_checkin = Button(right_panel, text=_(u'Check-in'), fg='green', bg='#aaaaaa',
                                command=lambda: master.replace_frame(checkin_grupyrn.gui.CameraFrame, True),
                                font=("Courier", 24), height=3, width=20)
        button_checkout = Button(right_panel, text=_(u'Check-out'), fg='red', bg='#aaaaaa',
                                 command=lambda: master.replace_frame(checkin_grupyrn.gui.CameraFrame, False),
                                 font=("Courier", 24), height=3, width=20)

        logo.pack(padx=(40, 0), side=LEFT, expand=1, fill=Y, ipady=100)

        title.pack(pady=(0, 40))
        button_checkin.pack()
        button_checkout.pack()
        right_panel.pack(padx=(100, 40), side=RIGHT)
