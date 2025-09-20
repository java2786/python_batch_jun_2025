import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QGridLayout, QPushButton
from PyQt5.QtCore import Qt

class SimpleCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My calculator")
        self.setGeometry(200, 200, 450, 500)
        self.init_ui()
    
    def init_ui(self):
        # main layout
        main_layout = QVBoxLayout()
        
        # display screen
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setText("0")
        self.display.setStyleSheet("font-size: 30px;padding: 10px;")
        
        # calculator initial state
        self.new_number = True 
        self.current_input = ""
        self.total = 0
        self.operation = ""
        
        
        
        main_layout.addWidget(self.display)  
        self.setLayout(main_layout)
        
        # button layout
        button_layout = QGridLayout()
        # button text
        buttons = [
            ['C', '±', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '='],
        ]
        
        # Create and place buttons in the grid layout
        for row, button_row in enumerate(buttons):
            for col, button_text in enumerate(button_row):
                if button_text == '':
                    continue;
                
                # create button with text and style
                button = QPushButton(button_text)
                button.setStyleSheet("font-size: 20px;padding: 10px;")

                button_layout.addWidget(button, row, col)
                
                # connect button to handler/method/function
                button.clicked.connect(lambda checked, text=button_text: self.button_clicked(text))
                
        # add layouts to main layout
        main_layout.addWidget(self.display)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
            
    def button_clicked(self, button_text):
        print(f"Button {button_text} clicked")
        # handle button click event to evaluate
        if button_text.isdigit() or button_text=='.':
            self.handle_number(button_text)
        elif button_text in ['+', '-', '/', '*']:
            self.handle_operator(button_text)
        elif button_text=='=':
            self.handle_equals()
        elif button_text=='C':
            self.reset()

    def handle_number(self, button_text):
        if self.new_number:
            self.current_input = button_text
            self.new_number = False 
        else:
            if button_text == '.' and '.' in self.current_input:
                return
            self.current_input += button_text
        print(self.current_input)
        self.display.setText(self.current_input)
        
    # + - / *
    def handle_operator(self, operator): 
        if operator == '':
            return 
        if self.current_input == "":
            return
        # 32 +
        # 2 + 4 +
        if self.operation and not self.new_number:
            self.handle_equals()
        else:
            self.total = float(self.current_input)
            self.operation = operator
            self.new_number = True 
        
    def handle_equals(self):
        if self.operation == "" or self.current_input =="":
            return 
        try:
            current_number = float(self.current_input) 
            if self.operation == "+":
                result = self.total + current_number
            elif self.operation == "-":
                result = self.total - current_number
            elif self.operation == "*":
                result = self.total * current_number
            elif self.operation == "/":
                if current_number == 0:
                    self.display.setText("Cannot divide by zero")
                    self.reset()
                    return 
                result = self.total / current_number
                
            self.display.setText(str(result))
            self.current_input = str(result)
            self.operation = ""
            self.new_number = True
            
        except Exception as ex:
            self.display.setText("Error")
            self.reset()

            
    def reset(self):
        self.new_number = True 
        self.current_input = ""
        self.total = 0
        self.operation = ""
        
        self.display.setText("")
        self.current_input = ""
        self.operation = ""
        self.new_number = True
""" 
self.new_number = True 
self.current_input = ""
self.total = 0
self.operation = ""
"""
if(__name__ == '__main__'):
    app = QApplication(sys.argv)

    calc = SimpleCalculator()
    calc.show()

    # run application in loop
    sys.exit(app.exec_())