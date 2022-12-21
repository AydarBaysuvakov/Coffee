import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyExeption(Exception):
    pass

class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect('coffee.sqlite')
        self.select_data()

    def select_data(self):
        res = self.connection.cursor().execute("""SELECT Coffee.ID, Coffee.name, Roast.degree, 
        type.type, Coffee.taste, Coffee.coast, Coffee.volume FROM Coffee INNER JOIN Roast 
        ON Coffee.Roast_Degree = roast.id INNER JOIN type ON Coffee.type = type.id""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())