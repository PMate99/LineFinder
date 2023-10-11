import cv2
import numpy as np
import math


def LineFinder(picture):
    # kep beolvasasa:
    img = cv2.imread(picture, cv2.IMREAD_COLOR)

    # atlagolo szures:
    noisesrc = cv2.blur(img, (5, 5))

    # eldetektalas:
    edges = cv2.Canny(noisesrc, 50, 200, None, 3)

    # vonalak illesztese
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)

    # leghosszabb vonalhossz kiszamitasa
    sizemax = math.sqrt(edges.shape[0] ** 2 + edges.shape[1] ** 2)

    # ciklushoz valtozok:
    szogtomb = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    rhotomb = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    index = 0
    counter = 0
    hiba = False

    # vonalak szurese es kirajzolasa:
    if lines is not None:
        for i in range(0, len(lines)):
            theta = lines[i][0][1]
            thetaFok = theta / np.pi * 180
            rho = lines[i][0][0]
            rho2 = rho
            if (rho < 0):
                rho = rho * (-1)

            for j in range(0, len(szogtomb)):
                if (szogtomb[j] == 0 and j == 0):
                    break
                elif ((szogtomb[j] < thetaFok + 5 and szogtomb[j] > thetaFok - 5) and
                      (rhotomb[j] < rho + 25.0 and rhotomb[j] > rho - 25.0)):
                    hiba = True
                    break

            if (not (hiba)):
                counter += 1
                szogtomb[index] = thetaFok
                rhotomb[index] = rho
                index += 1
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho2
                y0 = b * rho2

                pt1 = (int(x0 + sizemax * (-b)), int(y0 + sizemax * a))
                pt2 = (int(x0 - sizemax * (-b)), int(y0 - sizemax * a))
                cv2.line(img, pt1, pt2, (0, 0, 255), 3)
                cv2.imshow("Palcikak detektalasa", img)
                cv2.waitKey(0)
            elif (hiba):
                hiba = False

    # (counter, "db fogpalcika van a kepen")
    print(counter)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

LineFinder("./Pictures/palcika6.png")
