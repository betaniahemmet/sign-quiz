import os
import random
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from pathlib import Path

# Define the path to the folder containing videos
video_folder = Path("./mov")

# Get a list of all video files in the folder
video_files = [file.name for file in video_folder.iterdir() if file.is_file()]

# Initialize the Tkinter window
root = tk.Tk()
root.title("Gissa tecknet!")

# Create a canvas to display the video
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

# Create a label to display the question
question_label = tk.Label(root, text="Vilket tecken visas i filmen?")
question_label.pack()

# Create a list of four buttons for user choices
choice_buttons = []

# Initialize the question counter
question_counter = 0


# Function to handle user's choice
def check_choice(choice):
    global question_counter
    if choice == correct_choice:
        question_counter += 1
        if question_counter >= 15:
            result_label.config(text="Du vann! Spelet är slut")
            for button in choice_buttons:
                button.config(state=tk.DISABLED)  # Disable all choice buttons
        else:
            result_label.config(text="Rätt! Snart kommer nästa fråga...")
            root.after(
                3000, new_question
            )  # Pause for 3000 milliseconds (3 seconds) and move to the next question
    else:
        result_label.config(text="Nästan rätt! Försök igen.")


# Function to set up a new question
def new_question():
    global correct_choice, question_counter
    random_files = random.sample(video_files, 4)
    correct_choice = random_files[0]
    choices = random.sample(random_files, 4)
    random.shuffle(choices)

    # Load and display the video
    video_path = os.path.join(video_folder, correct_choice)
    cap = cv2.VideoCapture(video_path)

    def update_video():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            canvas.create_image(0, 0, anchor=tk.NW, image=img)
            canvas.img = img
            # Schedule the next update after 30 milliseconds (normal video frame rate)
            root.after(30, update_video)
        else:
            cap.release()
            canvas.delete("all")
            result_label.config(text="")
            update_choice_buttons(choices)

    def update_choice_buttons(choices):
        for i, choice in enumerate(choices):
            button_text = choice.split(".")[0].capitalize()
            choice_buttons[i].config(
                text=button_text,
                command=lambda c=choice: check_choice(c),
                state=tk.NORMAL,
            )  # Enable choice buttons

    def disable_choice_buttons():
        for button in choice_buttons:
            button.config(
                state=tk.DISABLED
            )  # Disable choice buttons while video is playing

    # Start video playback
    disable_choice_buttons()
    update_video()


# Create buttons for choices
for _ in range(4):
    button = tk.Button(
        root, text="", command=lambda: None, state=tk.DISABLED
    )  # Initially disable choice buttons
    choice_buttons.append(button)
    button.pack()

# Create a label to display the result
result_label = tk.Label(root, text="")
result_label.pack()

# Start the game with the first question
new_question()

# Run the Tkinter main loop
root.mainloop()
