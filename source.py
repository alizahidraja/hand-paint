import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

points = []

pencil_img = cv2.imread("images/pencil.png")
pencil_img = cv2.resize(pencil_img, (100,100))
undo_img = cv2.imread("images/undo.png")
undo_img = cv2.resize(undo_img, (100,100))
cancel_img = cv2.imread("images/cancel.png")
cancel_img = cv2.resize(cancel_img, (100,100))

x_offset = 500
y_offset = 10
pencil = False
undo = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    img = cv2.rectangle(img, (30, 30), (420, 420), (0, 255, 0), 3)
    img[50:50+100, x_offset:x_offset+100] = pencil_img
    img[170:170+100, x_offset:x_offset+100] = undo_img
    img[290:290+100, x_offset:x_offset+100] = cancel_img
    if pencil:
        img = cv2.rectangle(img, (500, 50), (600, 150), (0, 255, 0), 3)
    if undo:
        img = cv2.rectangle(img, (500, 170), (600, 270), (0, 255, 0), 3)

    tipx = 0
    tipy = 0
    

    for i in points:
        cv2.circle(img, i, 5, (0, 255, 0), cv2.FILLED)

    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = img.shape
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
                        # within grid
                        if pencil and a >= 30 and a <= 420 and b >= 30 and b <= 420:
                            points.append((a, b))

                        elif a >= 500 and a <= 600 and b >= 50 and b <= 150:
                            pencil = True
                            undo = False

                        elif a >= 500 and a <= 600 and b >= 170 and b <= 270:
                            pencil = False
                            undo = True
                            if len(points) > 0:
                                points.pop()
                        
                        elif a >= 500 and a <= 600 and b >= 290 and b <= 390:
                            pencil = False
                            undo = False
                            points = []
                        
                """
                if id == 16:
                    factor = 30
                    if (
                        tipx >= cx - factor
                        and tipx <= cx + factor
                        and tipy >= cy - factor
                        and tipy <= cy + factor
                    ):
                        if len(points) > 0:
                            points.pop()

                if id == 20:
                    factor = 30
                    if (
                        tipx >= cx - factor
                        and tipx <= cx + factor
                        and tipy >= cy - factor
                        and tipy <= cy + factor
                    ):
                        points = []
                
                """
                # if id ==0:
                # cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

            #mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # cv2.putText(
    #    img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
    # )

    cv2.imshow("Hand Paint", img)
    cv2.waitKey(1)
