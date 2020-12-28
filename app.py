import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QStatusBar, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import Qt



class HyperlinkLabel(QLabel):

    def __init__(self, parent=None):

        super().__init__()


        self.setOpenExternalLinks(True)

        self.setParent(parent)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Logical Propositions")


        input_proposicion = QLineEdit()
        input_proposicion.setMaxLength(100)
        input_proposicion.setPlaceholderText("Enter the proposition")
        
        label_author = QLabel("Author: Ionatan Perez")
        label_author.setAlignment(Qt.AlignBottom| Qt.AlignRight)

        linkTemplate = '<a href={0}>{1}</a>'
        label_source = HyperlinkLabel(self)
        label_source.setText(linkTemplate.format('https://github.com/IonatanPerez/ProposicionesLogicas', 'Source code'))
        label_source.setAlignment(Qt.AlignBottom| Qt.AlignRight)
 
        
        self.setStatusBar(QStatusBar(self))

        layout = QVBoxLayout()
        layout.addWidget(input_proposicion)
        layout.addStretch(0)
        layout.addWidget(label_author)
        layout.addWidget(label_source)
        

        widget_main = QWidget()
        widget_main.setLayout(layout)

        self.setCentralWidget(widget_main)
        self.setStatusBar(QStatusBar(self))
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()