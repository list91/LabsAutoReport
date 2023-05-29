import os

import docx


def create(name, config):
    original_docx = 'maket.docx'
    copy_docx = name
    os.system(f'cp {original_docx} {copy_docx}')
    doc = docx.Document(copy_docx)
    for para in doc.paragraphs:
        if "$НОМЕР_ЛАБ$" in para.text:
            para.text = para.text.replace("$НОМЕР_ЛАБ$", config["num_lab"])
        if "$СТУДЕНТ$" in para.text:
            para.text = para.text.replace("$СТУДЕНТ$", config["student"])
        if "$ПРЕПОДАВАТЕЛЬ$" in para.text:
            para.text = para.text.replace("$ПРЕПОДАВАТЕЛЬ$", config["master"])
        if "$ЗАДАНИЕ$" in para.text:
            para.text = para.text.replace("$ЗАДАНИЕ$", config["task"])
        if "$СХЕМА$" in para.text:
            para.text = para.text.replace("$СХЕМА$", config["scheme"])
        if "$ЯЗЫК_ПРОГРАММИРОВАНИЯ$" in para.text:
            para.text = para.text.replace("$ЯЗЫК_ПРОГРАММИРОВАНИЯ$", config["lang"])
        if "$АЛГОРИТМ$" in para.text:
            para.text = para.text.replace("$АЛГОРИТМ$", config["algorithm"])
        if "$КОД$" in para.text:
            para.text = para.text.replace("$КОД$", config["code"])
        if "$ВЫВОД_КОДА$" in para.text:
            para.text = para.text.replace("$ВЫВОД_КОДА$", config["code_output"])
        if "$ВЫВОД$" in para.text:
            para.text = para.text.replace("$ВЫВОД$", config["output"])

    doc.save(copy_docx)