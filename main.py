# whack_a_mole_apcsp.py
from tkinter import *
from tkinter.ttk import *
import random
import os

# Constants
TICK_SPEED = 1000
MOLE_INTERVAL = 600
EASY = 1000
MEDIUM = 600
HARD = 300
IMPOSSIBLE = 100
TIME_LIMIT = 30

# Global state
time_left = TIME_LIMIT
score_number = 0
mole_spots = []
selected_speed = MEDIUM
selected_difficulty = "Medium"

# Setup main window
window = Tk()
window.title("Whack-a-Mole")
window.geometry("800x600")
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)

# Images
mole_image_path = os.path.join(os.path.dirname(__file__), "mole.png")
mole_image = PhotoImage(file=mole_image_path).subsample(5, 5)

red_circle_path = os.path.join(os.path.dirname(__file__), "red_circle.png")
red_circle_image = PhotoImage(file=red_circle_path).subsample(3, 3)

# Frames
menu_frame = Frame(window)
game_frame = Frame(window)
end_frame = Frame(window)
instructions_frame = Frame(window)

# Student-developed procedure
def evaluate_click(event, is_mole, multiplier):
    global score_number
    if is_mole:
        for _ in range(multiplier):
            score_number += 1
    else:
        score_number -= 1
    score.config(text=f"Your score is: {score_number}")

# Timer logic
def master_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        time_bar["value"] = time_left
        timer_label.config(text=f"{time_left} seconds left")
        window.after(TICK_SPEED, master_timer)
    else:
        end_game()

# Show mole randomly

def mole_appear():
    for spot in mole_spots:
        spot.config(image=red_circle_image)
        spot.image = red_circle_image
        spot.bind("<Button-1>", lambda event: evaluate_click(event, False, 0))

    target = random.choice(mole_spots)
    target.config(image=mole_image)
    target.image = mole_image
    target.bind("<Button-1>", lambda event: evaluate_click(event, True, 1))

    window.after(selected_speed, mole_appear)

# Start game from menu
def start_game():
    global time_left, score_number
    time_left = TIME_LIMIT
    score_number = 0
    score.config(text=f"Your score is: {score_number}")
    difficulty_label.config(text=f"Difficulty: {selected_difficulty}")
    timer_label.config(text=f"{TIME_LIMIT} seconds left")
    time_bar["value"] = TIME_LIMIT

    menu_frame.pack_forget()
    instructions_frame.pack_forget()
    end_frame.pack_forget()
    game_frame.pack(fill=BOTH, expand=True)

    master_timer()
    mole_appear()

# Set difficulty from menu
def set_difficulty_and_start(speed, label):
    global selected_speed, selected_difficulty
    selected_speed = speed
    selected_difficulty = label
    start_game()

# End game and show end screen
def end_game():
    game_frame.pack_forget()
    for spot in mole_spots:
        spot.unbind("<Button-1>")
    final_score.config(text=f"Game Over! Final score: {score_number}")
    end_frame.pack(fill=BOTH, expand=True)

# Show instructions screen
def show_instructions():
    menu_frame.pack_forget()
    instructions_frame.pack(fill=BOTH, expand=True)

# Quit app
def quit_game():
    window.destroy()

# Menu screen
menu_label = Label(menu_frame, text="Whack-a-Mole", font=('Arial', 28))
menu_label.pack(pady=20)
Label(menu_frame, text="Select Difficulty", font=('Arial', 20)).pack(pady=10)
Button(menu_frame, text="Easy", command=lambda: set_difficulty_and_start(EASY, "Easy")).pack(pady=5)
Button(menu_frame, text="Medium", command=lambda: set_difficulty_and_start(MEDIUM, "Medium")).pack(pady=5)
Button(menu_frame, text="Hard", command=lambda: set_difficulty_and_start(HARD, "Hard")).pack(pady=5)
Button(menu_frame, text="Impossible", command=lambda: set_difficulty_and_start(IMPOSSIBLE, "Impossible")).pack(pady=5)
Button(menu_frame, text="Instructions", command=show_instructions).pack(pady=10)
Button(menu_frame, text="Quit", command=quit_game).pack(pady=20)
menu_frame.pack(fill=BOTH, expand=True)

# Instructions screen
Label(instructions_frame, text="Instructions", font=('Arial', 28)).pack(pady=20)
Label(instructions_frame, text="Click on the mole to gain points.\nClicking on a red circle loses you points!", font=('Arial', 18)).pack(pady=10)
Button(instructions_frame, text="Back to Menu", command=lambda: [instructions_frame.pack_forget(), menu_frame.pack(fill=BOTH, expand=True)]).pack(pady=20)

# Game screen
Label(game_frame, text="Hit the moles to score points!", font=('Arial', 20)).grid(row=0, column=6)
score = Label(game_frame, text=f"Your score is: {score_number}", font=('Arial', 18))
score.grid(row=1, column=6)
difficulty_label = Label(game_frame, text=f"Difficulty: {selected_difficulty}", font=('Arial', 18))
difficulty_label.grid(row=2, column=6)
Label(game_frame, text="Time remaining:", font=('Arial', 18)).grid(row=3, column=6)
time_bar = Progressbar(game_frame, length=100, mode="determinate", orient="horizontal", maximum=TIME_LIMIT)
time_bar.grid(row=4, column=6)
timer_label = Label(game_frame, text=f"{TIME_LIMIT} seconds left", font=('Arial', 16))
timer_label.grid(row=5, column=6)

positions = [(10, 1), (10, 6), (10, 12), (30, 1), (30, 6), (30, 12)]
for row, col in positions:
    lbl = Label(game_frame, image=red_circle_image)
    lbl.grid(row=row, column=col)
    mole_spots.append(lbl)

# End screen
final_score = Label(end_frame, text="", font=('Arial', 24))
final_score.pack(pady=30)
menu_button = Button(end_frame, text="Return to Menu", command=lambda: [end_frame.pack_forget(), menu_frame.pack(fill=BOTH, expand=True)])
menu_button.pack(pady=10)
Button(end_frame, text="Quit", command=quit_game).pack(pady=10)

# Run window
window.mainloop()
