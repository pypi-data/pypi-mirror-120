import numpy as np
import torch
import cv2
from yolov5_inference.models.experimental import attempt_load
from yolov5_inference.utils.datasets import letterbox
from yolov5_inference.utils.general import non_max_suppression, scale_coords


class DetectObject(object):
    def __init__(self, weights, classes):
        # self.source = "yolov5_inference/test"
        assert isinstance(classes, dict), 'classes must be dictionary'
        self.classes = classes
        self.weights = weights
        self.img_size = 640
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = attempt_load(self.weights, map_location=self.device)
        self.model.to(self.device).eval()

    def detect(self, im0s):
        img = letterbox(im0s, new_shape=self.img_size)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        # Inference
        pred = self.model(img, augment=True)[0]
        # Apply NMS
        pred = non_max_suppression(pred, 0.5, 0.5, agnostic=True)
        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    x_min, y_min, x_max, y_max = [int(xyxy[index].item()) for index in range(4)]
                    cv2.rectangle(im0s, (x_min, y_min), (x_max, y_max), color=(0, 255, 0))
                    cls = cls.detach().cpu().numpy().astype(np.int8).tolist()
                    cv2.putText(im0s, self.classes[cls], (x_min, y_min), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1,
                                color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
                    # return im0s[y_min:y_max, x_min:x_max]
            # else:
            #     return im0s
        return im0s


if __name__ == '__main__':
    img = cv2.imread('../test/240172424_262872675656592_2069795755616540656_n.jpg')
    class_name = {0: 'text', 1: 'title', 2: 'list', 3: 'table', 4: 'figure'}
    model = DetectObject(weights='../best.pt', classes=class_name)
    rs = model.detect(img)
    print(rs.shape)
