

import os
import cv2
import numpy as np
import pickle
import tkinter as tk
from tkinter import messagebox

# --- Step 1: Create a simple Tkinter popup window to get name ---

def get_name():
    def submit():
        user_name = entry.get().strip()
        if user_name:
            root.user_name = user_name
            root.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter a valid name.")

    root = tk.Tk()
    root.title("Face Data Collection")
    root.geometry("300x120")
    root.resizable(True, True)

    label = tk.Label(root, text="Enter your name:", font=("Arial", 12))
    label.pack(pady=10)

    entry = tk.Entry(root, font=("Arial", 14))
    entry.pack(pady=5)
    entry.focus()

    btn = tk.Button(root, text="Submit", command=submit)
    btn.pack(pady=10)

    root.user_name = None
    root.mainloop()
    return root.user_name

name = get_name()
if not name:
    print("Name not entered. Exiting...")
    exit()

# --- Step 2: Initialize camera and face cascade ---
face_data = []
i = 0
camera = cv2.VideoCapture(0)
facecascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

# --- Step 3: Capture face frames ---
while True:
    ret, frame = camera.read()
    if not ret:
        print("Camera error. Exiting...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facecascade.detectMultiScale(gray, 1.3, 4)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w, :]
        resized_face = cv2.resize(face, (50, 50))

        if i % 10 == 0 and len(face_data) < 10:
            face_data.append(resized_face)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    i += 1

    cv2.putText(frame, f"Collecting data for: {name}", (10, 30), font, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Captured: {len(face_data)} / 10", (10, 60), font, 0.6, (255, 255, 0), 1)
    cv2.putText(frame, "Press ESC to quit early", (10, 90), font, 0.5, (200, 200, 200), 1)

    cv2.imshow("Face Capture", frame)

    if cv2.waitKey(1) == 27 or len(face_data) >= 10:
        break

# --- Step 4: Cleanup ---
camera.release()
cv2.destroyAllWindows()

face_data = np.asarray(face_data)
face_data = face_data.reshape(10, -1)

# --- Step 5: Save data ---
os.makedirs('data', exist_ok=True)

names_path = 'data/names.pkl'
faces_path = 'data/faces.pkl'

if os.path.exists(names_path):
    with open(names_path, 'rb') as f:
        names = pickle.load(f)
    names += [name] * 10
else:
    names = [name] * 10

with open(names_path, 'wb') as f:
    pickle.dump(names, f)

if os.path.exists(faces_path):
    with open(faces_path, 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, face_data, axis=0)
else:
    faces = face_data

with open(faces_path, 'wb') as f:
    pickle.dump(faces, f)

# --- Step 6: Show success popup ---
tk.messagebox.showinfo("Success", f"✅ Successfully added 10 face samples for '{name}'!")
