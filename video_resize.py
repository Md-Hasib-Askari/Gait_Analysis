import cv2

# Set the new width and height of the resized video
new_width = 640
new_height = 480

# Read the input video file
cap = cv2.VideoCapture('video2.mp4')

# Set the output video format and frame rate
output_format = cv2.VideoWriter_fourcc(*'mp4v')
output_fps = 30

# Create the output video writer object
out = cv2.VideoWriter('video.mp4', output_format, output_fps, (new_width, new_height))

# Loop through the frames of the input video, resize each frame, and write it to the output video
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        resized_frame = cv2.resize(frame, (new_width, new_height))
        out.write(resized_frame)
    else:
        break

# Release the input and output video objects
cap.release()
out.release()
