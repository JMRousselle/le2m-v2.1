#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This script helps to create the skelet of parts for LE2M
"""

import sys
import os
import shutil
import logging
from PyQt4 import QtGui
from creatorutil import creatortrans, get_appdir
import creatorutil
from creatorgui import GuiCreator


# for i18n
if sys.platform.startswith("win"):
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang

logger = None


def gdir(b, d):
    return os.path.join(b, d)


def creator():
    def close():
        if __name__ == "__main__":
            sys.exit(0)
        else:
            return

    global logger
    creatorutil.create_logger()
    logger = logging.getLogger("creator")
    screen = GuiCreator()

    if screen.exec_():
        expe_directory, configuration = screen.get_configuration()

        substitutions = {
            "EXPERIENCE_NOM": configuration.expe_name,
            "EXPERIENCE_NOM_COURT": configuration.expe_shortname,
            "EXPERIENCE_MENU": configuration.expe_menu,
            "EXPERIENCE_REPETITIONS_NOMBRE": configuration.periods,
            "EXPERIENCE_GROUPES_TAILLE": configuration.groups_size,
            "EXPERIENCE_GROUPES_FORMATION_CHAQUE_PERIODE":
                configuration.groups_eachperiod,
            "EXPERIENCE_MONNAIE": configuration.currency
        }

        steps = [
            (create_directories,
             [expe_directory, configuration.expe_name]),
            (copy_files,
             [expe_directory, configuration.expe_name]),
            (substitute_words,
             [os.path.join(expe_directory, configuration.expe_name),
              substitutions])]
        for s in steps:
            logger.info(creatortrans(
                u"Call of {func} with args {args} ...").format(
                func=s[0].__name__, args=s[1:]))
            if not s[0](*s[1]):
                QtGui.QMessageBox.critical(
                    None, creatortrans(u"Error"),
                    creatortrans(u"Something wrong happens! Contact "
                                 u"the developer and/or look the logs"))
        logger.info(
            creatortrans(u"Files for {expename} created successfully").format(
                expename=configuration.expe_name))
        QtGui.QMessageBox.information(
            None, creatortrans(u"Success"),
            creatortrans(u"Files for {expename} created successfully").format(
                expename=configuration.expe_name))
        close()

    else:
        close()


def create_directories(expedir, expename):
    """
    Create the directories as well as the __init__ files
    In the main __init__ file import the part module, it is for sqlalchemy
    (because the part module is not imported in the server module)
    :param expedir:
    :param expename:
    :return:
    """
    target = gdir(expedir, expename)
    try:

        if os.path.exists(target):
            raise ValueError(
                creatortrans(u"A directory with the same part name already "
                             u"exists"))
        os.mkdir(target)
        with open(os.path.join(target, "__init__.py"), "wb") as f:
            f.write("import {}Part  # for sqlalchemy".format(expename))
        os.mkdir(gdir(target, "{}GuiSrc".format(expename)))
        open(os.path.join(
            target, "{}GuiSrc".format(expename), "__init__.py"), "wb").close()
        os.mkdir(gdir(target, "{}Doc".format(expename)))
        # i18n
        os.mkdir(gdir(target, "locale"))
        os.mkdir(os.path.join(target, "locale", "en_US"))
        os.mkdir(os.path.join(target, "locale", "en_US", "LC_MESSAGES"))
        os.mkdir(os.path.join(target, "locale", "fr_FR"))
        os.mkdir(os.path.join(target, "locale", "fr_FR", "LC_MESSAGES"))

    except (ValueError, IOError) as e:
        logger.critical(creatortrans(u"Error: {msg}".format(msg=e)))
        return 0

    else:
        return 1


def copy_files(expedir, expename):
    src = os.path.join(get_appdir(), "filestocopy")
    target = os.path.join(expedir, expename)

    try:
        for f in [i for i in os.listdir(src) if not ("__init__" in i or
            os.path.splitext(i)[1] == ".pyc")]:
            fin = os.path.join(src, f)
            suf = fin.split("_")[1]
            if "Decision" in fin:
                fout = \
                    os.path.join(target, "{}GuiSrc".format(expename),
                                 "{}{}".format(expename, suf))
            else:
                fout = os.path.join(target, "{}{}".format(expename, suf))
            logger.info("Copy of {} to {}".format(fin, fout))
            shutil.copy(fin, fout)

    except (IOError, ValueError) as e:
        logger.info(creatortrans(u"Error: {msg}").format(msg=e))
        return 0

    else:
        return 1


def substitute_words(expedir, substitutions):
    try:
        for filename in os.listdir(expedir):
            filepath = os.path.join(expedir, filename)

            if os.path.isfile(filepath) and \
                os.path.splitext(filepath)[1] == ".py":

                logger.info(creatortrans(
                    u"Substitutions for file {}").format(filepath))

                with open(filepath, 'r') as f:
                    filedata = f.read().decode("utf-8")

                for oldword, newword in substitutions.iteritems():
                    filedata = filedata.replace(oldword, newword)

                with open(filepath, 'w') as f:
                    f.write(unicode.encode(filedata, "utf-8"))

    except IOError as e:
        logger.info(creatortrans(u"Error: {msg}").format(msg=e))
        return 0

    else:
        return 1


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    creator()
    sys.exit(app.exec_())