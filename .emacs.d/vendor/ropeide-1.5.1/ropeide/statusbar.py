from Tkinter import *

import rope.base.exceptions
import ropeide.uihelpers


class StatusBarException(ropeide.uihelpers.RopeUIError):
    pass


class StatusText(object):

    def __init__(self, status_bar_manager, kind, label):
        self.manager = status_bar_manager
        self.kind = kind
        self.label = label
        self.width = 0

    def set_width(self, width):
        self.width = width
        self.set_text(self.get_text())
        #        self.label['width'] = width

    def set_text(self, text):
        self.label['text'] = text.ljust(self.width)

    def get_text(self):
        return self.label['text'].rstrip()

    def remove(self):
        self.manager.remove_status(self)


class StatusBarManager(object):
    """Manages the status bar"""

    def __init__(self, status_bar, font=('courier',)):
        self.status_bar = status_bar
        self.font = font
        self.status_text = {}

    def get_status(self, kind):
        if kind not in self.status_text:
            raise StatusBarException('StatusText <%s> does not exist' % kind)
        return self.status_text[kind]

    def create_status(self, kind):
        if kind in self.status_text:
            raise StatusBarException('StatusText <%s> already exists' % kind)
        label = Label(self.status_bar, text=' ', height=1,
                      relief=RIDGE, font=self.font)
        if self.font is not None:
            label['font'] = self.font
        self.status_text[kind] = StatusText(self, kind, label)
        label.pack(side=LEFT)
        self.status_text[kind].set_text('')
        return self.status_text[kind]

    def remove_status(self, status):
        if status.kind in self.status_text:
            status.label.destroy()
            del self.status_text[status.kind]
