# Face Recognition Attendance System

This project is a face recognition attendance system built using Python, OpenCV, and the face_recognition library. It captures faces through the webcam, recognizes known faces, and logs their attendance in a CSV file. Unknown faces are captured and stored in a separate folder for further analysis.

## Features

- Recognizes and logs attendance of known faces.
- Saves images of unrecognized faces in a specified folder.
- Uses CSV files to store attendance logs.
- Uses OpenCV for video capture and face_recognition for face encoding and matching.

## Prerequisites

- Python 3.x
- OpenCV
- face_recognition library
- dlib library (used by face_recognition)
- CSV module (standard library)
- datetime module (standard library)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/face-recognition-attendance.git
   cd face-recognition-attendance


   pip install opencv-python face_recognition dlib


Place the images of the students to be recognized in the project directory and name them appropriately (e.g., student1.jpg, student2.jpg).

Modify the known_face_encodings and known_face_names arrays in face_recognition_attendance.py to include the encodings and names of the students:




known_face_encodings = [
    encoding_student1,
    encoding_student2
]
known_face_names = [
    "priyanshu",
    "hariom"
]
face-recognition-attendance/
│
├── recognized_students.csv       # CSV file to log recognized students
├── student1.jpg                  # Image file of student 1
├── student2.jpg                  # Image file of student 2
├── blacklist/                    # Folder to store images of unrecognized faces
├── face_recognition_attendance.py # Main Python script


Acknowledgements
This project uses the face_recognition library by Adam Geitgey.
The OpenCV library is used for video capture and image processing.
License
This project is licensed under the MIT License. See the LICENSE file for details.
