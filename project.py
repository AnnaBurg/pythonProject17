from datetime import datetime
import pyaudio
import wave
import sqlite3
import sys
import pandas as pd


from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog
from PyQt6.QtCore import QTimer
from pathlib import Path


# chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
ropen = True
chunk = int(RATE / 20)
p = pyaudio.PyAudio()


def start():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print(i, p.get_device_info_by_index(i)['name'])


class MyWidget(QMainWindow):
    filenamea = 'EMPTY'
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=chunk)
    stream.close()

    all = []
    aux = []
    flagaudio = True
    flagrecord = False
    flag = False

    def __init__(self):
        super().__init__()
        uic.loadUi('myproject.ui', self)
        self.pushButton.clicked.connect(self.rec)
        self.pushButton_2.clicked.connect(self.pause)
        self.pushButton_4.clicked.connect(self.cont)
        self.pushButton_3.clicked.connect(self.stop)
        self.con = sqlite3.connect('audio.sqlite')
        self.time_elapsed = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.action_3.triggered.connect(self.export_file)
        self.filters = 'Text Files (*.txt)'
        self.path = None

    def start_stop_timer(self):
        if not self.timer.isActive():
            self.timer.start(1000)
        else:
            self.timer.stop()

    def update_time(self):
        self.time_elapsed += 1
        hours = self.time_elapsed // 3600
        minutes = (self.time_elapsed % 3600) // 60
        seconds = self.time_elapsed % 60

        self.lineEdit.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def rec(self):
        print("REC")
        if self.filenamea == 'EMPTY':
            self.filenamea = datetime.now().strftime("%Y-%m-%d_%H_%M_%S.wav")
            self.flagaudio = True
            self.flagrecord = True
            self.stream = p.open(format=FORMAT,
                                 channels=CHANNELS,
                                 rate=RATE,
                                 input=True,
                                 frames_per_buffer=chunk)
            self.stream.start_stream()
            self.time_elapsed = 0
            self.start_stop_timer()
            self.recorder()

    def pause(self):
        print("PAUSE")
        if self.filenamea != 'EMPTY':
            self.flagrecord = False
            self.start_stop_timer()

    def cont(self):
        print("CONT")
        if self.filenamea != 'EMPTY':
            self.flagrecord = True
            self.start_stop_timer()
            self.stream.start_stream()

    def stop(self):
        print("STOP")
        if self.filenamea != 'EMPTY':
            self.flagaudio = False
            self.start_stop_timer()
            self.update_time()
            self.stream.close()
            print(self.filenamea)
            self.all += self.aux
            datas = b''.join(self.all)
            wf = wave.open(self.filenamea, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(datas)
            wf.close()
            print("stop")
            text, ok_pressed = QInputDialog.getMultiLineText(self, "Описание",
                                                             "Введите описание к аудиозаписи")
            if ok_pressed:
                self.insert_db(self.filenamea, text)
            self.filenamea = 'EMPTY'

    def recorder(self):
        print("RECORDER")
        while self.flagaudio:

            if self.flagrecord:
                print("->REC")
                data = self.stream.read(chunk)
                self.aux.append(data)
                self.update_time()
            else:
                print("->PAUSE")
                if self.flagaudio:
                    self.all += self.aux
                    del self.aux[:]
                    data = 0
                    self.stream.stop_stream()
                else:
                    pass
            QApplication.processEvents()
            if self.flagaudio == False:
                break

    def insert_db(self, name, t):
        data = self.con.execute("SELECT MAX(id) FROM AUDIO")
        new_id = 0
        for row in data:
            new_id = row[0] + 1
            break
        sql = "INSERT INTO AUDIO (id, name, description) VALUES (" + str(new_id) + ",'" + name + "', '" + t + "' )"
        self.con.execute(sql)
        self.con.execute('commit')

    def closeEvent(self, event):
        self.con.close()

    def export_file(self):
        print('export')

        filename, _ = QFileDialog.getSaveFileName(
            self, 'Save File', filter=self.filters
        )

        if not filename:
            return

        self.path = Path(filename)
        self.path.write_text(str(pd.read_sql("SELECT * FROM AUDIO", self.con)))


def main():
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    app.exec()
    p.terminate()
    print('End')


if __name__ == '__main__':
    main()
