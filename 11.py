import pandas as pd
import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QTableView
from PyQt6.QtSql import QSqlQueryModel

con = sqlite3.connect("audio.sqlite")

df = str(pd.read_sql("SELECT * FROM AUDIO", con))
print(df)
# sql = 'SELECT * FROM mytable'
#
# model = QSqlQueryModel()
# model.setQuery(sql, con)
#
# # Связать модель с таблицей
# table_view = QTableView()
# table_view.setModel(model)
# table_view.show()
#
# def main():
#     app = QApplication(sys.argv)
#     app.exec()
#
# if __name__ == '__main__':
#     main()
