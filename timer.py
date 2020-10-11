import threading, time, signal
from datetime import timedelta

from PyQt5 import QtWidgets

from playsound import playsound
import win10toast

from view import Dial

isActive = False   # global variable that says if timer is set


class MyTimer(threading.Thread):
    """This class count down timer and move dial back to the default position"""
    def __init__(self, hours: QtWidgets.QLabel, minutes: QtWidgets.QLabel, seconds: QtWidgets.QLabel, dial: QtWidgets.QDial, set_default):
        threading.Thread.__init__(self)
        self.counter = 0
        self.dial_controller = True
        self.fun = set_default
        self.dial = dial
        self.hours_label = hours
        self.minutes_label = minutes
        self.seconds_label = seconds
        self.seconds_label.show()
        self.hours = int(hours.text())
        self.min = int(minutes.text())
        self.sec = 59
        self.daemon = True  # True: if the main thread is killed this thread will be killed too
        self.stopped = threading.Event()
        self.interval = timedelta(seconds=1)
        self.execute = self.count_down

    def count_down(self):
        self.sec -= 1
        self.seconds_label.setText(str(self.sec))
        if self.sec == 0:
            self.sec = 59

        if self.counter == 60:
            self.min -= 1
            if self.min == -1:
                if self.hours > 0:
                    self.hours -= 1
                    self.min = 59
                    self.hours_label.setText(str(self.hours))
                else:
                    """show message time left"""
                    self.times_up()
                    self.stop()

            self.dial.setValue(self.hours * 60 + self.min)
            self.minutes_label.setText(str(self.min))
            self.counter = 0

        self.counter += 1

    def times_up(self):

        self.back_to_default()
        self.fun()
        playsound("Sounds/alarm2.mp3", False)
        toaster = win10toast.ToastNotifier()
        toaster.show_toast("Timer", "Times's up!", icon_path="Graphic/timer_icon.ico", duration=5)

    def back_to_default(self):
        global isActive
        isActive = False
        self.seconds_label.setText("59")
        self.dial.setDisabled(False)
        self.seconds_label.hide()

    def stop(self):
        self.back_to_default()
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            try:
                self.execute()
            except RuntimeError:
                """This exception is rised when progrem is closed"""
                self.stopped.set()


