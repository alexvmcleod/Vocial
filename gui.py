import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from vocial import Vocial

class ChatWidget(QWidget):

    message_sent = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        
        self.setWindowTitle("Vocial")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
            }
            QTextEdit {
                background-color: #383838;
                color: #ffffff;
                border: 1px solid #5f5f5f;
                border-radius: 5px;
            }
            QLineEdit {
                background-color: #383838;
                color: #ffffff;
                border: 1px solid #5f5f5f;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #3e3e3e;
                color: #ffffff;
                border: 1px solid #5f5f5f;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4e4e4e;
            }
        """)

        self.layout = QVBoxLayout()

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        self.layout.addWidget(self.chat_history)
        self.layout.addWidget(self.message_input)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

    def send_message(self):
        message = self.message_input.text()
        self.message_sent.emit(message)
        self.message_input.clear()

    def add_message(self, message):
        self.chat_history.append(message)


class ChatApp(QApplication):

    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.asking_first_question = True
        self.first_question_response = None
        self.vocial = Vocial()
        self.init_ui()

    def init_ui(self):
        self.chat_widget = ChatWidget()
        self.chat_widget.message_sent.connect(self.handle_message_sent)
        self.chat_widget.add_message("Vocial: What is your username?\n")
        self.chat_widget.show()

    def handle_message_sent(self, message):
        # Replace this line with your function that processes the message and returns a response
        if self.asking_first_question:
            self.first_question_response = message
            self.chat_widget.add_message(f"Vocial: Welcome, {self.first_question_response}!\n")
            self.asking_first_question = False
        else:
            response = f"{self.first_question_response}: {message}\n"
            self.chat_widget.add_message(response)
            responsething = f"Vocial: {self.vocial.main(message,testing=False)}\n"
            self.chat_widget.add_message(responsething)


def main():
    app = ChatApp(sys.argv)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()