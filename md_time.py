from datetime import datetime, timedelta
import time

class MD_time:
    """A class for hand time for motion detection"""
    def __init__(self, md):
        """Initialize time attributes"""
        self.settings = md.settings
        self.time_limit = timedelta(minutes=self.settings.timelimit.minute)

    def time_range(self):
        """Check now if in the time range"""
        self.dt = datetime.now()
        self.start_time = self.dt.replace(
            hour=self.settings.time_range.start_time.hour,
            minute=self.settings.time_range.start_time.minute
            )
        self.end_time = self.dt.replace(
            hour=self.settings.time_range.end_time.hour,
            minute=self.settings.time_range.end_time.minute
            )
        if self.dt > self.start_time and self.dt < self.end_time:
            return True
        else: return False

    def sleep_time(self, minute=1):
        """Get the program wait for a time"""
        time.sleep(minute * 60)