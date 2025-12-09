import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pathlib import Path
from ultralytics import YOLO


#color scheme
BG_COLOR = "#000000"     #background
FG_COLOR = "#ffffff"     #text color
ACCENT_COLOR = "#3a5f77" #buttons
FONT = ("Arial", 12)

project_root = Path(__file__).resolve().parent.parent.parent
model_path_cat_vs_dog = project_root / "models" / "dog_vs_cat" / "dog_vs_cat_model_0.pt"
model_path_breed = project_root / "models" / "breed" / "breed_model_0.pt"

# try to load both yolo models
model_cat_vs_dog = None
model_breed = None

try:
    model_cat_vs_dog = YOLO(model_path_cat_vs_dog)
    model_breed = YOLO(model_path_breed)
except Exception as e:
    messagebox.showerror(
        "Model Error", 
        f"Failed to load one or both models. Please check file paths:\n\n"
        f"Dog/Cat Path: {model_path_cat_vs_dog}\n"
        f"Breed Path: {model_path_breed}\n\n"
        f"Details: {e}"
    )

class DogCatClassifierApp:
    def __init__(self, master):
        #setup window and gui
        self.master = master
        master.title("Furry Friends Classifier")
        master.configure(bg=BG_COLOR)

        self.master.geometry("700x750")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(2, weight=1)

        self.image_path = None

        self.title_label = tk.Label(master, text="upload an image to classify", font=("Arial", 18, "bold"), bg=BG_COLOR, fg=FG_COLOR)
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")

        self.upload_button = tk.Button(master, text="select image", command=self.select_image, font=FONT, bg=ACCENT_COLOR, fg="white", activebackground=FG_COLOR, relief=tk.FLAT, padx=10, pady=5)
        self.upload_button.grid(row=1, column=0, pady=10)

        self.image_frame = tk.Frame(master, bd=2, relief=tk.SUNKEN, bg="black")
        self.image_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.image_frame.grid_propagate(False)

        self.image_label = tk.Label(self.image_frame, text="your image will appear here.", fg="gray", bg="black")
        self.image_label.pack(expand=True, fill="both")

        self.result_frame = tk.Frame(master, bg=BG_COLOR)
        self.result_frame.grid(row=3, column=0, pady=(10, 20), padx=20, sticky="ew")
        
        # prediction 1: dog vs cat
        self.label_cat_dog = tk.Label(self.result_frame, text="class prediction: awaiting image.", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR, pady=5)
        self.label_cat_dog.pack(fill="x")
        
        # prediction 2: breed
        self.label_breed = tk.Label(self.result_frame, text="breed prediction: awaiting image.", font=("Arial", 14), bg=BG_COLOR, fg=FG_COLOR, pady=5)
        self.label_breed.pack(fill="x")

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            title="select a dog or cat image.",
            filetypes=(
                ("image files", "*.jpg;*.jpeg;*.png"),
                ("all files", "*.*")
            )
        )
        if self.image_path:
            self.display_image()
            self.run_prediction()

    def display_image(self):
        img = Image.open(self.image_path)
        
        #calculate frame size for resizing
        frame_width = self.image_frame.winfo_width() - 4
        frame_height = self.image_frame.winfo_height() - 4
        
        #resize image to fit the frame while maintaining aspect ratio
        if frame_width > 0 and frame_height > 0:
            ratio = min(frame_width / img.width, frame_height / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo, text="", bg="black")
        self.image_label.image = self.photo # keep a reference to prevent garbage collection

    def _format_prediction(self, model_label, model_instance):
        #run prediction on the specific model
        results = model_instance.predict(source=self.image_path, verbose=False)
        
        result = results[0]
        prob = result.probs
        top_class_id = prob.top1
        
        top_confidence = prob.top1conf.item()
        label = result.names[top_class_id]
        
        confidence_percent = top_confidence * 100
        
        result_text = f"{model_label}: {label.upper()} ({confidence_percent:.0f}% confident)."
        
        return result_text

    def run_prediction(self):
        #check if both models loaded successfully
        if not model_cat_vs_dog or not model_breed:
            self.label_cat_dog.config(text="class prediction: one or both models failed to load.", fg="red")
            self.label_breed.config(text="breed prediction: one or both models failed to load.", fg="red")
            return

        try:
            # run dog vs cat prediction
            cat_dog_text = self._format_prediction("class", model_cat_vs_dog)
            self.label_cat_dog.config(text=cat_dog_text, fg="#2ecc71") # green success color

            # run breed prediction
            breed_text = self._format_prediction("breed", model_breed)
            self.label_breed.config(text=breed_text, fg="#2ecc71")

        except Exception as e:
            #handle any errors during the prediction process
            error_msg = f"prediction failed: {e}."
            self.label_cat_dog.config(text=error_msg, fg="red")
            self.label_breed.config(text=error_msg, fg="red")
            print(f"prediction error: {e}")


if __name__ == "__main__":
    if model_cat_vs_dog is not None and model_breed is not None:
        root = tk.Tk()
        app = DogCatClassifierApp(root)
        
        root.bind("<Configure>", lambda event: app.display_image() if app.image_path else None)
        
        root.mainloop()
    else:
        pass