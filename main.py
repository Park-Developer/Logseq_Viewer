
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
import os
import make_doc

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Button
        self.Load_Btn=QPushButton("Load")
        self.Load_Btn.clicked.connect(self.load_clicked)
        # Label
        self.log_dir = QLabel('Directory : ', self)
        self.log_dir__val=QLabel(os.getcwd() , self)

        self.state = QLabel('State : ', self)
        self.state__val=QLabel("" , self)

        self.vbox=QVBoxLayout()


        self.hbox1= QHBoxLayout()
        self.hbox1.addWidget(self.log_dir)
        self.hbox1.addWidget(self.log_dir__val)
        
        self.hbox2= QHBoxLayout()
        self.hbox2.addWidget(self.state)
        self.hbox2.addWidget(self.state__val)

        self.hbox3= QHBoxLayout()
        self.hbox3.addWidget(self.Load_Btn)
        
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

        self.setLayout(self.vbox)

        self.setWindowTitle('Logseq View')
        self.move(300, 300)
        self.resize(400, 200)
        self.show()

    def load_clicked(self):
        self.state__val.setText("Upload!")
        
        # Initial Setting
        logseq_addr=os.getcwd()
        debug_flag=True

        # Create Logseq Doc!
        make_doc.create_log_Doc(logseq_addr,debug_flag) 


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())