import cv2
# import tensorflow as tf
import os
import numpy as np
from ultralytics import YOLO

def run_yolo_inference(image_path):

    model = YOLO(image_path)

    # Đọc ảnh từ đường dẫn file
    # img = cv2.imread(image_path)

    # Kiểm tra nếu ảnh đọc thành công
    # if img is None:
    #     raise ValueError(f"Cannot read image at path: {image_path}")

    # Resize ảnh nếu cần (theo yêu cầu đầu vào của mô hình YOLO)
    # img_resized = cv2.resize(img, (640, 640))

    # Xử lý inference với mô hình YOLOv8 TFLite
    # current_dir = os.path.dirname(__file__)
    # model_path = os.path.join(current_dir, "best.tflite")
    # model = tf.lite.Interpreter(model_path="D:/AppUser/AndroidStudio/TestAppServices/app/src/main/python/best.tflite")
    # interpreter.allocate_tensors()
    #
    # input_details = interpreter.get_input_details()
    # output_details = interpreter.get_output_details()
    #
    # # Chuẩn bị input cho mô hình
    # input_data = img_resized.astype(np.float32)
    # input_data = np.expand_dims(input_data, axis=0)  # Thêm chiều batch
    #
    # # Nếu mô hình yêu cầu chuẩn hóa dữ liệu, hãy thực hiện
    # input_data = input_data / 255.0  # Chia cho 255 để chuẩn hóa về [0, 1]
    #
    # interpreter.set_tensor(input_details[0]['index'], input_data)
    #
    # # Chạy mô hình
    # interpreter.invoke()
    #
    # # Lấy output
    # output_data = interpreter.get_tensor(output_details[0]['index'])
    #
    # return output_data
    return model_path