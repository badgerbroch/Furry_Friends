from ultralytics import YOLO
if __name__ == "__main__":
    model = YOLO("yolo11s-cls.pt")
    model.train(
        data="pets_breed_split",
        epochs=50,
        imgsz=256,
        batch=64,
        amp=True
    )