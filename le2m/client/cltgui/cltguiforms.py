# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from client.cltgui.cltguisrc import cltguiwait
from util.utili18n import le2mtrans


class GuiAttente(QtGui.QWidget):
    """
    The waiting screen. This is the main screen of the application, the only
    one to be fullscreen
    """
    def __init__(self, parent=None):
        super(GuiAttente, self).__init__(parent)

        self.ui = cltguiwait.Ui_WaitingScreen()
        self.ui.setupUi(self)

        self.ui.lbl_waiting.setText(le2mtrans(u"Please wait ..."))

