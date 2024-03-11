import base64
import io
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
import face_recognition
import cv2
import numpy as np
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.views.decorators.http import require_POST
import face_recognition
from django.http import JsonResponse
from .models import MyModel
import json
from PIL import Image


def run(request):
    if request.method == "POST":
        # Get the image data from the POST request
        image_data = request.POST.get("image_data")
        image_data_str = image_data.replace("data:image/jpeg;base64,", "")
        image_data = base64.b64decode(image_data_str)
        nparr = np.frombuffer(image_data, np.uint8)

       
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        name = face_detection(image)

    return render(request, "img.html", {"name": name})


def face_detection(frame):
    # matches_name=[]
    known_face_encodings = []
    known_face_names = []
    for face in MyModel.objects.all():
        encoding = json.loads(face.face_encoding)
        known_face_encodings.append(np.array(encoding))
        known_face_names.append(face.name)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations
        )

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )
            name = "Unknown"

            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                face_names.append(name)
            else:
                name = "Unknown"
                face_names.append(name)
                

            #face_names.append(name)
        print(face_names)

    process_this_frame = not process_this_frame

    return face_names


def gen_frames(cap):
    while True:
        obama_image = face_recognition.load_image_file("karanjecket.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("dharmik.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        yash_image = face_recognition.load_image_file("yash.jpg")
        yash_face_encoding = face_recognition.face_encodings(yash_image)[0]

        swayam_image = face_recognition.load_image_file("swayam.jpg")
        swayam_encoding = face_recognition.face_encodings(swayam_image)[0]
        kenil_image = face_recognition.load_image_file("kenil.jpg")
        kenil_encoding = face_recognition.face_encodings(kenil_image)[0]

        # Create arrays of known face encodings and their names
        known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding,
            yash_face_encoding,
            swayam_encoding,
            kenil_encoding,
        ]
        known_face_names = ["Karan", "dharmik", "yash", "swayam", "kenil"]

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        success, frame = cap.read()
        if not success:
            break
        else:
            if process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding
                    )
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding
                    )
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)
                    print(face_names)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(
                    frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
                )
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(
                    frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
                )

            # Display the resulting image
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


def index(request):
    return render(request, "index.html")


@gzip.gzip_page
def video_feed(request):
    cap = cv2.VideoCapture(0)
    return StreamingHttpResponse(
        gen_frames(cap), content_type="multipart/x-mixed-replace;boundary=frame"
    )


CASCADE_PATH = (
    "haarcascade_frontalface_default.xml"  # Path to the face cascade XML file
)


def detect_and_recognize_faces(frame):
    # Load known face encodings from the database
    print(frame)
    matches_name = []
    known_face_encodings = []
    known_face_names = []
    for face in MyModel.objects.all():
        encoding = json.loads(face.face_encoding)
        known_face_encodings.append(np.array(encoding))
        known_face_names.append(face.name)
    print(f"known ---{known_face_names}")

    # Convert frame to RGB for face recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print(f"rgb -{rgb_frame}")

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    print(f"face locations{face_locations}")
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    print(face_encodings)

    # Recognize faces
    for (top, right, bottom, left), face_encoding in zip(
        face_locations, face_encodings
    ):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            print(name)
            matches_name.append(name)

        # Draw rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw label with name above the rectangle
        cv2.rectangle(frame, (left, top - 25), (right, top), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 0.5, (0, 0, 0), 1)
    print(matches_name)


def gen_frames1(camera):
    # Use 0 for default camera, or provide the path to a video file
    while True:
        success, frame = camera.read()

        if not success:
            break
        else:
            detect_and_recognize_faces(frame)
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@gzip.gzip_page
def live_feed1(request):
    try:
        camera = cv2.VideoCapture(0)
        return StreamingHttpResponse(
            gen_frames1(camera), content_type="multipart/x-mixed-replace;boundary=frame"
        )
    except Exception as e:
        print(f"An error occurred: {e}")
