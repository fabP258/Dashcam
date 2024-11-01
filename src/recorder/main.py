import time
from recorder.runner import Runner

if __name__ == "__main__":
    runner = Runner()
    runner.start()
    time.sleep(60)
    runner.stop()
