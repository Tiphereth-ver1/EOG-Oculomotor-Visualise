import datetime

class Data_Logger:
    def __init__(self):
        self.start = datetime.datetime.now()
        filename = self.start.strftime("%Y-%m-%d_%H-%M-%S.txt")

        self.file = open(filename, "w")
        if self.file == None:
            raise FileNotFoundError(f"The logging file could not be created.")
        
    def write_message(self, msg: str):
        now = datetime.datetime.now()
        elapsed = now - self.start

        timestamp = now.strftime("%H:%M:%S.%f")[:-3]  # HH:MM:SS.mmm
        elapsed_s = elapsed.total_seconds()

        self.file.write(
            f"[{timestamp}] [+{elapsed_s:8.3f}s] {msg}\n"
        )
        self.file.flush()

    def close_logger(self):
        self.file.close()