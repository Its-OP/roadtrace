import cv2
import keras
import numpy as np
import tensorflow as tf
from numpy.compat import long

from entities import Vehicle, Region
from services.BaseService import BaseService, Frame


class _ChannelValue:
    val = -1.0
    intensity = -1.0


class ColorInferenceService(BaseService[str]):
    color_codes = {0: 'black', 1: 'blue', 2: 'cyan', 3: 'gray', 4: 'green', 5: 'red', 6: 'white', 7: 'yellow'}

    def __init__(self, color_picker_model: keras.Sequential):
        self._model = color_picker_model

    def _update_vehicle(self, vehicle: Vehicle, feature: str):
        vehicle.color = feature

    def _extract_feature(self, region: Region, preprocessed_frame: Frame) -> str | None:
        tensor = preprocessed_frame.reshape((1, 100, 100, 3))
        prediction_tensor = self._model(tensor)
        color_code: int = int(tf.argmax(prediction_tensor, axis=1).numpy()[0])
        color_conf: float = prediction_tensor.numpy()[0][color_code]
        return self.color_codes[color_code] if color_conf > 0.8 else None

    def _preprocess_frame(self, frame: Frame) -> np.ndarray:
        rescaled_frame = cv2.resize(frame, (100, 100), interpolation=cv2.INTER_AREA)
        light_intensity = self.__get_atmospheric_light_intensity(rescaled_frame)
        return self.__dehaze(rescaled_frame, light_intensity)

    def _should_process_vehicle(self, vehicle: Vehicle) -> bool:
        return vehicle.color is None

    def __get_atmospheric_light_intensity(self, img: np.ndarray) -> float:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        top_num = int(img.shape[0] * img.shape[1] * 0.001)
        top_list = [_ChannelValue()] * top_num
        dark_channel = self.__find_dark_channel(img)

        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                val = img.item(y, x, dark_channel)
                intensity = gray.item(y, x)
                for t in top_list:
                    if t.val < val or (t.val == val and t.intensity < intensity):
                        t.val = val
                        t.intensity = intensity
                        break
        max_channel = _ChannelValue()
        for t in top_list:
            if t.intensity > max_channel.intensity:
                max_channel = t
        return max_channel.intensity

    # Finding the dark channel i.e. the pixel with the lowest R/G/B value
    @staticmethod
    def __find_dark_channel(img: np.ndarray) -> long:
        return np.unravel_index(np.argmin(img), img.shape)[2]

    # Finding a coarse image which gives us a transmission map
    @staticmethod
    def __coarse(minimum, x, maximum):
        return max(minimum, min(x, maximum))

    # Uses values from other functions to aggregate and give us a clear image
    def __dehaze(self, img: np.ndarray, light_intensity: float, window_size=20, t0=0.55, w=0.95) -> np.ndarray:
        size = (img.shape[0], img.shape[1])

        out_img = np.zeros(img.shape, img.dtype)

        for y in range(size[0]):
            for x in range(size[1]):
                x_low = max(x - (window_size // 2), 0)
                y_low = max(y - (window_size // 2), 0)
                x_high = min(x + (window_size // 2), size[1])
                y_high = min(y + (window_size // 2), size[0])

                slice_img = img[y_low:y_high, x_low:x_high]

                dark_channel = self.__find_dark_channel(slice_img)
                t = 1.0 - (w * img.item(y, x, dark_channel) / light_intensity)

                out_img.itemset((y, x, 0), self.__coarse(0, ((img.item(y, x, 0) - light_intensity) /
                                                             max(t, t0) + light_intensity), 255))
                out_img.itemset((y, x, 1), self.__coarse(0, ((img.item(y, x, 1) - light_intensity) /
                                                             max(t, t0) + light_intensity), 255))
                out_img.itemset((y, x, 2), self.__coarse(0, ((img.item(y, x, 2) - light_intensity) /
                                                             max(t, t0) + light_intensity), 255))
        return out_img
