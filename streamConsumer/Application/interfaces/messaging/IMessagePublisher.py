import queue
import threading
import time
from abc import ABC, abstractmethod

from Application.interfaces.messaging.IMessage import IMessage


class IMessagePublisher(ABC, threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._message_queue: queue.Queue[IMessage] = queue.Queue()
        self._stop_signal = threading.Event()
        self._is_active = True

    @abstractmethod
    def run(self) -> None:
        pass

    def send_message(self, message: IMessage):
        if self._is_active:
            self._message_queue.put(message)

    def stop(self):
        # Stop accepting new messages
        self._is_active = False

        # Wait for the message queue to be emptied
        while not self._message_queue.empty():
            time.sleep(0.1)

        # Signal the thread to stop
        self._stop_signal.set()
