# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from twisted.internet.defer import AlreadyCalledError
import random
import logging
from datetime import datetime
from configuration import configparam as params
from client import clttexts as textes
from configuration.configvar import NATIONALITES, ETUDES_DISCIPLINES, \
    ETUDES_ANNEES
from client.cltgui.cltguisrc import cltguiwelc, cltguipopup, cltguifinal, \
    cltguisummary, cltguihist, cltguiquestfinal
from util.utili18n import le2mtrans
from cltguitablemodels import TableModelHistorique
from cltguiwidgets import WExplication, WTableview, WPeriod

logger = logging.getLogger("le2m")


class GuiAccueil(QtGui.QDialog):
    """
    L'écran d'accueil. Un bouton permet d'informer l'expérimentateur que
    le sujet a fini de lire les instructions
    """
    def __init__(self, defered, automatique, parent):
        super(GuiAccueil, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique

        # creation gui
        self.ui = cltguiwelc.Ui_Dialog()
        self.ui.setupUi(self)

        # centre écran avec image labo
        welcfont = self.ui.label_welcome.font()
        welcfont.setPointSize(20)
        welcfont.setBold(True)
        self.ui.label_welcome.setText(u"<font color='blue'>{}</font>".format(
            textes.ACCUEIL_label_welcome))
        try:
            img_labo_pix = QtGui.QPixmap(params.getp("WELCOMEPICTURE"))
            self.ui.label_image_accueil.setPixmap(img_labo_pix)
        except IOError:
            self.ui.label_image_accueil.setText(
                textes.ACCUEIL_label_image_accueil)

        self.ui.label_instructions.setText(
            le2mtrans(u"Please read the instructions that stand beside the "
                      u"computer. You are asked to click on the button below "
                      u"when you have finished."))

        # bouton
        self.ui.pushButton_valider.setText(le2mtrans(u"Instructions read"))
        self.ui.pushButton_valider.clicked.connect(self._accept)
        
        self.setWindowTitle(textes.ACCUEIL_titre)
        self.setFixedSize(900, 575)
    
        if self._automatique: 
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._accept)
            self._timer.start(7000)

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        self.ui.pushButton_valider.setEnabled(False)
        logger.info(u"Welcome callback: 1")
        self._defered.callback(1)
        self.accept()
        
    def reject(self):
        pass


class GuiHistorique(QtGui.QDialog):
    def __init__(self, parent, historique):
        super(GuiHistorique, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)

        # table model: either historique or a new (empty) one
        self.tablemodel = TableModelHistorique(historique or [[], []])
        self.widtableview = WTableview(self, self.tablemodel)
        layout.addWidget(self.widtableview)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setWindowTitle(textes.le2mtrans(u"History"))
        self.adjustSize()
        self.setFixedSize(self.size())
        
    def reject(self):
        pass
        

class GuiRecapitulatif(QtGui.QDialog):
    """
    Boite de dialogue pour le récapitulatif de la période ou du jeu one-shot
    Si one-shot permet vaut 0
    ecran_historique permet, si précisé de passer un écran historique qui vient
    en remplacement de celui par défaut.
    """
    def __init__(self, defered, automatique, parent, periode, historique,
                 texte_recap, ecran_historique=None):
        super(GuiRecapitulatif, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique
        self.ecran_historique = \
            ecran_historique or GuiHistorique(self, historique)

        layout = QtGui.QVBoxLayout(self)

        if periode:
            self.widperiod = WPeriod(
                period=periode, ecran_historique=self.ecran_historique,
                parent=self)
            layout.addWidget(self.widperiod)

        self.widexplication = WExplication(text=texte_recap, parent=self)
        layout.addWidget(self.widexplication)

        # ligne historique (entêtes et dernière ligne de l'historique)
        histo_recap = [historique[0], historique[-1]]
        self.tablemodel = TableModelHistorique(histo_recap)
        self.widtableview = WTableview(parent=self, tablemodel=self.tablemodel,
                                       size=(450, 80))
        self.widtableview.ui.tableView.verticalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)
        layout.addWidget(self.widtableview)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        # automatique
        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)

        # taille et titre
        self.setWindowTitle(le2mtrans(u"Summary"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        """
        :return:
        """
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        logger.info(u"callback: Ok summary")
        self._defered.callback(1)
        self.accept()
        
    def reject(self):
        pass


class GuiPopup(QtGui.QDialog):
    def __init__(self, defered, txt, temps=7000, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = cltguipopup.Ui_Dialog()
        self.ui.setupUi(self)

        self._defered = defered
        self.ui.textEdit.setHtml(txt)

        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setVisible(False)
        self.ui.buttonBox.accepted.connect(self._accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle(le2mtrans(u"Information"))
        self.setFixedSize(350, 200)

        if temps > 0:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._accept)
            self._timer.start(temps)

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        self._defered.callback(1)
        self.accept()
            
    def reject(self):
        pass
    

class GuiFinal(QtGui.QDialog):
    """
    The final screen. Displays the final payoff and allows the subject to
    make comments
    """
    def __init__(self, defered, auto, parent, txt):
        super(GuiFinal, self).__init__(parent)

        self.ui = cltguifinal.Ui_Dialog()
        self.ui.setupUi(self)

        self._defered = defered
        self._automatique = auto

        self.ui.textEdit_explication.setText(txt)

        self.ui.label_merci.setText(
            le2mtrans(u"The experiment is over, thank you for your participation"))

        self.ui.label_commentaires.setText(
            u"<html><body><p>" +
            le2mtrans(u"You can write comments about the experiment in the "
                      u"area just below") + u"<br />" +
            le2mtrans(u"Click on the \"save\" button once finished.") +
            u"</p></body></html>")

        self.ui.pushButton_valider.setText(le2mtrans(u"Save"))
        self.ui.pushButton_valider.clicked.connect(self._save)

        if self._automatique:
            self.ui.textEdit_commentaires.setText(
                le2mtrans(u"This is an automatic sentence"))
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._save)
            self._timer.start(7000)

        self.setWindowTitle(le2mtrans(u"End of the experiment"))

    def _save(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass
        self.ui.pushButton_valider.setEnabled(False)
        self.ui.textEdit_commentaires.setEnabled(False)
        commentaires = unicode(
            self.ui.textEdit_commentaires.toPlainText().toUtf8(), "utf-8")
        # suppression des ; car exportation csv
        commentaires = commentaires.replace(";", ",")
        try:
            self._defered.callback(commentaires)
        except AlreadyCalledError:
            pass

    def reject(self):
        self._save()
        super(GuiFinal, self).reject()

    def close(self):
        self._save()
        super(GuiFinal, self).close()


class GuiQuestionnaireFinal(QtGui.QDialog):
    """
    Le questionnaire final
    """
    # todo: setText of all the widget of this dialog and translate the errors
    # messages
    def __init__(self, defered, automatique, parent=None):
        super(GuiQuestionnaireFinal, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique
        
        self.ui = cltguiquestfinal.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.textEdit.setText(textes.QUESTFINAL_explication)
        self.ui.textEdit.setFixedSize(600, 70)

        self._annee = datetime.now().year
        self.ui.spinBox_naissance.setValue(self._annee)
        self.ui.cb_nationalite.addItems(NATIONALITES)
        self.ui.cb_etudiant_discipline.addItems(ETUDES_DISCIPLINES)
        self.ui.cb_etudiant_niveau.addItems(ETUDES_ANNEES)
        self.ui.pushButton_valider.clicked.connect(self._stop)
        
        if self._automatique:

            # naissance --------------------------------------------------------
            alea_naissance = random.randint(16, 60)
            self.ui.spinBox_naissance.setValue(self._annee - alea_naissance)

            # genre ------------------------------------------------------------
            self.ui.rb_homme.setChecked(True) 
            if random.randint(0, 1):
                self.ui.rb_femme.setChecked(True)

            # nationalité ------------------------------------------------------
            self.ui.cb_nationalite.setCurrentIndex(
                random.randint(1, self.ui.cb_nationalite.count() - 1))

            # couple -----------------------------------------------------------
            self.ui.rb_couple_oui.setChecked(True) 
            if random.randint(0, 1):
                self.ui.rb_couple_non.setChecked(True)

            # etudiant ---------------------------------------------------------
            self.ui.rb_etudiant_oui.setChecked(True)
            if random.randint(0, 1):
                self.ui.rb_etudiant_non.setChecked(True)
            if self.ui.rb_etudiant_oui.isChecked():
                self.ui.cb_etudiant_discipline.setCurrentIndex(
                    random.randint(1,
                                   self.ui.cb_etudiant_discipline.count() - 1))
                self.ui.cb_etudiant_niveau.setCurrentIndex(
                    random.randint(1, self.ui.cb_etudiant_niveau.count() - 1))

            # expériences antérieures ------------------------------------------
            self.ui.rb_experiences_oui.setChecked(True)
            if random.randint(0, 1): 
                self.ui.rb_experiences_non.setChecked(True)

            # nombre frères et soeurs ------------------------------------------
            self.ui.spinBox_fratrie_nombre.setValue(random.randint(0, 10))

            # rang parmi frères et soeurs --------------------------------------
            self.ui.spinBox_fratrie_rang.setValue(
                0 if self.ui.spinBox_fratrie_nombre.value() == 0 else
                random.randint(0, self.ui.spinBox_fratrie_nombre.value() + 1))

            # sportivité -------------------------------------------------------
            self.ui.rb_sportif_oui.setChecked(True)
            if random.randint(0, 1):
                self.ui.rb_sportif_non.setChecked(True)
            if self.ui.rb_sportif_oui.isChecked():
                self.ui.rb_sportif_collectif.setChecked(True)
                if random.randint(0, 1): 
                    self.ui.rb_sportif_individuel.setChecked(True)
                self.ui.rb_sportif_competition_oui.setChecked(True)
                if random.randint(0, 1): 
                    self.ui.rb_sportif_competition_non.setChecked(True)

            # religiosité ------------------------------------------------------
            self.ui.cb_religion_place.setCurrentIndex(
                random.randint(1, self.ui.cb_religion_place.count() - 1))
            self.ui.cb_religion_croyance.setCurrentIndex(
                random.randint(1, self.ui.cb_religion_croyance.count() - 1))
            self.ui.cb_religion_nom.setCurrentIndex(
                random.randint(1, self.ui.cb_religion_nom.count() - 1))
            
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(self._stop)
            self._timer.start(7000)

        self.setWindowTitle(le2mtrans(u"Final questionnaire"))
        self.setFixedSize(715, 590)
    
    def reject(self):
        pass
    
    def _stop(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass

        self.ui.pushButton_valider.setEnabled(False)
        inputs = dict()
        try:
            # année de naissance -----------------------------------------------
            naissance = self.ui.spinBox_naissance.value()
            if naissance >= self._annee or naissance < (self._annee - 100): 
                raise ValueError(u"Année de naissance non valide.")
            else:
                inputs['naissance'] = naissance

            # genre ------------------------------------------------------------
            if not (self.ui.rb_homme.isChecked() or
                    self.ui.rb_femme.isChecked()):
                raise ValueError(u"Vous devez préciser votre genre.")
            else:
                inputs['genre'] = self.ui.rb_homme.isChecked()

            # nationalite ------------------------------------------------------
            if self.ui.cb_nationalite.currentIndex() == 0: 
                raise ValueError(u"Vous devez préciser votre nationalité.")
            else:
                inputs['nationalite'] = self.ui.cb_nationalite.currentIndex()

            # couple -----------------------------------------------------------
            if not (self.ui.rb_couple_oui.isChecked() or
                    self.ui.rb_couple_non.isChecked()):
                raise ValueError(u"Vous devez préciser si vous êtes "
                                 u"ou non en couple.")
            else:
                inputs['couple'] = self.ui.rb_couple_oui.isChecked()

            # étudiant ---------------------------------------------------------
            if not (self.ui.rb_etudiant_oui.isChecked() or
                    self.ui.rb_etudiant_non.isChecked()):
                raise ValueError(u"Vous devez préciser si vous êtes "
                                 u"ou non étudiant(e).")
            else:
                inputs['etudiant'] = self.ui.rb_etudiant_oui.isChecked()
            if inputs['etudiant'] is True:
                if self.ui.cb_etudiant_discipline.currentIndex() == 0:
                    raise ValueError(u"Vous devez préciser la discipline "
                                     u"que vous étudiez.")
                else: 
                    inputs['etudiant_discipline'] = \
                        self.ui.cb_etudiant_discipline.currentIndex()
                if self.ui.cb_etudiant_niveau.currentIndex() == 0: 
                    raise ValueError(u"Vous devez préciser votre niveau "
                                     u"d'études.")
                else: 
                    inputs['etudiant_niveau'] = \
                        self.ui.cb_etudiant_niveau.currentIndex()

            # participation expériences ----------------------------------------
            if not (self.ui.rb_experiences_oui.isChecked() or
                    self.ui.rb_experiences_non.isChecked()):
                raise ValueError(u"Vous devez préciser si vous avez déjà ou "
                                 u"non participer à une expérience d'économie.")
            else:
                inputs['experiences'] = self.ui.rb_experiences_oui.isChecked()

            # fratrie ----------------------------------------------------------
            inputs["fratrie_nombre"] = self.ui.spinBox_fratrie_nombre.value()
            inputs["fratrie_rang"] = self.ui.spinBox_fratrie_rang.value()
            if inputs["fratrie_nombre"] == 0 and inputs["fratrie_rang"] > 0:
                raise ValueError(u"Si vous n'avez pas de frères et soeurs "
                                 u"mettez 0 comme rang.")
            if inputs["fratrie_rang"] > inputs["fratrie_nombre"] + 1:
                raise ValueError(u"Si vous avez {fratrie_nombre} frères et "
                                 u"soeurs vous ne pouvez avoir comme rang "
                                 u"{fratrie_rang}".format(**inputs))
            
            # sportivité -------------------------------------------------------
            if not (self.ui.rb_sportif_oui.isChecked() or
                    self.ui.rb_sportif_non.isChecked()):
                raise ValueError(u"Vous devez préciser si vous pratiquez ou "
                                 u"non un sport")
            else:
                inputs['sportif'] = self.ui.rb_sportif_oui.isChecked()

            if inputs['sportif']:
                # Type de sport
                if not (self.ui.rb_sportif_collectif.isChecked() or
                        self.ui.rb_sportif_individuel.isChecked()):
                    raise ValueError(u"Vous devez préciser s'il s'agit d'un "
                                     u"sport individuel ou collectif")
                else:
                    inputs['sportif_type'] = \
                        self.ui.rb_sportif_individuel.isChecked()
                # Competition
                if not (self.ui.rb_sportif_competition_oui.isChecked() or
                        self.ui.rb_sportif_competition_non.isChecked()):
                    raise ValueError(u"Vous devez préciser si vous pratiquez "
                                     u"votre sport en compétition ou non")
                else:
                    inputs['sportif_competition'] = \
                        self.ui.rb_sportif_competition_oui.isChecked()

            # religion ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # religion_place
            if self.ui.cb_religion_place.currentIndex() == 0:
                raise ValueError(u"Vous devez préciser la place que tient "
                                 u"la religion dans votre vie")
            else:
                inputs['religion_place'] = \
                    self.ui.cb_religion_place.currentIndex()
            # religion_croyance
            if self.ui.cb_religion_croyance.currentIndex() == 0:
                raise ValueError(u"Vous devez préciser votre degré de croyance")
            else:
                inputs['religion_croyance'] = \
                    self.ui.cb_religion_croyance.currentIndex()
            # religion_nom
            if self.ui.cb_religion_nom.currentIndex() == 0:
                raise ValueError(u"Vous devez préciser le nom de votre "
                                 u"religion")
            else:
                inputs["religion_nom"] = self.ui.cb_religion_nom.currentIndex()
        
        except ValueError as e:
            QtGui.QMessageBox.critical(self, u"Erreur", e.message)
            self.ui.pushButton_valider.setEnabled(True)
            return
        
        if not self._automatique:
            confirm = QtGui.QMessageBox.question(
                self, u"Confirmation",
                u"Vous confirmez les informations saisies?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if confirm == QtGui.QMessageBox.No:
                self.ui.pushButton_valider.setEnabled(True)
                return
        self._defered.callback(inputs)
        self.accept()
