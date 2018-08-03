import sys
from os.path import abspath

import pkg_resources

from checkin_grupyrn.gui import intro
from checkin_grupyrn import config
from checkin_grupyrn.i18n import *

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *


class GruPyRNCheckin(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title(config.get('window_title'))
        self.configure(background='white')
        # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        # self.tk.attributes('-zoomed', True)
        path = 'assets/icon.png'  # always use slash
        filepath = pkg_resources.resource_filename(__name__, path)
        imgicon = PhotoImage(file=abspath(filepath))
        self.call('wm', 'iconphoto', self._w, imgicon)

        self.geometry('800x480')

        self._frame = None
        self.replace_frame(intro.IntroFrame)

        self.fullscreen_state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        # self.toggle_fullscreen()

    def toggle_fullscreen(self, event=None):
        self.fullscreen_state = not self.fullscreen_state  # Just toggling the boolean
        self.attributes("-fullscreen", self.fullscreen_state)
        return "break"

    def end_fullscreen(self, event=None):
        self.fullscreen_state = False
        self.attributes("-fullscreen", False)
        return "break"

    def replace_frame(self, frame_class, *args, **kwargs):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, *args, **kwargs)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
