from datetime import datetime
import json
from pathlib import Path


class Data_Logger:
    def __init__(self):
        self.output_dir = Path(__file__).resolve().parent / "promptrecords"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.start = datetime.now()
        self.main_data = None
        self.file = None

    def init_main_data(self, subject_info):
        self.close_logger()
        self.start = datetime.now()
        self.subject_id = subject_info["subject_id"]
        stem = f"Subject{self.subject_id}-{self.start:%Y-%m-%d_%H-%M-%S}"
        self.txt_path = self.output_dir / f"{stem}.txt"
        self.json_path = self.output_dir / f"{stem}.json"
        self.file = self.txt_path.open("x", encoding="utf-8")
        self.file.write(
            f"被试编号: {self.subject_id} | 姓名（英文）: {subject_info['subject_name']} | 年龄: {subject_info['age']} | "
            f"CDR等级: {subject_info['cdr']} | 性别: {subject_info['gender']}\n"
        )
        self.file.flush()
        self.main_data = {
            "session": {
                **subject_info,
                "start_time": self.start.isoformat(timespec="milliseconds"),
                "sampling_rate": 500,
            },
            "events": [],
        }

    def add_event(self, event_type, **kwargs):
        if self.main_data is None:
            return
        now = datetime.now()
        event = {
            "time": now.isoformat(timespec="milliseconds"),
            "elapsed_seconds": round((now - self.start).total_seconds(), 3),
            "type": event_type,
            **kwargs,
        }
        if isinstance(event_type, dict) and event_type.get("type") == "trial pause":
            event.update(event_type)
        self.main_data["events"].append(event)

    def save(self):
        with self.json_path.open("w", encoding="utf-8") as file:
            json.dump(self.main_data, file, indent=4, ensure_ascii=False)

    def write_message(self, msg: str):
        if self.file is None:
            return
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S.%f")[:-3]
        elapsed_s = (now - self.start).total_seconds()
        if msg.endswith(" experiment started."):
            self.file.write("\n")
        self.file.write(f"[{timestamp}] [+{elapsed_s:8.3f}s] {msg}\n")
        self.file.flush()

    def close_logger(self):
        if self.file is not None:
            self.file.close()
            self.file = None
