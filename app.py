import gettext

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

_ = gettext.gettext

def print_some_strings():
    print(_("Hello world"))
    print(_("aanother thing"))





es = gettext.translation('base', localedir='locales', languages=['es'])
es.install()
_ = es.gettext

if __name__=='__main__':
    print_some_strings()

