from abc import ABC, abstractmethod
import cv2


class IVideoProcessor(ABC):
    @abstractmethod
    def start_processing(self, cap: cv2.VideoCapture):
        pass
