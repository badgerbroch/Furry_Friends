from pathlib import Path
from ultralytics import YOLO
# root of where repo was cloned
base_path = Path.home() / "Desktop" / "Senior Year" / "Super_Senior" / "Furry Friends" 
# model path
model_path = base_path / "Furry_Friends" / "models" / "breed" / "breed_model_0.pt"

image_folder = base_path / "Furry_Friends" / "src" / "inference" / "example_images"

dog_image = image_folder / "dog_example_0.jpg"

model = YOLO(model_path)
# Predicting breed from dog image
def run_predict():
    return model.predict(source=dog_image)[0]

if __name__ == "__main__":
    import cProfile, pstats
    
    run_predict()
    prof = cProfile.Profile()
    prof.enable()
    
    # Averaging loop
    for _ in range(30):
        run_predict()
    
    prof.disable()
    out_path = Path(__file__).with_suffix(".prof")
    prof.dump_stats(out_path)
    