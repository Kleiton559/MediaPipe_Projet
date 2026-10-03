import cv2
import numpy as np
import mediapipe as mp
import ledAction as la
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ============================================================
# LANDMARKS DO OLHO ESQUERDO
# ============================================================

LEFT_EYE = [
    362, 382, 381, 380, 374, 373, 390, 249,
    263, 466, 388, 387, 386, 385, 384, 398
]


# ============================================================
# FUNÇÃO PARA CALCULAR A DISTÂNCIA ENTRE DOIS PONTOS
# ============================================================

def distance(point1, point2):

    return np.linalg.norm(
        np.array(point1) - np.array(point2)
    )


# ============================================================
# FUNÇÃO PARA CALCULAR O EAR
# ============================================================

def calculate_eye_aspect_ratio(face_landmarks):

    # Obter os pontos do olho esquerdo
    points = []

    for index in LEFT_EYE:

        landmark = face_landmarks[index]

        points.append(
            np.array([
                landmark.x,
                landmark.y
            ])
        )


    # Distâncias verticais
    vertical_1 = distance(
        points[1],
        points[5]
    )

    vertical_2 = distance(
        points[2],
        points[4]
    )


    # Distância horizontal
    horizontal = distance(
        points[0],
        points[8]
    )


    # EAR
    ear = (
        vertical_1 + vertical_2
    ) / (
        2.0 * horizontal
    )

    return ear


# ============================================================
# FUNÇÃO PARA DESENHAR O OLHO
# ============================================================

def draw_left_eye(image, detection_result):

    for face_landmarks in detection_result.face_landmarks:

        points = []

        for landmark in face_landmarks:

            x = int(
                landmark.x * image.shape[1]
            )

            y = int(
                landmark.y * image.shape[0]
            )

            points.append((x, y))


        # Desenhar linhas do olho
        for i in range(len(LEFT_EYE)):

            current_point = LEFT_EYE[i]

            next_point = LEFT_EYE[
                (i + 1) % len(LEFT_EYE)
            ]

            cv2.line(
                image,
                points[current_point],
                points[next_point],
                (255, 0, 0),
                2
            )

    return image


# ============================================================
# CONFIGURAÇÃO DO MEDIAPIPE
# ============================================================

base_options = python.BaseOptions(
    model_asset_path="face_landmarker.task"
)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1
)

detector = vision.FaceLandmarker.create_from_options(
    options
)


# ============================================================
# WEBCAM
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("ERRO: Não foi possível abrir a webcam.")

    exit()


# ============================================================
# LOOP PRINCIPAL
# ============================================================

while True:

    success, frame = cap.read()

    if not success:

        print(
            "ERRO: Não foi possível obter a imagem."
        )

        break


    # ========================================================
    # BGR → RGB
    # ========================================================

    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # ========================================================
    # CRIAR MP.IMAGE
    # ========================================================

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame_rgb
    )


    # ========================================================
    # DETECTAR ROSTO
    # ========================================================

    detection_result = detector.detect(
        mp_image
    )


    # ========================================================
    # DESENHAR OLHO
    # ========================================================

    annotated_image = draw_left_eye(
        frame_rgb,
        detection_result
    )


    # ========================================================
    # DETECTAR OLHO ABERTO / FECHADO
    # ========================================================

    if len(detection_result.face_landmarks) > 0:

        face_landmarks = detection_result.face_landmarks[0]


        # Calcular EAR
        ear = calculate_eye_aspect_ratio(
            face_landmarks
        )


        # ----------------------------------------------------
        # LIMIAR
        # ----------------------------------------------------

        if ear < 0.50:

            eye_status = "OLHO ESQUERDO FECHADO"
            print("OLHO ESQUERDO FECHADO")
            la.apagarLED()

        else:

            eye_status = "OLHO ESQUERDO ABERTO"
            print("OLHO ESQUERDO ABERTO")
            la.acenderLED()

        # ====================================================
        # LOG NO TERMINAL
        # ====================================================

        print(
            f"EAR: {ear:.3f} | {eye_status}"
        )


        # ====================================================
        # MOSTRAR STATUS NA IMAGEM
        # ====================================================

        cv2.putText(
            annotated_image,
            eye_status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


        # Mostrar valor do EAR
        cv2.putText(
            annotated_image,
            f"EAR: {ear:.3f}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


    else:

        cv2.putText(
            annotated_image,
            "ROSTO NAO DETECTADO",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )


    # ========================================================
    # RGB → BGR
    # ========================================================

    annotated_image = cv2.cvtColor(
        annotated_image,
        cv2.COLOR_RGB2BGR
    )


    # ========================================================
    # MOSTRAR IMAGEM
    # ========================================================

    cv2.imshow(
        "Deteccao do Olho Esquerdo",
        annotated_image
    )


    # ========================================================
    # SAIR COM Q
    # ========================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ============================================================
# LIBERTAR RECURSOS
# ============================================================

cap.release()

cv2.destroyAllWindows()