from ultralytics import YOLO

model = YOLO("yolo11s-cls.pt")
model.train(
    data="pets_split",
    epochs=50,
    imgsz=256,
    batch=64,
    amp=True
)