


from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import pyaudio
import numpy as np
import pylab
import time
import sys
import matplotlib.pyplot as plt


class AudioPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Audio Player')

        self.play = QPushButton('Play', self)
        self.play.move(50, 50)
        self.play.clicked.connect(self.start)

        self.pause = QPushButton('Pause', self)
        self.pause.move(150, 50)

        self.stop = QPushButton('Stop', self)
        self.stop.move(250, 50)

    def start(self):
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            print(i, p.get_device_info_by_index(i)['name'])

        RATE = 44100
        CHUNK = int(RATE / 20)

        def soundplot(stream):

            t1 = time.time()
            # use np.frombuffer if you face error at this line
            data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
            print(data)

        if __name__ == "__main__":
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
            for i in range(sys.maxsize ** 10):
                soundplot(stream)
            stream.stop_stream()
            stream.close()
            p.terminate()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()
    sys.exit(app.exec())

# import sys
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
# from PyQt6.QtMultimedia import QA
# f
#
#
# class Dictaphone(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.recorder = QAudioRecorder()
#
#         self.record_button = QPushButton("Record")
#         self.record_button.clicked.connect(self.start_recording)
#
#         self.stop_button = QPushButton("Stop")
#         self.stop_button.clicked.connect(self.stop_recording)
#
#         self.play_button = QPushButton("Play")
#         self.play_button.clicked.connect(self.play_recording)
#
#         self.status_label = QLabel("Status: Ready")
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.record_button)
#         layout.addWidget(self.stop_button)
#         layout.addWidget(self.play_button)
#         layout.addWidget(self.status_label)
#
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#
#     def start_recording(self):
#         self.recorder.setOutputLocation(QUrl("output.wav"))
#         self.recorder.record()
#         self.status_label.setText("Status: Recording")
#
#     def stop_recording(self):
#         self.recorder.stop()
#         self.status_label.setText("Status: Recording stopped")
#
#     def play_recording(self):
#         self.recorder.setSourceLocation(QUrl("output.wav"))
#         player = QMediaPlayer()
#         player.setMedia(self.recorder)
#         player.play()
#         self.status_label.setText("Status: Playing")

#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Dictaphone()
#     window.show()
#     sys.exit(app.exec())


