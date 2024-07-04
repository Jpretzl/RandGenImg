import random
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageDraw, ImageTk
import time

target_image = [
    "WWWWWRRRRRRWWWWW",
    "WWWWRRRRRRRRRRWW",
    "WWWWBBBSSS0SWWWW",
    "WWWBSBSSSS0SSSWW",
    "WWWBSBSSSSS0SSSW",
    "WWWBBSSSSS0000WW",
    "WWWWWSSSSSSSSWWW",
    "WWWWRRbRRbRWWWWW",
    "WWWRRRbRRbRRRWWW",
    "WWRRRRbbbbRRRRWW",
    "WWSSRbYbbYbRSSWW",
    "WWSSSbbbbbbSSSWW",
    "WWSSbbbbbbbbSSWW",
    "WWWWbbbWWbbbWWWW",
    "WWWBBBBWWBBBBWWW",
    "WWBBBBBWWBBBBBWW"
]

colors = {
    'R': (255, 0, 0),
    'S': (255, 224, 189),
    'W': (255, 255, 255),
    'B': (150, 75, 0),
    ' ': (255, 255, 255),
    'b': (0, 0, 255),
    '0': (0, 0, 0),
    'Y': (255, 255, 0)
}

target_pixels = [(x, y, colors[pixel]) for y, row in enumerate(target_image) for x, pixel in enumerate(row) if pixel != ' ']

root = tk.Tk()
root.title("Pixel Art Evolution")

frame = tk.Frame(root)
frame.pack()

canvas = tk.Canvas(frame, width=256, height=256)
canvas.grid(row=0, column=0, padx=5, pady=5)

log_widget = scrolledtext.ScrolledText(frame, width=50, height=20, state='disabled')
log_widget.grid(row=0, column=1, padx=5, pady=5)

image = Image.new('RGB', (16, 16), 'white')
draw = ImageDraw.Draw(image)

correct_pixels = set()

running = False

def update_image():
    img_resized = image.resize((256, 256), Image.NEAREST)
    img_tk = ImageTk.PhotoImage(img_resized)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk

def randomize_pixels():
    for _ in range(100):
        x, y = random.randint(0, 15), random.randint(0, 15)
        if (x, y) not in correct_pixels:
            color = random.choice(list(colors.values()))
            draw.point((x, y), fill=color)

def evaluate_image():
    pixels = image.load()
    score = 0
    for (x, y, color) in target_pixels:
        if pixels[x, y] == color:
            score += 1
            correct_pixels.add((x, y))
    return score

def log_message(message):
    log_widget.config(state='normal')
    log_widget.insert(tk.END, message + "\n")
    log_widget.config(state='disabled')
    log_widget.yview(tk.END)

def evolve():
    global running
    best_score = 0
    generation = 0
    while running and best_score < len(target_pixels):
        randomize_pixels()
        score = evaluate_image()
        if score > best_score:
            best_score = score
            log_message(f"Generation {generation}: New best score: {best_score}")
        generation += 1
        update_image()
        root.update_idletasks()
        root.update()
        time.sleep(0.25)
        if not running:
            break

def start():
    global running
    if not running:
        running = True
        root.after(0, evolve)

def pause():
    global running
    running = False

start_button = tk.Button(root, text="Start", command=start)
start_button.pack(side=tk.LEFT, padx=5, pady=5)

pause_button = tk.Button(root, text="Pause", command=pause)
pause_button.pack(side=tk.RIGHT, padx=5, pady=5)

root.mainloop()
