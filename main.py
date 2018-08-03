import os

from checkin_grupyrn.app import GruPyRNCheckin

if __name__ == '__main__':
    app = GruPyRNCheckin()

    # Enter fullscreen automatically when on Raspberry
    if os.uname()[4][:3] == 'arm':
        app.toggle_fullscreen()

    app.mainloop()
