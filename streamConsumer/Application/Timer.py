import time


class Timer:
    def __init__(self, message: str):
        self.message = message

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_time = time.time() - self.start_time
        print(f"{self.message}. Time elapsed: {elapsed_time:.2f} seconds")
