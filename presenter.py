import sys
import threading
import time
from datetime import datetime, timedelta

from PyQt5 import QtWidgets, QtCore, QtGui

import view
import timer


class Presenter:
    def __init__(self, view_: view.View):
        self.view = view_
        self.update_time = None
        self.timer = 0
        self.t = None

    def set_default_style(self):
        """Set button back to 'Start' after timer is finished"""
        self.view.timer_button.active = False

    def timer_button_clicked(self, active):
        if active is False:   # Start
            self.start_timer()
        else:  # Cancel
            self.t.stop()

    def start_timer(self):
        if timer.isActive is False:
            timer.isActive = True
            self.view.dial.setDisabled(True)
            self.t = timer.MyTimer(self.view.hours, self.view.minutes, self.view.seconds, self.view.dial, self.set_default_style)
            self.t.start()

    def dial_moved(self, value):
        self.timer = value
        if self.timer < 60:
            self.view.minutes.setText(str(self.timer))
            self.view.hours.setText("0")
        elif self.timer < 60 * 8:  # timer limit is 8 hours - it's timer for studying / working so it doesn't need more
            hours = int(self.timer / 60)
            minutes = int(self.timer % 60)
            self.view.hours.setText(str(hours))
            self.view.minutes.setText(str(minutes))
        else:
            self.timer = 0

    def set_current_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        week_day = datetime.today().strftime('%A')
        self.view.time_label.setText(current_time)
        self.view.day_label.setText(week_day)

    def set_timer(self):
        """Wait till another minute and start repeated timer with 60 seconds interval"""
        time.sleep(60.0 - (time.time() % 60))

        self.set_current_time()  # set new time and...
        self.update_time = RepeatedTimer(timedelta(seconds=60), self.set_current_time)  # set repeated timer with 60s interval
        self.update_time.start()

    def show(self):
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon('Graphic/timer_icon.png'))
        MainWindow = QtWidgets.QMainWindow()
        self.view.setup(MainWindow)

        self.set_current_time()
        t = threading.Thread(target=self.set_timer)
        t.daemon = True  # kill this thread when main thread is killed
        t.start()

        MainWindow.show()
        sys.exit(app.exec_())


class RepeatedTimer(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)

        self.daemon = True  # True: if the main thread is killed this thread will be killed too
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            try:
                self.execute(*self.args, **self.kwargs)
            except RuntimeError:
                """This exception is rised when progrem is closed"""
                self.stopped.set()


