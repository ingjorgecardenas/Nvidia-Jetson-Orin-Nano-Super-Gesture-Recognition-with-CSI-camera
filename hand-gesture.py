import cv2
import mediapipe as mp
import time
import math

# PIPELINE para JETPACK 6.X (Ajustado a las capacidades reales de tu sensor)
def gstreamer_pipeline(sensor_id=0, capture_width=640, capture_height=480, display_width=640, display_height=480, framerate=30, flip_method=0):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=True"
        % (sensor_id, capture_width, capture_height, framerate, flip_method, display_width, display_height)
    )

# Sacamos la función de lógica fuera del main para que sea eficiente
def is_hello_gesture(hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]
    palm = hand_landmarks.landmark[0]
    distances = [
        math.sqrt((hand_landmarks.landmark[tip].x - palm.x) ** 2 +
                  (hand_landmarks.landmark[tip].y - palm.y) ** 2 +
                  (hand_landmarks.landmark[tip].z - palm.z) ** 2)
        for tip in finger_tips
    ]
    open_palm_threshold = 0.2
    return all(distance > open_palm_threshold for distance in distances)

def main():
    # CAMBIO: Usamos 60 FPS porque es lo que tu sensor reporta para 1280x720
    pipeline_str = gstreamer_pipeline(sensor_id=0, framerate=60, flip_method=0)
    camera = cv2.VideoCapture(pipeline_str, cv2.CAP_GSTREAMER)
    
    if not camera.isOpened():
        print("Error: No se pudo abrir la sesión de captura. Ejecutá el reset del daemon primero.")
        return
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False, 
        max_num_hands=1, 
        min_detection_confidence=0.5, 
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils

    prev_time = time.time()

    print("Cámara iniciada con éxito. Presioná 'q' para salir.")
    
    while True:
        ret, frame = camera.read()
        if not ret or frame is None:
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Usamos la lógica de gestos
                if is_hello_gesture(hand_landmarks):
                    cv2.putText(frame, "Funciono!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        # FPS
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Gesture Recognition", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
