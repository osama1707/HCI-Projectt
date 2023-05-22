import cv2
import face_recognition
import sqlite3
import io
import pyttsx3

# Connect to the database
connection = sqlite3.connect("PersonsData.db")
cursor = connection.cursor()

ct=0
# Retrieve the information of known faces from the database
known_faces = {}
cursor.execute("SELECT Person_name, Person_Info, picture FROM PersonsData")
rows = cursor.fetchall()
for name, person_info, image_data in rows:
    try:
        # Load image data as a file-like object
        image_stream = io.BytesIO(image_data)
        face_image = face_recognition.load_image_file(image_stream)
        face_encoding = face_recognition.face_encodings(face_image)[0]
        known_faces[name] = (face_encoding, person_info)
    except Exception as e:
        print(f"Error loading image for {name}: {e}")

# Initialize the camera capture
video_capture = cv2.VideoCapture(0)

# Initialize the text-to-speech engine
engine = pyttsx3.init()


voice_assistant_active = False


def speak(text):
    global voice_assistant_active
    voice_assistant_active = True
    engine.say(text)
    engine.runAndWait()
    voice_assistant_active = False

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    
    # Convert the frame to RGB format
    rgb_frame = frame[:, :, ::-1]
    
    # Find all faces in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
            [known_face[0] for known_face in known_faces.values()],
            face_encoding
        )
        name = "Unknown Person"
        if True in matches:
            match_index = matches.index(True)
            name = list(known_faces.keys())[match_index]
        face_names.append(name)
    
    # Draw rectangles and names around the detected faces
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Read out the person's information
        if name != "Unknown Person" and not voice_assistant_active:
            person_info = known_faces[name][1]
            speak(person_info)

            

    
    # Display the resulting frame
    cv2.imshow('Video', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture, close the window, and disconnect from the database
video_capture.release()
cv2.destroyAllWindows()
connection.close()
