import cv2
import numpy as np


# Função para contar os dedos
def contar_dedos(contorno):
    # Inicialize o contador de dedos
    dedos = 0

    # Calcula o centro do contorno
    centro = None
    if len(contorno) > 0:
        M = cv2.moments(contorno)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centro = (cx, cy)

    # Se o centro foi calculado, conte os dedos
    if centro is not None:
        cv2.circle(frame, centro, 5, (0, 0, 255), -1)
        hull = cv2.convexHull(contorno, returnPoints=False)
        defects = cv2.convexityDefects(contorno, hull)

        if defects is not None:
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(contorno[s][0])
                end = tuple(contorno[e][0])
                far = tuple(contorno[f][0])

                # Calcule a distância entre os pontos
                a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angulo = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

                # Se o ângulo for menor que 90 graus, considere como um dedo
                if angulo < np.pi / 2:
                    dedos += 1
                    cv2.circle(frame, far, 5, (0, 0, 255), -1)

    return dedos


# Inicialize a captura de vídeo
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Pré-processamento da imagem
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Encontre os contornos na imagem
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dedos_contados = 0
    for contorno in contornos:
        if cv2.contourArea(contorno) > 1000:  # Ajuste esse valor conforme necessário
            dedos_contados = contar_dedos(contorno)

    # Exiba o número de dedos contados na janela
    cv2.putText(frame, str(dedos_contados), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Mostre a imagem com a contagem de dedos
    cv2.imshow("Contagem de Dedos", frame)

    if cv2
