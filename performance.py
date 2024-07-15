from datetime import datetime

class Performance():
    def __init__(self, fpath):
        self.fpath = fpath
        
    def log(self, g):
        with open(self.fpath, "a") as f:
            uuid = g.uuid
            status_code = g.status_code
            response_time = (g.end-g.start)*1000
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {uuid}, {status_code}, {response_time:.3f}\n")
        