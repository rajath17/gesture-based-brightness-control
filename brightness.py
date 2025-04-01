import cv2
import mediapipe as mp
import screen_brightness_control as sbc
import csv
from datetime import datetime

# Initialize MediaPipe Hand Detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
# Start video capture
cap = cv2.VideoCapture(0)
# File to save brightness history
csv_filename = "brightness_log.csv"

# Write CSV headers if the file does not exist
try:
    with open(csv_filename, "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Monitor", "Brightness Level"])
except FileExistsError:
    pass  # If file exists, continue

# Get connected monitors
monitors = sbc.list_monitors()  # List of detected screens
print(f"Detected Monitors: {monitors}")

# Initialize current brightness level for each monitor
current_brightness = {}
for monitor in monitors:
    try:
        current_brightness[monitor] = sbc.get_brightness(display=monitor)[0]  # assuming it returns a list
    except Exception as e:
        print(f"Error getting brightness for {monitor}: {e}")
        current_brightness[monitor] = 50  # Default fallback brightness

# Open the CSV file for appending before the loop starts
with open(csv_filename, "a", newline="") as file:
    writer = csv.writer(file)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip frame and convert color
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame for hand detection
        result = hands.process(rgb_frame)

        action = "No Change"

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Thumb tip and thumb base positions
                thumb_tip_y = hand_landmarks.landmark[4].y  # Thumb tip (y-coordinate)
                thumb_base_y = hand_landmarks.landmark[2].y  # Thumb base (y-coordinate)

                # Thumb UP increases brightness by 20%
                if thumb_tip_y < thumb_base_y - 0.05:  # Thumb is up (tip is higher than base)
                    for monitor in monitors:
                        if current_brightness[monitor] < 100:
                            current_brightness[monitor] = min(100, current_brightness[monitor] + 20)  # Increase brightness
                            action = f"Brightness: {current_brightness[monitor]}% (Increasing)"
                            sbc.set_brightness(current_brightness[monitor], display=monitor)

                # Thumb DOWN decreases brightness by 20%
                elif thumb_tip_y > thumb_base_y + 0.05:  # Thumb is down (tip is lower than base)
                    for monitor in monitors:
                        if current_brightness[monitor] > 20:
                            current_brightness[monitor] = max(20, current_brightness[monitor] - 20)  # Decrease brightness
                            action = f"Brightness: {current_brightness[monitor]}% (Decreasing)"
                            sbc.set_brightness(current_brightness[monitor], display=monitor)

                # Get current date and time
                now = datetime.now()
                date_time = now.strftime("%d-%m-%Y %H:%M:%S")

                # Log brightness level with timestamp for each monitor
                for monitor in monitors:
                    writer.writerow([date_time, monitor, current_brightness[monitor]])

                # Print the log in the console
                for monitor in monitors:
                    print(f"Time: {date_time}, Monitor: {monitor}, Brightness: {current_brightness[monitor]}%")

        # Get current date and time
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y %H:%M:%S")

        # Display information on screen
        cv2.putText(frame, action, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 205, 10), 2)
        cv2.putText(frame, "Gesture-Based Brightness Control System", (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, date_time, (350, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (158, 0, 0), 2)

        # Show the video frame
        cv2.imshow("Gesture-Based Brightness Control", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
