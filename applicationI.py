import customtkinter as ctk
from realtime_detectionI import update_frame, release_video  
import warnings

warnings.filterwarnings("ignore")

# Initialize customtkinter with a theme and color mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create the main window
root = ctk.CTk()
root.title("AI Webcam Viewer & Prediction")

# Set window size and position
w, h = 600, 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - w) // 2
y = (screen_height - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")

# Configure grid layout for better structure
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Title Label
title_label = ctk.CTkLabel(root, text="Indian Sign Language", font=("Arial", 24, "bold"))
title_label.grid(row=0, column=0, pady=(20, 10))

# Video Feed Label
video_label = ctk.CTkLabel(root, text="")
video_label.grid(row=1, column=0, padx=20, pady=10)

# Prediction Display Text Area
text_area = ctk.CTkTextbox(root, width=540, height=150, font=("Arial", 20, "bold"))
text_area.grid(row=2, column=0 , padx=20, pady=(10, 20))

# Start video stream within the application
update_frame(video_label, text_area)

# Start the main application loop
root.mainloop()

# Release the video capture when the window is closed
release_video()