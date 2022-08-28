from tensorflow.keras.models import model_from_json
import numpy as np
import cv2
import os



os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def predict_img(img,filename):
    img = cv2.imread(img)

    scale_percent = int(((1200/img.shape[1]))*100)

    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)   
    # resize image
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    gray_fr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facec.detectMultiScale(gray_fr, 1.3, 5)
    for (x, y, w, h) in faces:
        fc = gray_fr[y:y+h, x:x+w]
        roi = cv2.resize(fc, (48, 48))
        pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
        cv2.putText(img, pred, (x, y), font, 1, (255, 255, 0), 2)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        path = os.path.join('static\\imageresult\\', filename)
        #cv2.imshow('Facial Expression Recognization', img)
        cv2.imwrite(path,img)
        
    # cv2.imshow('Facial Expression Recognization', img)
    # if cv2.waitKey(0) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()    

        
class FacialExpressionModel(object):
    EMOTIONS_LIST = ["Angry", "Disgust",
                    "Fear", "Happy",
                    "Neutral", "Sad",
                    "Surprise"]
    def __init__(self, model_json_file, model_weights_file):
        # load model from JSON file
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)
        # load weights into the new model
        self.loaded_model.load_weights(model_weights_file)
        self.loaded_model.make_predict_function()
    def predict_emotion(self, img):
        self.preds = self.loaded_model.predict(img)
        return FacialExpressionModel.EMOTIONS_LIST[np.argmax(self.preds)]




if __name__=="__main__":
    facec = cv2.CascadeClassifier('SupportFiles//haarcascade_frontalface_default.xml')
    model = FacialExpressionModel("SupportFiles//model.json", "SupportFiles//model_weights.h5")
    font = cv2.FONT_HERSHEY_SIMPLEX

    predict_img("testimage\IMG_5848.jpg",'IMG_5848.jpg')
    #$predict_img("testimage\WhatsApp Image 2022-06-01 at 9.08.35 AM.jpeg",'WhatsApp Image 2022-06-01 at 9.08.35 AM.jpeg')
