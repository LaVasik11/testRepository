import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          task_text TEXT,
                          importance TEXT,
                          task_date TEXT,
                          task_note TEXT)''')
        self.conn.commit()

    def add_task_to_db(self, task_text, task_importance, task_date, task_note):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tasks (task_text, importance, task_date, task_note) VALUES (?, ?, ?, ?)",
                       (task_text, task_importance, task_date, task_note))
        self.conn.commit()

    def remove_task_from_db(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def get_tasks_from_db(self, sort_by_importance=True):
        cursor = self.conn.cursor()
        if sort_by_importance:
            cursor.execute("SELECT * FROM tasks ORDER BY importance DESC")
        else:
            cursor.execute("SELECT * FROM tasks ORDER BY task_date DESC")
        return cursor.fetchall()


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(403, 297)

        self.tasks = []

        self.stackedWidget = QtWidgets.QStackedWidget(Dialog)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 10, 381, 281))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.text_task = QtWidgets.QTextEdit(self.page)
        self.text_task.setGeometry(QtCore.QRect(0, 170, 381, 111))
        self.text_task.setObjectName("textEdit")
        self.dateEdit = QtWidgets.QDateEdit(self.page)
        self.dateEdit.setGeometry(QtCore.QRect(120, 30, 111, 31))
        self.dateEdit.setObjectName("dateEdit")
        self.task = QtWidgets.QLabel(self.page)
        self.task.setGeometry(QtCore.QRect(0, 140, 381, 21))
        self.task.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.task.setAlignment(QtCore.Qt.AlignCenter)
        self.task.setObjectName("label_3")
        self.importance_comboBox = QtWidgets.QComboBox(self.page)
        self.importance_comboBox.setGeometry(QtCore.QRect(120, 70, 111, 31))
        self.importance_comboBox.setObjectName("comboBox")
        self.importance_comboBox.addItem("")
        self.importance_comboBox.addItem("")
        self.importance_comboBox.addItem("")
        self.importance_comboBox.addItem("")
        self.importance = QtWidgets.QLabel(self.page)
        self.importance.setGeometry(QtCore.QRect(10, 70, 101, 31))
        self.importance.setObjectName("label")
        self.term = QtWidgets.QLabel(self.page)
        self.term.setGeometry(QtCore.QRect(10, 30, 101, 31))
        self.term.setObjectName("label_2")
        self.add_task = QtWidgets.QPushButton(self.page)
        self.add_task.setGeometry(QtCore.QRect(10, 110, 221, 31))
        self.add_task.setObjectName("pushButton")
        self.note_text = QtWidgets.QPlainTextEdit(self.page)
        self.note_text.setGeometry(QtCore.QRect(250, 70, 121, 71))
        self.note_text.setObjectName("plainTextEdit")
        self.note = QtWidgets.QLabel(self.page)
        self.note.setGeometry(QtCore.QRect(250, 20, 111, 21))
        self.note.setAlignment(QtCore.Qt.AlignCenter)
        self.note.setObjectName("label_6")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.task_list = QtWidgets.QListWidget(self.page_2)
        self.task_list.setGeometry(QtCore.QRect(10, 60, 371, 211))
        self.task_list.setObjectName("listWidget")
        self.sort_by = QtWidgets.QLabel(self.page_2)
        self.sort_by.setGeometry(QtCore.QRect(20, 30, 121, 16))
        self.sort_by.setAlignment(QtCore.Qt.AlignCenter)
        self.sort_by.setObjectName("label_4")
        self.sort_by_date = QtWidgets.QRadioButton(self.page_2)
        self.sort_by_date.setGeometry(QtCore.QRect(240, 30, 111, 17))
        self.sort_by_date.setObjectName("radioButton")
        self.sort_by_importance = QtWidgets.QRadioButton(self.page_2)
        self.sort_by_importance.setGeometry(QtCore.QRect(150, 30, 82, 17))
        self.sort_by_importance.setObjectName("radioButton_2")
        self.task_list_label = QtWidgets.QLabel(self.page_2)
        self.task_list_label.setGeometry(QtCore.QRect(70, 0, 231, 20))
        self.task_list_label.setAlignment(QtCore.Qt.AlignCenter)
        self.task_list_label.setObjectName("label_5")
        self.stackedWidget.addWidget(self.page_2)
        self.add_task.clicked.connect(self.add_task_to_list)
        self.dateEdit.setDate(QtCore.QDate.currentDate())

        self.retranslateUi(Dialog)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.sort_by_importance.clicked.connect(self.sort_tasks_by_importance)
        self.sort_by_date.clicked.connect(self.sort_tasks_by_date)

        self.remove_task_button = QtWidgets.QPushButton(self.page_2)
        self.remove_task_button.setGeometry(QtCore.QRect(250, 0, 125, 23))
        self.remove_task_button.setObjectName("remove_task_button")
        self.remove_task_button.setText("Удалить задачу")
        self.remove_task_button.clicked.connect(self.remove_task)


        self.pushButton_task_list = QtWidgets.QPushButton(self.page)
        self.pushButton_task_list.setGeometry(QtCore.QRect(10, 0, 221, 21))
        self.pushButton_task_list.setObjectName("pushButton_next")
        self.pushButton_task_list.setText("Список задач")
        self.pushButton_task_list.clicked.connect(self.switchToPage2)

        self.pushButton_add_task = QtWidgets.QPushButton(self.page_2)
        self.pushButton_add_task.setGeometry(QtCore.QRect(10, 0, 125, 23))
        self.pushButton_add_task.setObjectName("pushButton_back")
        self.pushButton_add_task.setText("Добавление задачи")
        self.pushButton_add_task.clicked.connect(self.switchToPage1)


        self.importance_map = {
            "Очень важно": 3,
            "Важно": 2,
            "Среднее": 1,
            "Не важно": 0
        }

    def switchToPage1(self):
        self.stackedWidget.setCurrentIndex(0)

    def switchToPage2(self):
        self.stackedWidget.setCurrentIndex(1)
        self.update_task_list()



    def remove_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            row = self.task_list.row(selected_item)
            self.task_list.takeItem(row)
            del self.tasks[row]


    def sort_tasks_by_importance(self):
        try:
            self.tasks.sort(key=lambda task: self.importance_map.get(self.get_importance(task), 0), reverse=True)
            self.update_task_list()
        except Exception as e:
            print("Error sorting by importance:", e)

    def get_importance(self, task):
        parts = task.split('Важность: ')
        if len(parts) > 1:
            importance_str = parts[1].split(',')[0]
            return importance_str.strip()
        return ""

    def sort_tasks_by_date(self):
        try:
            self.tasks.sort(
                key=lambda task: QtCore.QDate.fromString(task.split('Срок выполнения: ')[1], 'dd/MM/yyyy'),
                reverse=True)
            self.update_task_list()
        except Exception as e:
            print("Error sorting by date:", e)


    def add_task_to_list(self):
        task_text = self.text_task.toPlainText()
        task_importance = self.importance_comboBox.currentText()
        task_date = self.dateEdit.date().toString('dd/MM/yyyy')
        task_note = self.note_text.toPlainText()

        task = f"Задача: {task_text}, Примичание: {task_note}, Важность: {task_importance}, Срок выполнения: {task_date}"

        if task not in self.tasks:
            self.tasks.append(task)
            self.update_task_list()
            self.text_task.clear()
            self.importance_comboBox.setCurrentIndex(0)
            self.dateEdit.setDate(QtCore.QDate.currentDate())
            self.note_text.clear()

    def update_task_list(self):
        self.task_list.clear()
        self.task_list.addItems(self.tasks)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "task manager"))
        self.task.setText(_translate("Dialog", "Задача:"))
        self.importance_comboBox.setItemText(0, _translate("Dialog", "Очень важно"))
        self.importance_comboBox.setItemText(1, _translate("Dialog", "Важно"))
        self.importance_comboBox.setItemText(2, _translate("Dialog", "Среднее"))
        self.importance_comboBox.setItemText(3, _translate("Dialog", "Не важно"))
        self.importance.setText(_translate("Dialog", "Важность задачи:"))
        self.term.setText(_translate("Dialog", "Срок выполнения:"))
        self.add_task.setText(_translate("Dialog", "Добавть задачу"))
        self.note.setText(_translate("Dialog", "Примичание"))
        self.sort_by.setText(_translate("Dialog", "Сортировать по:"))
        self.sort_by_date.setText(_translate("Dialog", "Дате выполнения"))
        self.sort_by_importance.setText(_translate("Dialog", "Важносте"))
        self.task_list_label.setText(_translate("Dialog", "Список заданий"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
