from detectron2.engine import DefaultPredictor
import prediction_config

import cv2

def prediction(image_path):

    im = cv2.imread(image_path)
    predictor = DefaultPredictor(prediction_config.get_prediction_config())
    outputs = predictor(im)
    print(outputs["instances"].scores)
    if len(outputs["instances"]) == 0: # 결과가 빈 값일 때
        print('output empty')
        return False
    if outputs["instances"].scores.max() > 0.85:
        return True
    else:
        return False