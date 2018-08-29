# coding=utf-8
import os
import sys
import threading
from time import sleep

import cv2
import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar

import grupyrn_checkin.gui
from grupyrn_checkin.decoder import decode_qrcode

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *

from PIL import Image, ImageTk


class CameraFrame(Frame):

    def __init__(self, master, check):
        Frame.__init__(self, master)

        self._bg = 'white'
        self.configure(bg=self._bg)

        text = Label(self, text=_(u'Place the QR-Code on the camera'), bg=self._bg)
        text.config(font=("Courier", 25))
        text.pack(ipady=20, expand=1, fill=Y)

        self.vs = VideoStream(usePiCamera=os.uname()[4][:3] == 'arm').start()
        self.check = check
        self.panel = None
        self.videoframe = None
        self.found = None

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        cancel_button = Button(self, text=_(u'Cancel'), fg='red',
                               command=lambda: master.replace_frame(grupyrn_checkin.gui.IntroFrame),
                               font=("Courier", 24),
                               height=1, width=20)
        cancel_button.pack(pady=(0, 20), side=BOTTOM)

    def videoLoop(self):
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.videoframe = self.vs.read()
                while self.vs.read() is None:
                    sleep(0.3)
                    self.videoframe = self.vs.read()
                self.videoframe = imutils.resize(self.videoframe, width=450)

                barcodes = pyzbar.decode(self.videoframe)

                # loop over the detected barcodes
                for barcode in barcodes:
                    # extract the bounding box location of the barcode and draw
                    # the bounding box surrounding the barcode on the image
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(self.videoframe, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    barcode_data = barcode.data.decode("utf-8")
                    barcode_type = barcode.type

                    if barcode_type == 'QRCODE':
                        if not self.found:
                            self.found = barcode_data
                            break

                    # draw the barcode data and barcode type on the image
                    # text = "{} ({})".format(barcodeData, barcodeType)
                    # cv2.putText(self.videoframe, text, (x, y - 10),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.videoframe, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image).transpose(Image.FLIP_LEFT_RIGHT)

                image = ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = Label(self, image=image)
                    self.panel.image = image
                    self.panel.pack(padx=10, pady=10)
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

                if self.found:
                    self.stopEvent.set()
                    self.master.replace_frame(grupyrn_checkin.gui.CheckinFrame, self.found, self.check)
        except TclError:
            print("[INFO] caught a TclError")

    def destroy(self):
        self.stopEvent.set()
        self.vs.stop()
        Frame.destroy(self)
