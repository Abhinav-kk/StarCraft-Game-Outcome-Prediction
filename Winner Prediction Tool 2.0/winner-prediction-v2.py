# Winner Prediction Tool using Tkinter

# Importing the required libraries
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfile
import pandas as pd
import joblib
from tkinter import font as tkFont
import os
import sys
from PIL import ImageTk, Image


def restart_app():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# App will contain a slider, a file browser and two entries with label which shows the win percentage of both players

# Function to calculate the win percentage of the players


model = joblib.load('rf_model.pkl')


# Function to browse the file
def browse_file():
    # Opening the file browser
    file_path = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
    path = file_path.name
    file_path_entry.config(state="normal")
    # Displaying the file path in the entry widget
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, path)
    file_path_entry.config(state="readonly")


def read_update_slider():
    data = pd.read_csv(file_path_entry.get())
    percentile_80_grouped = data.groupby(
        'ReplayID')['Frame'].quantile(player1_slider.get()/100)
    print(player1_slider.get()/100)
    # Define a function to find the row with the closest 'Frame' value to the 80th percentile within each group

    def find_nearest_row(group):
        nearest_index = (
            group['Frame'] - percentile_80_grouped[group.name]).abs().idxmin()
        return group.loc[[nearest_index]]

    # Apply the function to each group of 'ReplayID' and concatenate the results
    nearest_rows = data.groupby(
        'ReplayID', group_keys=False).apply(find_nearest_row)

    # Reset the index if needed
    nearest_rows.reset_index(drop=True, inplace=True)
    X = nearest_rows.drop(['Time Elapsed (minutes:seconds)'], axis=1)
    X["ReplayID"] = 1
    X["Player"] = 0
    X["Enemy Player"] = 1
    values = model.predict_proba(X)
    print(values)

    player1_win_percentage.config(state=tk.NORMAL)
    player2_win_percentage.config(state=tk.NORMAL)

    player1_win_percentage.delete(0, tk.END)
    player1_win_percentage.insert(0, str(values[0][0]*100))

    player2_win_percentage.delete(0, tk.END)
    player2_win_percentage.insert(0, str(values[0][1]*100))

    player1_win_percentage.config(state=tk.DISABLED)
    player2_win_percentage.config(state=tk.DISABLED)


def read_update_auto():
    data = pd.read_csv(file_path_entry.get())
    percentile_80_grouped = data.groupby(
        'ReplayID')['Frame'].quantile(player1_slider.get()/100)
    print(player1_slider.get()//100)
    # Define a function to find the row with the closest 'Frame' value to the 80th percentile within each group

    def find_nearest_row(group):
        nearest_index = (
            group['Frame'] - percentile_80_grouped[group.name]).abs().idxmin()
        return group.loc[[nearest_index]]

    # Apply the function to each group of 'ReplayID' and concatenate the results
    nearest_rows = data.groupby(
        'ReplayID', group_keys=False).apply(find_nearest_row)

    # Reset the index if needed
    nearest_rows.reset_index(drop=True, inplace=True)
    X = nearest_rows.drop(['Time Elapsed (minutes:seconds)'], axis=1)
    X["ReplayID"] = 1
    X["Player"] = 0
    X["Enemy Player"] = 1
    values = model.predict_proba(X)
    print(values)

    player1_win_percentage.config(state=tk.NORMAL)
    player2_win_percentage.config(state=tk.NORMAL)

    player1_win_percentage.delete(0, tk.END)
    player1_win_percentage.insert(0, str(values[0][0]*100))

    player2_win_percentage.delete(0, tk.END)
    player2_win_percentage.insert(0, str(values[0][1]*100))

    player1_win_percentage.config(state=tk.DISABLED)
    player2_win_percentage.config(state=tk.DISABLED)


def read_update_Live():
    data = pd.read_csv(file_path_entry.get())

    # Take last row
    nearest_rows = data.tail(1)
    # print(data)
    X = nearest_rows.drop(['Time Elapsed (minutes:seconds)'], axis=1)
    X["ReplayID"] = 1
    X["Player"] = 0
    X["Enemy Player"] = 1
    values = model.predict_proba(X)
    print(values)

    # get frame value and store in i
    i = nearest_rows['Frame'].values[0]

    live_frames_label.config(text="Frame: " + str(i))

    player1_win_percentage.config(state=tk.NORMAL)
    player2_win_percentage.config(state=tk.NORMAL)

    player1_win_percentage.delete(0, tk.END)
    player1_win_percentage.insert(0, str(values[0][0]*100))

    player2_win_percentage.delete(0, tk.END)
    player2_win_percentage.insert(0, str(values[0][1]*100))

    player1_win_percentage.config(state=tk.DISABLED)
    player2_win_percentage.config(state=tk.DISABLED)


def show_message():
    # Getting the win percentage of the players
    player1_win = player1_win_percentage.get()
    player2_win = player2_win_percentage.get()

    # Getting the file path
    file_path = file_path_entry.get()

    # Displaying the message box
    messagebox.showinfo("Prediction Result", "Player 1 Win Percentage: " + player1_win +
                        "\nPlayer 2 Win Percentage: " + player2_win + "\nFile Path: " + file_path)


def startGameSlider():
    read_update_slider()


def startGameAuto(i=0):
    if i <= 100:
        print(i)
        player1_slider.set(i)
        # Update the slider and process other pending events
        player1_slider.update_idletasks()
        read_update_auto()
        show_label.config(text="Game Progression: " + str(i) + "%")
        # Schedule the next call to this function after 500 milliseconds
        root.after(500, startGameAuto, i+1)


def startGameLive():
    read_update_Live()
    # Schedule the next call to this function after 500 milliseconds
    root.after(1000, startGameLive)


# Creating the main window
root = tk.Tk()

# Setting the title and size of the window
root.title("Winner Prediction Tool")
root.geometry("705x305")

# Create a canvas to hold the background image
canvas = tk.Canvas(root, width=700, height=300)
# canvas on full grid
canvas.grid(row=0, column=0, rowspan=7, columnspan=3)

# Load the background image with PIL
# Change to the path of your image file
bg_image_path = os.getcwd() + "/starcraft-wallpaper.jpg"
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1000, 517))  # Resize the image to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Add image to the Canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create a frame to hold the widgets
frame0 = ttk.Frame(canvas)  # Define the size of frame0

# Place the frame on the canvas; this allows for easy placement and layering
canvas.create_window(500, 258.5, window=frame0, anchor='center')

s = ttk.Style()

root.wm_attributes('-transparentcolor', '#ab23ff')
# Create style used by default for all Frames
s.configure('TFrame', background='black')
s.configure('TLabel', background='black',
            foreground="white", font=("Arial", 10, "bold"))
s.configure('TButton', background='black',
            foreground="white", font=("Arial", 10, "bold"))
s.configure('TEntry', background='black',
            foreground="white", font=("Arial", 10, "bold"))
s.configure('TScale', background='black',
            foreground="white", font=("Arial", 10, "bold"))


customFont = tkFont.Font(family="Helvetica", size=15, weight="bold")
heading_label = tk.Label(root, text="StarCraft Winner Prediction v2",
                         font=customFont, bg='black', fg='white')
heading_label.grid(pady=5, row=0, column=1)

# Creating a label for the player 1
player1_label = ttk.Label(root, text="Replay Game Progression")
player1_label.grid(pady=5, row=2, column=0)

# Creating a slider for player 1
player1_slider = ttk.Scale(root, from_=0, to=100,
                           orient="horizontal", length=200)
player1_slider.grid(pady=5, row=2, column=1)

# Show label for showing slider value
show_label = ttk.Label(root, text="Game Progression: 0%")
show_label.grid(pady=5, row=2, column=2)

# Function to show the value of the slider


def show_value(value):
    show_label.config(text="Game Progression: " + str(int(value//1)) + "%")


# Binding the slider to the show_value function
player1_slider.bind("<Motion>", lambda x: show_value(player1_slider.get()))

replay_type_label = ttk.Label(root, text="Replay Based Predictions")
replay_type_label.grid(pady=5, row=1, column=0)

# Creating a button to calculate the win percentage
calculate_button = tk.Button(
    root, text="Calculate Replay Win Percentage Slider", command=startGameSlider)
calculate_button.grid(pady=5, row=1, column=1)

# Creating a button to calculate the win percentage
calculate_button = tk.Button(
    root, text="Calculate Replay Win Percentage Auto", command=startGameAuto)
calculate_button.grid(pady=5, row=1, column=2)

live_type_label = ttk.Label(root, text="Live Real-Time Predictions")
live_type_label.grid(pady=5, row=3, column=0)
# Creating a button to calculate the win percentage
calculate_button = tk.Button(
    root, text="Calculate Live Win Percentage", command=startGameLive)
calculate_button.grid(pady=5, row=3, column=1)

# Show label for showing slider value
live_frames_label = ttk.Label(root, text="Frames: 0")
live_frames_label.grid(pady=5, row=3, column=2)

winner_label = ttk.Label(root, text="Winner % of Player")
winner_label.grid(pady=5, row=6, column=0)

# Creating a label for the win percentage of player 1
player1_win_percentage_label = ttk.Label(root, text="Player 1 Win Percentage")
player1_win_percentage_label.grid(
    pady=5, row=5, column=1)  # Place in row 0, column 0

# Creating an entry widget to display the win percentage of player 1
player1_win_percentage = tk.Entry(root)
# Place in row 0, column 1
player1_win_percentage.grid(pady=7, row=6, column=1)
player1_win_percentage.config(state="disabled")

# Creating a label for the win percentage of player 2
player2_win_percentage_label = ttk.Label(root, text="Player 2 Win Percentage")
player2_win_percentage_label.grid(
    pady=5, row=5, column=2)  # Place in row 0, column 2

# Creating an entry widget to display the win percentage of player 2
player2_win_percentage = tk.Entry(root)
# Place in row 0, column 3
player2_win_percentage.grid(pady=5, row=6, column=2)
player2_win_percentage.config(state="disabled")

# Creating a button to browse the file
browse_button = tk.Button(root, text="Browse File",
                          command=browse_file, width=16)
browse_button.grid(pady=5, row=4, column=0)

# Creating an entry widget to display the file path
file_path_entry = tk.Entry(root, width=30)
file_path_entry.grid(pady=5, row=4, column=1)
file_path_entry.delete(0, tk.END)
file_path_entry.insert(0, "Select a File To View Path")
file_path_entry.config(state="disabled")

# Restart button
restart_button = tk.Button(root, text="Reload App",
                           command=restart_app, width=15, background='red')
restart_button.grid(pady=5, row=0, column=2)

# Running the main loop
root.mainloop()

# End of code