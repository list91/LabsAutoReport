import os.path
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit
import os
import docx
import gpt
from wordCreater import create

# def getCodeTXT(path_to_file):
#     with open(path_to_file, 'r') as f:
#         script = f.read()
#     return script

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.text_lab_number = None
        self.combo_select = None
        self.text_task = None
        self.text_language_input = None  # - создаем новый атрибут для поля ввода языка программирования
        self.text_task_input = None
        self.title = 'Автоотчет'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Заголовок
        label_title = QLabel('Автоотчет', self)
        label_title.move(10, 10)

        # Поле для ввода языка программирования
        label_language = QLabel('Язык программирования:', self)
        label_language.move(10, 50)

        self.text_language_input = QLineEdit(self) # Присваиваем значение, введённое пользователем, атрибуту text_language_input
        self.text_language_input.move(200, 50)
        self.text_language_input.resize(280, 20)


        # Поле для ввода задания
        label_task = QLabel('Задание:', self)
        label_task.move(10, 80)

        self.text_task_input = QLineEdit(self)
        self.text_task_input.move(200, 80)
        self.text_task_input.resize(280, 20)

        # Поле с выбором из списка
        label_select = QLabel('Выбор:', self)
        label_select.move(10, 110)

        self.combo_select = QComboBox(self)
        self.combo_select.addItem('Скурыдина Е. М.')
        self.combo_select.addItem('-пусто-')
        # combo_select.addItem('Вариант 3')
        self.combo_select.move(200, 110)
        self.combo_select.resize(200, 20)

        # Поле для ввода номера лабораторной работы
        label_lab_number = QLabel('Номер лабораторной:', self)
        label_lab_number.move(10, 140)

        self.text_lab_number = QLineEdit(self)
        self.text_lab_number.move(200, 140)
        self.text_lab_number.resize(80, 20)

        # Кнопка для запуска
        button_run = QPushButton('Запуск', self)
        button_run.setToolTip('Нажмите, чтобы запустить скрипт')
        button_run.move(10, 170)
        button_run.resize(80, 30)
        button_run.clicked.connect(self.run_script)


        # Окно для вывода информации
        label_output = QLabel('Вывод:', self)
        label_output.move(10, 210)

        self.text_output = QTextEdit(self, readOnly=True)
        self.text_output.move(10, 230)
        self.text_output.resize(480, 60)

        self.show()

    def run_script(self):
        self.text_output.setText("START")

        task = self.text_task_input.text() # получаем текст из поля ввода задачи

        lang = self.text_language_input.text() # получаем текст из поля ввода языка программирования

        code = gpt.generate_promt(f"{task}\nРеши данную задачу на языке {lang}. Верни результат в виде кода", gpt.History().get_dict())

        algorithm = gpt.generate_promt(f"{code}\nПриведи алгоритм данного кода.", gpt.History().get_dict())

        gpt.History().clear()

        print("algorithm - OK")

        code_output = gpt.generate_promt(f"{code}\nВыведи результат кода.", gpt.History().get_dict())

        gpt.History().clear()

        print("code_output FINISH")

        output = gpt.generate_promt(f"{code}\nНа основе данного кода составь вывод для отчета.",gpt.History().get_dict())
        print("output FINISH")
        config = {
            "num_lab": self.text_lab_number.text(),
            "student": "Ануфриев С. В.",
            "master": self.combo_select.currentText(),
            "task": task,
            "scheme": "NULL",
            "lang": lang,
            "algorithm": algorithm,
            "code": code,
            "code_output": code_output,
            "output": output,
        }
        name = f"lab{self.text_lab_number.text()}_{lang}.docx"
        if os.path.isfile(name):
            os.remove(name)
        create(name, config)
        msg = f"Отчет успешно создан в файле {name}"
        print(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
