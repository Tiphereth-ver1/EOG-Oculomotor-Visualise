from datetime import datetime
import json

class Data_Logger:
    def __init__(self):
        self.start = datetime.now()
        filename = self.start.strftime("%Y-%m-%d_%H-%M-%S.txt")  # 《《《《《《《《《《《文本日志命名格式，输出到启动工作目录，程序初始化即创建
        self.subject_id = 000  # 《《《《《《《《《《《初始受试者编号，000等于0，目前只在内存中递增

        self.main_data = None

        self.file = open(filename, "w")
        if self.file == None:
            raise FileNotFoundError(f"The logging file could not be created.")
        
    def init_main_data(self):
        self.main_data  = {
            "session": {
                "subject_id": self.subject_id,
                "start_time": datetime.now().isoformat(timespec="milliseconds"),
                "sampling_rate": 500  # 《《《《《《《《《《《采样率元数据Hz，不设置硬件采样率，也不代表已采集EOG数据
            },
            "events": []
        }
        self.subject_id += 1  # 《《《《《《《《《《《会话初始化后编号加1，所以文件名比session.subject_id大1

    def add_event(self, event_type, **kwargs):
        print("event added")
        now = datetime.now()
        elapsed = now - self.start
        elapsed_seconds = elapsed.total_seconds()
        event = {
            "time": datetime.now().isoformat(timespec="milliseconds"),
            "elapsed_seconds": round(elapsed_seconds, 3),  # 《《《《《《《《《《《相对日志器创建时刻的经过秒数，保留3位小数，不是每轮重新计时
            "type": event_type,  # 《《《《《《《《《《《当前调用方传入字典，所以type字段保存整个事件对象
            **kwargs
        }

        self.main_data["events"].append(event)

    def save(self):
        print()
        with open(f"{self.subject_id}.json", "w") as f:  # 《《《《《《《《《《《JSON保存路径及命名入口，同名文件会覆盖
            json.dump(
                self.main_data,
                f,
                indent=4  # 《《《《《《《《《《《JSON缩进空格数，仅影响排版
            )
    
    def write_message(self, msg: str):
        now = datetime.now()
        elapsed = now - self.start

        timestamp = now.strftime("%H:%M:%S.%f")[:-3]  # HH:MM:SS.mmm
        elapsed_s = elapsed.total_seconds()

        self.file.write(
            f"[{timestamp}] [+{elapsed_s:8.3f}s] {msg}\n"
        )
        self.file.flush()

    def close_logger(self):
        self.file.close()
