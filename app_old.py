import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QStatusBar, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Logical Propositions")
        layout = QVBoxLayout()
        
        input_proposicion = QLineEdit()
        input_proposicion.setMaxLength(100)
        input_proposicion.setPlaceholderText("Enter the proposition")
        layout.addWidget(input_proposicion)
        

        button_check = QPushButton("Check syntax",self)    
        button_check.setToolTip("Check the syntaxis of proposition")
        layout.addWidget(button_check)


        layout.addStretch(0)
        
        label_author = QLabel("Author: Ionatan Perez")
        label_author.setAlignment(Qt.AlignRight)
        layout.addWidget(label_author)

        linkTemplate = '<a href={0}>{1}</a>'
        label_source = QLabel()
        label_source.setOpenExternalLinks(True)
        label_source.setText(linkTemplate.format('https://github.com/IonatanPerez/ProposicionesLogicas', 'Source code'))
        label_source.setAlignment(Qt.AlignRight)
        layout.addWidget(label_source)
        
        widget_main = QWidget()
        widget_main.setLayout(layout)

        self.setCentralWidget(widget_main)
        self.setStatusBar(QStatusBar(self))
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()