# 🌞 Gesture-Based Brightness Control

This project implements a **touchless brightness control system** using **hand gestures**.  
By analyzing the distance between fingers with a webcam feed, the brightness level of the screen can be adjusted in real-time without using keyboard shortcuts or buttons.  

---

## 📖 Introduction
Modern HCI (Human-Computer Interaction) is moving towards **touchless interfaces**.  
This project demonstrates how **computer vision + hand tracking** can be applied to dynamically adjust screen brightness.  

- **Core idea:**  
  - Detect hand using a webcam.  
  - Measure distance between **thumb and index finger**.  
  - Map that distance to brightness levels (0–100%).  

This is useful for accessibility, smart classrooms, and futuristic computer interaction systems.

---

## 🚀 Features
- 🖐️ **Real-time hand tracking** using **MediaPipe**.  
- 🌡️ **Dynamic mapping** of finger distance to brightness level.  
- 💻 Works on **any laptop/PC with a webcam**.  
- ⚡ **Fast & lightweight**, runs in real time.  
- 🌙 Can be extended to control **volume, contrast, or other system settings**.  

---

## 🛠️ Tech Stack
- **Python 3.x**
- **OpenCV** → Image processing & webcam feed  
- **MediaPipe** → Hand detection & landmark extraction  
- **NumPy** → Mathematical operations  
- **ScreenBrightnessControl** → Adjust brightness (Windows/Linux)  
- **PyAutoGUI (optional)** → Extra automation if needed  

---

## 📂 Project Structure
gesture-brightness-control/
│── main.py # Main script
│── HandTrackingModule.py # Custom module (if separated)
│── requirements.txt # Dependencies
│── README.md # Documentation
