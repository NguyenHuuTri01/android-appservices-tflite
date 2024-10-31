import cv2
import numpy as np
from asb import AndroidScreenBuffer

# Biến toàn cục để lưu khung hình trước đó
previous_frame = None

def detect_faces(diff_threshold=5000):
    global previous_frame

    # Sử dụng AndroidScreenBuffer để chụp màn hình
    screen_buffer = AndroidScreenBuffer()
    screen_buffer.run()
    image_data = screen_buffer.get_last_frame()  # Lấy dữ liệu hình ảnh từ màn hình

    if image_data is not None:
        # Chuyển đổi byte array thành hình ảnh OpenCV
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Nếu đây là khung hình đầu tiên, chỉ cần lưu và xử lý
        if previous_frame is None:
            previous_frame = image
        else:
            # Tính sự khác biệt giữa khung hình hiện tại và khung hình trước
            diff = cv2.absdiff(previous_frame, image)
            non_zero_count = np.count_nonzero(diff)

            # Nếu sự khác biệt nhỏ hơn threshold, coi khung hình là trùng lặp
            if non_zero_count < diff_threshold:
                return "Duplicate frame detected. Skipping processing."

            # Cập nhật khung hình trước với khung hình hiện tại
            previous_frame = image

        # Sử dụng cascade classifier để phát hiện khuôn mặt
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Phát hiện khuôn mặt
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        coordinates = []
        for (x, y, w, h) in faces:
            coordinates.append(f"Face detected at: X: {x}, Y: {y}, Width: {w}, Height: {h}")

        if not coordinates:
            return "No faces detected"

        return "\n".join(coordinates)
    else:
        return [1,2,3,4,5]