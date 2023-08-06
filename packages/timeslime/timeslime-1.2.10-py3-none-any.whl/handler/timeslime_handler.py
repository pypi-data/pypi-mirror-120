from datetime import datetime, timedelta
from requests.exceptions import ConnectionError

from timeslime.model import Timespan
from timeslime.handler import DatabaseHandler, TimeslimeServerHandler, NtpServerHandler

class TimeslimeHandler():
    def __init__(self, daily_working_time, database_handler: DatabaseHandler, ntp_server_handler: NtpServerHandler, timeslime_server_handler: TimeslimeServerHandler = None):
        self.daily_working_time = daily_working_time
        self.database_handler = database_handler
        self.ntp_server_handler = ntp_server_handler
        self.timeslime_server_handler = timeslime_server_handler
        self.timespan = self.database_handler.get_recent_timespan()
        self.on_start = None
        self.on_stop = None

    def start_time(self):
        if not self.ntp_server_handler.ntp_server_is_synchronized:
            print('NTP server is not synchronized yet. Wait a few seconds to get an accurate time tracking.')
            return
        self.stop_time()
        self.timespan = Timespan()
        self.timespan.start_time = datetime.now()
        self.database_handler.save_timespan(self.timespan)
        if self.timeslime_server_handler is not None:
            try:
                self.timeslime_server_handler.send_timespan(self.timespan)
            except ConnectionError:
                pass
        if self.on_start is not None:
            self.on_start()

    def stop_time(self):
        if not self.ntp_server_handler.ntp_server_is_synchronized:
            print('NTP server is not synchronized yet. Wait a few seconds to get an accurate time tracking.')
            return
        if self.timespan is not None and self.timespan.start_time is not None and self.timespan.stop_time is None:
            self.timespan.stop_time = datetime.now()
            self.database_handler.save_timespan(self.timespan)
            if self.timeslime_server_handler is not None:
                try:
                    self.timeslime_server_handler.send_timespan(self.timespan)
                except ConnectionError:
                    pass
        if self.on_stop is not None:
            self.on_stop()

    def get_elapsed_time(self) -> bool:
        if not self.ntp_server_handler.ntp_server_is_synchronized:
            print('NTP server is not synchronized yet. Wait a few seconds to get an accurate time tracking.')
            return
        daily_sum_in_seconds = self.database_handler.get_tracked_time_in_seconds()
        current_timedelta = timedelta(seconds=0)
        if self.timespan is not None and self.timespan.stop_time is None:
            current_timedelta = datetime.now() - self.timespan.start_time
        return self.daily_working_time - daily_sum_in_seconds - current_timedelta

    def is_running(self):
        if self.database_handler.get_recent_timespan() is not None:
            return True
        else:
            return False
