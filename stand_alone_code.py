import cv2
import mediapipe as mp
# import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

points = []

pencil_img = cv2.imread("images/pencil.png")
pencil_img = cv2.resize(pencil_img, (100, 100))
undo_img = cv2.imread("images/undo.png")
undo_img = cv2.resize(undo_img, (100, 100))
cancel_img = cv2.imread("images/cancel.png")
cancel_img = cv2.resize(cancel_img, (100, 100))

x_offset = 500
y_offset = 10
pencil = False
undo = False

with mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8,
        ) as hand_mesh:
    while cap.isOpened():
        success, image = cap.read()

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        results = hand_mesh.process(image)
        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        image = cv2.rectangle(image, (30, 30), (420, 420), (0, 255, 0), 3)
        image[50 : 50 + 100, x_offset : x_offset + 100] = pencil_img
        image[170 : 170 + 100, x_offset : x_offset + 100] = undo_img
        image[290 : 290 + 100, x_offset : x_offset + 100] = cancel_img
        cv2.putText(image, "By: alizahidraja", (250, 470), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # Show Selected
        if pencil:
            image = cv2.rectangle(image, (500, 50), (600, 150), (0, 255, 0), 3)
        if undo:
            image = cv2.rectangle(image, (500, 170), (600, 270), (0, 255, 0), 3)
        
        # Draw dots
        for i in points:
            cv2.circle(image, i, 5, (0, 255, 0), cv2.FILLED)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id,lm)
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if id == 4:
                        tipx = cx
                        tipy = cy

                    if id == 8:
                        factor = 30
                        if (
                            tipx >= cx - factor
                            and tipx <= cx + factor
                            and tipy >= cy - factor
                            and tipy <= cy + factor
                        ):
                            a = int((tipx + cx) / 2)
                            b = int((tipy + cy) / 2)
                            # make dots
                            if pencil and a >= 30 and a <= 420 and b >= 30 and b <= 420:
                                points.append((a, b))

                            # pencil
                            elif a >= 500 and a <= 600 and b >= 50 and b <= 150:
                                pencil = True
                                undo = False

                            # undo
                            elif a >= 500 and a <= 600 and b >= 170 and b <= 270:
                                pencil = False
                                undo = True
                                if len(points) > 0:
                                    points.pop()

                            # cancel
                            elif a >= 500 and a <= 600 and b >= 290 and b <= 390:
                                pencil = False
                                undo = False
                                points = []
                    #if id ==0:
                    #    cv2.circle(image, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

            #mpDraw.draw_landmarks(image, handLms, mp.solutions.hands.HAND_CONNECTIONS)
            

    """
    # FPS Counter
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(
       img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
    )
    """
    cv2.imshow("Hand Paint", image)
    cv2.waitKey(1)
