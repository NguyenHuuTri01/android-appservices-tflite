import cv2
import numpy as np
import os

def detect_faces(image_path):

    current_dir = os.path.dirname(__file__)
    cfg_path = os.path.join(current_dir, "yolov3.cfg")
    weights_path = os.path.join(current_dir, "yolov3.weights")
    names_path = os.path.join(current_dir, "coco.names")
    # Load YOLO
    net = cv2.dnn.readNet(weights_path, cfg_path)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i.item() - 1] for i in net.getUnconnectedOutLayers()]
    with open(names_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Load image
    # nparr = np.frombuffer(imageData, np.uint8)
    # img =  cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img =  cv2.imread(image_path)

    if img is None:
        return "Error: Could not decode image."

    height, width, channels = img.shape

    # Prepare the image for YOLO
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Perform detection
    outs = net.forward(output_layers)

    # Showing information on the screen
    class_ids = []
    confidences = []
    boxes = []
    coordinates = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-maximum suppression to remove duplicates
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            coordinates.append(f"{label} detected at: X: {x}, Y: {y}, Width: {w}, Height: {h}")
    if not coordinates:
        result = "No objects detected"
    else:
        result = "\n".join(coordinates)
    return result
