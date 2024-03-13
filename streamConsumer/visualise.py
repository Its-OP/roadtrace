import cv2
import json


# Load JSON data
def load_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data


# Draw bounding boxes on the frame
def draw_bounding_boxes(frame, frame_number, boxes_info):
    for obj_id, box in boxes_info.items():
        x1, y1, x2, y2 = int(box['x1']), int(box['y1']), int(box['x2']), int(box['y2'])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, obj_id, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    return frame


# Main function to process the video
def process_video(video_file, json_file, output_file):
    boxes_data = load_json(json_file)
    cap = cv2.VideoCapture(video_file)

    # Video properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        str_frame_number = str(frame_number)
        if str_frame_number in boxes_data:
            frame = draw_bounding_boxes(frame, str_frame_number, boxes_data[str_frame_number])

        out.write(frame)
        frame_number += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()


# Example usage
json_file = './Artifacts/export/export.json'
video_file = './Artifacts/import/demo_5sec.mp4'
output_file = './Artifacts/export/demo_5sec.mp4'
process_video(video_file, json_file, output_file)
