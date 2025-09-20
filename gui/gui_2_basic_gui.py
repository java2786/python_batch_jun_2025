import sys
from PyQt5.QtWidgets import QApplication, QWidget


# create board
app = QApplication(sys.argv)

# create window
window = QWidget()
window.setWindowTitle("Basic GUI Application")
window.setGeometry(100, 100, 280, 80)
window.move(1000, 30)

window.show()

# run application in loop
sys.exit(app.exec_())