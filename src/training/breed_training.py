from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolo11s-cls.pt")
    
    
    model.train(
        data="pets_breed_split",
        epochs=120,
        patience=20,
        imgsz=256,
        batch=32,
        optimizer="AdamW", # Adam over SGD since small dataset
        device=0,
        lr0=1e-3, # smaller lr since small dataset
        lrf=0.01,
        label_smoothing=0.1,
        weight_decay=0.01,
        dropout=0.2,
        
        workers=4,
        cache=True,
        val=True,
        seed=0,
    )