from datetime import datetime
import json

class Data_Logger:
    def __init__(self):
        self.start = datetime.now()
        filename = self.start.strftime("%Y-%m-%d_%H-%M-%S.txt")
        self.subject_id = 000

        self.main_data = None

        self.file = open(filename, "w")
        if self.file == None:
            raise FileNotFoundError(f"The logging file could not be created.")
        
    def init_main_data(self):
        self.main_data  = {
            "session": {
                "subject_id": self.subject_id,
                "start_time": datetime.now().isoformat(timespec="milliseconds"),
                "sampling_rate": 500
            },
            "events": []
        }
        self.subject_id += 1

    def add_event(self, event_type, **kwargs):
        print("event added")
        now = datetime.now()
        elapsed = now - self.start
        elapsed_seconds = elapsed.total_seconds()
        event = {
            "time": datetime.now().isoformat(timespec="milliseconds"),
            "elapsed_seconds": round(elapsed_seconds, 3),
            "type": event_type,
            **kwargs
        }

        self.main_data["events"].append(event)

    def save(self):
        timestamp = self.main_data["session"]["start_time"]
        timestamp = timestamp.replace(":", "-")

        with open(f"({self.subject_id}) - {timestamp}.json", "w") as f:
            json.dump(
                self.main_data,
                f,
                indent=4
            )
    
    def write_message(self, msg: str, time : str):
        now = datetime.now()
        elapsed = now - self.start

        timestamp = now.strftime("%H:%M:%S.%f")[:-3]  # HH:MM:SS.mmm
        elapsed_s = elapsed.total_seconds()



        self.file.write(
            f"Formerly [{time}] [{timestamp}] [+{elapsed_s:8.3f}s] {msg}\n"
        )
        self.file.flush()

    def close_logger(self):
        self.file.close()