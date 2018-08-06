import os

from grupyrn_checkin.app import GruPyRNCheckin

if __name__ == '__main__':
    app = GruPyRNCheckin()

    # Enter fullscreen automatically when on Raspberry
    if os.uname()[4][:3] == 'arm':
        app.toggle_fullscreen()

    app.mainloop()
