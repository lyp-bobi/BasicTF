import cv2
import os
from matplotlib import pyplot as plt

list = os.listdir("./diagrams")

for i in range(0,len(list)):
    path=os.path.join("./diagrams",list[i])
    path= os.path.abspath(path)
    print(path)
    imgs=[]
    kps=[]
    dess=[]
    if(os.path.isfile(path)):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sift = cv2.xfeatures2d.SIFT_create()
        kp, des = sift.detectAndCompute(gray, None)
        imgs.append(img)
        kps.append(kp)
        dess.append(des)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(dess[0], dess[1], k=2)

    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    # cv2.drawMatchesKnn expects list of lists as matches.
    img3 = cv2.drawMatchesKnn(imgs[0], kps[0], imgs[1], kps[1], good, flags=2)

    plt.imshow(img3), plt.show()



        # img = cv2.drawKeypoints(gray, kps, img)
        #
        # cv2.imshow("img", img)
        #
        # k = cv2.waitKey(0)
        # if k & 0xff == 27:
        #     cv2.destroyAllWindows()