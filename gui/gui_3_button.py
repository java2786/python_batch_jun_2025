import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

class GreetingApp(QWidget): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button + Event")
        self.setGeometry(100, 100, 480, 280)
        self.move(500, 500)
        
        self.button = QPushButton("Greet", self)
        self.button.move(100, 0)
        
        # click button - handler 
        self.button.clicked.connect(self.on_click)

    def on_click(self):
        print("Button clicked")
        QMessageBox.information(self, "Greeting", "Hello, User!")

# create board
app = QApplication(sys.argv)

my_window = GreetingApp()
my_window.show()

# run application in loop
sys.exit(app.exec_())