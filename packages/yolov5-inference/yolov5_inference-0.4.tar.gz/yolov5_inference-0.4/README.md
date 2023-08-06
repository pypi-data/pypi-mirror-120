Package dung de inference model yolov5 voi custom object
# Install
```bash
pip install yolov5_inference
```

# Use
```bash
from yolov5_inference.infer import DetectObject
model = DetectObject(weights='../path/of/weights')
img_path = '../path/of/img'
rs = model.detect(img_path)
```
