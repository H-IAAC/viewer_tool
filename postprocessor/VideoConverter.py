import cv2
import mediapipe as mp
import ffmpegcv
import face_recognition #https://github.com/ageitgey/face_recognition

class VideoConverter:
    @staticmethod
    def hide_faces2(video_in, video_out):
        
        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(video_in)
        
        video_fps = int(video_capture.get(cv2.CAP_PROP_FPS))
        video_output = ffmpegcv.VideoWriter(video_out, None, video_fps)

        # Initialize some variables
        face_locations = []
        print("0")
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face detection processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(small_frame, model="cnn")
            print("1")
            # Display the results
            for top, right, bottom, left in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                print("2")
                # Extract the region of the image that contains the face
                face_image = frame[top:bottom, left:right]
                print("3")
                # Blur the face image
                face_image = cv2.GaussianBlur(face_image, (99, 99), 30)
                print("4")
                # Put the blurred face region back into the frame image
                frame[top:bottom, left:right] = face_image
            print("5")
            # Display the resulting image
            #cv2.imshow('Video', frame)
            video_output.write(frame)
            print("6")
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        video_output.release()
    
    
    
    
    
    @staticmethod
    def hide_faces(video_in, video_out):
        cap = cv2.VideoCapture(video_in)

        video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        if (video_width >= 540 or video_width >= 960):
            video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)
            video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2)
        
        print(f"->    {video_in} video_height: {video_height} video_width: {video_width}")
        print(f"->    {video_in} video_fps: {video_fps}")
        
        out = ffmpegcv.VideoWriter(video_out, None, video_fps)
        
        prev_detected = False
        prev_results = None
        
        with mp.solutions.face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5) as face_detection:

            while True:
                success, img = cap.read()
                
                if not success:
                    continue
                
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                img.flags.writeable = False
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                results = face_detection.process(img)
                
                # Draw the face detection annotations on the image.
                img.flags.writeable = True
                img = cv2.resize(img, (video_width, video_height))
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)            
                
                if results.detections or prev_detected:
                    if results.detections:
                        prev_results = results.detections
                    prev_detected = True
                    
                    for detection in prev_results:

                        bboxC = detection.location_data.relative_bounding_box
                        ih, iw, ic = img.shape

                        # For rectange
                        bbox = int((bboxC.xmin - 0.04) * iw), int((bboxC.ymin - 0.04) * ih), int(bboxC.width * iw * 2), int(bboxC.height * ih * 2)                       
                        cv2.rectangle(img, bbox, (0,0,0), -1)

                out.write(img)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        print(f"->    {video_in} hide_faces completed")
        cap.release()
        out.release()
        