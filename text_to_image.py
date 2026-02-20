import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Dataset paths
asl_dir = r"D:\P-34\ISL and ASL\ASL data\asl_alphabet_train\asl_alphabet_train"
isl_dir = r"D:\P-34\ISL and ASL\ISL data\Indian"  # <-- Corrected ISL path

class SignLanguageImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Letter Viewer")
        self.root.geometry("700x700")
        self.root.configure(bg="#f0f8ff")

        # Heading
        self.heading = tk.Label(root, text="Sign Language Letter Viewer", font=("Arial", 22, "bold"), bg="#f0f8ff", fg="#333")
        self.heading.pack(pady=15)

        # Dropdown to select language
        self.language_var = tk.StringVar(value="ASL")
        self.language_menu = tk.OptionMenu(root, self.language_var, "ASL", "ISL")
        self.language_menu.config(font=("Arial", 14), bg="#0072ff", fg="white")
        self.language_menu.pack(pady=10)

        # Instruction label
        self.label = tk.Label(root, text="Enter letters (A-Z):", font=("Arial", 16), bg="#f0f8ff")
        self.label.pack(pady=5)

        # Entry widget
        self.entry = tk.Entry(root, font=("Arial", 16), justify="center")
        self.entry.pack(pady=10, ipadx=20)

        # Show Images button
        self.button = tk.Button(root, text="Show Images", font=("Arial", 14), bg="#0072ff", fg="white", command=self.show_images, relief="raised", bd=3)
        self.button.pack(pady=10)

        # Frame for images
        self.image_frame = tk.Frame(root, bg="#f0f8ff")
        self.image_frame.pack(pady=20, fill="both", expand=True)

        # Scrollable canvas for images
        self.canvas = tk.Canvas(self.image_frame, bg="#f0f8ff")
        self.scrollbar = tk.Scrollbar(self.image_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f8ff")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="top", fill="both", expand=True)
        self.scrollbar.pack(side="bottom", fill="x")

    def show_images(self):
        input_text = self.entry.get().strip().upper()

        # Validate input
        if not input_text.isalpha():
            messagebox.showerror("Invalid Input", "Please enter only letters A-Z.")
            return

        # Choose correct dataset based on selection
        selected_language = self.language_var.get()
        if selected_language == "ASL":
            dataset_path = asl_dir
        elif selected_language == "ISL":
            dataset_path = isl_dir
        else:
            messagebox.showerror("Language Error", "Unknown language selected.")
            return

        # Clear previous images
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Display images
        for char in input_text:
            character_folder = os.path.join(dataset_path, char)

            if not os.path.exists(character_folder):
                messagebox.showerror("Folder Error", f"No folder found for '{char}' in {selected_language}.")
                continue

            image_files = [f for f in os.listdir(character_folder) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
            if not image_files:
                messagebox.showerror("No Images", f"No images found for '{char}' in {selected_language}.")
                continue

            selected_image = random.choice(image_files)
            image_path = os.path.join(character_folder, selected_image)

            try:
                # Load and resize the image
                img = Image.open(image_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)

                img_label = tk.Label(self.scrollable_frame, image=img, bg="#f0f8ff")
                img_label.image = img  # Keep reference
                img_label.pack(side=tk.LEFT, padx=10, pady=10)

            except Exception as e:
                messagebox.showerror("Image Error", f"Error loading image for '{char}': {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageImageApp(root)
    root.mainloop()
