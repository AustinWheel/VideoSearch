import cv2

class ImageConvert:
    def __init__(self, videoPath: str) -> None:
        self.videoPath = videoPath

    
    def generateImages(self, step: int):
        cam = cv2.VideoCapture(self.videoPath)

        currentframe = 0
        frames_captured = 0

        while (True):
            ret, frame = cam.read()
            if ret:
                if currentframe > (step):
                    currentframe = 0
                    name = 'data/photos/frame' + str(frames_captured) + '.jpg'
                    print(name)
                    cv2.imwrite(name, frame)
                    frames_captured += 1
                currentframe += 1
            if ret==False:
                break
        cam.release()
        cv2.destroyAllWindows()