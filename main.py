import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class MyExeption(Exception):
    pass

class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect('coffee.sqlite')
        self.select_data()
        self.pushButton.clicked.connect(self.add)

    def add(self):
        self.ask = Ask(self)
        self.ask.show()

    def select_data(self):
        res = self.connection.cursor().execute("""SELECT Coffee.ID, Coffee.name, Roast.degree, 
        type.type, Coffee.taste, Coffee.coast, Coffee.volume FROM Coffee INNER JOIN Roast 
        ON Coffee.Roast_Degree = roast.id INNER JOIN type ON Coffee.type = type.id""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название', 'Степень прожарки', "Тип", "Вкус", "Цена", "Объем"])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


    def closeEvent(self, event):
        self.connection.close()

class Ask(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.fillbox()
        self.pushButton.clicked.connect(self.get_info)

    def get_info(self):
        try:
            self.name = self.namele.text()
            self.roast = self.roastbox.currentText()
            self.type = self.typbox.currentText()
            self.taste = self.tastele.text()
            self.coast = int(self.coastle.text())
            self.volume = int(self.volle.text())
            self.check()
        except MyExeption:
            self.error.setText('Неверно заполнена форма')
        except ValueError:
            self.error.setText('Неверно заполнена форма')
        self.close()
        roast = self.main.connection.cursor().execute('SELECT * FROM roast').fetchall()
        for i in roast:
            if i[1] == self.roast:
                r = i[0]
        typ = self.main.connection.cursor().execute('SELECT * FROM type').fetchall()
        for i in typ:
            if i[1] == self.type:
                t = i[0]
        cur = self.main.connection.cursor()
        que = "INSERT INTO Coffee(name, Roast_Degree, type, Taste, Coast, Volume) VALUES "
        que += f"('{self.name}', {r}, '{t}', '{self.taste}', '{self.coast}', '{self.volume}')"
        cur.execute(que)
        self.main.connection.commit()
        self.main.select_data()

    def check(self):
        if self.coast < 0 or self.volume < 0:
            raise MyExeption

    def fillbox(self):
        roast = self.main.connection.cursor().execute('SELECT * FROM Roast').fetchall()
        for degree in roast:
            self.roastbox.addItem(degree[1])
        for type in ('Молотый', 'В зёрнах'):
            self.typbox.addItem(type)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())