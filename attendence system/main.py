import cv2
import face_recognition
import csv
import os
from datetime import datetime

# Students ke images load karein
image_of_student1 = face_recognition.load_image_file("student1.jpg")
image_of_student2 = face_recognition.load_image_file("student2.jpg")

# Images ka encoding karein
encoding_student1 = face_recognition.face_encodings(image_of_student1)[0]
encoding_student2 = face_recognition.face_encodings(image_of_student2)[0]

# Known face encodings aur names ka array banayein
known_face_encodings = [
    encoding_student1,
    encoding_student2
]
known_face_names = [
    "priyanshu",
    "hariom"
]

# Variables initialize karein
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Recognized students ke liye ek dictionary banayein
recognized_students = {}

# Webcam ka reference lein (0 usually built-in webcam hoti hai)
video_capture = cv2.VideoCapture(0)

# CSV file ko append mode mein open karein
with open('recognized_students.csv', mode='a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # CSV se existing names ko recognized_students dictionary mein read karein
    with open('recognized_students.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            recognized_students[row[0]] = True

    # Folder create karein jahan unrecognized face ka image save hoga
    blacklist_folder = 'blacklist'
    if not os.path.exists(blacklist_folder):
        os.makedirs(blacklist_folder)

    while True:
        # Frame-by-frame capture karein
        ret, frame = video_capture.read()

        # Frame ko flip karein horizontally for mirror effect
        frame = cv2.flip(frame, 1)

        # BGR color se RGB color mein convert karein
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if process_this_frame:
            # Current frame mein sabhi faces aur unke encodings ko dhoondein
            face_locations = face_recognition.face_locations(rgb_frame, model='hog')
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            face_names = []
            for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                # Known faces ke sath match karke dekhein
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Agar known_face_encodings mein match mila, toh name ko update karein
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    # Check karein agar yeh student pehle se recognized hai ya nahi
                    if name not in recognized_students:
                        # Recognized student ka name aur timestamp CSV mein likhein
                        now = datetime.now()
                        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                        csv_writer.writerow([name, timestamp])

                        # Is student ko recognized mark karein
                        recognized_students[name] = True
                else:
                    # Unrecognized student ka image capture karke blacklist folder mein save karein
                    face_image = frame[top:bottom, left:right]
                    img_name = f"{blacklist_folder}/unrecognized_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                    cv2.imwrite(img_name, face_image)
                    print("Unrecognized face detected! Image saved in 'blacklist' folder.")

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Results display karein
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Face ke aas paas ek rectangle banayein
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Name ke neeche label banayein
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Resulting image display karein
        cv2.imshow('Attendance System', frame)

        # Keyboard se 'q' press karke quit karein
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Webcam ko release karein
video_capture.release()
cv2.destroyAllWindows()
