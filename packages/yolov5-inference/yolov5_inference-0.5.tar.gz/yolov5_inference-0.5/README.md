Package dung de inference model yolov5 voi custom object
# Install
```bash
pip install yolov5_inference
```

# Use
```bash
from yolov5_inference.infer import DetectObject
class_name = {0: 'text', 1: 'title', 2: 'list', 3: 'table', 4: 'figure'}
model = DetectObject(weights='../path/of/weights', classes=class_name)
img_path = '../path/of/img'
rs = model.detect(img_path)
```
