# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cltguifinal.ui'
#
# Created: Thu Jan 28 09:58:33 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(572, 541)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_merci = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_merci.setFont(font)
        self.label_merci.setObjectName(_fromUtf8("label_merci"))
        self.horizontalLayout_3.addWidget(self.label_merci)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textEdit_explication = QtGui.QTextEdit(Dialog)
        self.textEdit_explication.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_explication.sizePolicy().hasHeightForWidth())
        self.textEdit_explication.setSizePolicy(sizePolicy)
        self.textEdit_explication.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit_explication.setMaximumSize(QtCore.QSize(550, 80))
        self.textEdit_explication.setReadOnly(True)
        self.textEdit_explication.setObjectName(_fromUtf8("textEdit_explication"))
        self.horizontalLayout.addWidget(self.textEdit_explication)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.label_commentaires = QtGui.QLabel(Dialog)
        self.label_commentaires.setObjectName(_fromUtf8("label_commentaires"))
        self.horizontalLayout_2.addWidget(self.label_commentaires)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.textEdit_commentaires = QtGui.QTextEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_commentaires.sizePolicy().hasHeightForWidth())
        self.textEdit_commentaires.setSizePolicy(sizePolicy)
        self.textEdit_commentaires.setMinimumSize(QtCore.QSize(550, 300))
        self.textEdit_commentaires.setMaximumSize(QtCore.QSize(550, 500))
        self.textEdit_commentaires.setObjectName(_fromUtf8("textEdit_commentaires"))
        self.horizontalLayout_4.addWidget(self.textEdit_commentaires)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.pushButton_valider = QtGui.QPushButton(Dialog)
        self.pushButton_valider.setObjectName(_fromUtf8("pushButton_valider"))
        self.horizontalLayout_5.addWidget(self.pushButton_valider)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        spacerItem6 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.verticalLayout_2.addItem(spacerItem6)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_merci.setText(_translate("Dialog", "L\'expérience est terminée, merci pour votre participation", None))
        self.label_commentaires.setText(_translate("Dialog", "<html><body><p>Vous pouvez écrire des commentaires sur l\'expérience dans la zone ci-dessous.<br>Cliquez sur le bouton \"Enregistrer les commentaires\" lorsque vous avez terminé.</p></body></html>", None))
        self.pushButton_valider.setText(_translate("Dialog", "Enregistrer les commentaires", None))

