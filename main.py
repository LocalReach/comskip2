import cv2
import numpy as np
import time

# Threshold for considering a frame as black
BLACK_THRESHOLD = 30
# Duration of black screen in milliseconds to trigger logging
BLACK_SCREEN_DURATION = 1

# Initialize the background subtractor
background_subtractor = cv2.createBackgroundSubtractorMOG2()

def is_black_frame(frame):
    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate mean intensity of the frame
    mean_intensity = np.mean(gray_frame)
    # If mean intensity is below the threshold, consider it as a black frame
    return mean_intensity < BLACK_THRESHOLD

def main():
    # Replace 'your_stream_url_or_path' with the actual stream URL or path
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open stream.")
        return

    black_screen_start_time = None
    prev_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame.")
            break

        # Apply background subtraction
        fg_mask = background_subtractor.apply(frame)

        # Perform frame differencing with previous frame
        if prev_frame is not None:
            diff = cv2.absdiff(frame, prev_frame)
            diff_mean = np.mean(diff)

            if diff_mean > BLACK_THRESHOLD:
                if black_screen_start_time is None:
                    black_screen_start_time = time.time() * 1000  # Convert to milliseconds
            else:
                if black_screen_start_time is not None:
                    # Calculate duration of black screen
                    duration = (time.time() * 1000) - black_screen_start_time
                    if duration >= BLACK_SCREEN_DURATION:
                        print("Black screen or cut detected for {} milliseconds".format(duration))
                    black_screen_start_time = None

        # Update previous frame
        prev_frame = frame.copy()

        cv2.imshow('Stream', frame)
        cv2.imshow('Foreground Mask', fg_mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
