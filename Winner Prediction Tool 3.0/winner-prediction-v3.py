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
import subprocess
from PIL import ImageTk, Image
import numpy as np
import sklearn.preprocessing as labelEncoder
from sklearn.model_selection import train_test_split


def restart_app():
    # Use a list for the command and arguments, avoiding the need to manually handle escaping
    cmd = [sys.executable] + sys.argv
    subprocess.Popen(cmd)
    root.destroy()

# App will contain a slider, a file browser and two entries with label which shows the win percentage of both players

# Function to calculate the win percentage of the players


model1 = joblib.load('rf_model.pkl')
model2 = joblib.load('lr_model.pkl')
custom_model = joblib.load('rf_model.pkl')

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


def browse_model_file():
    global custom_model

    # Opening the file browser
    file_path = askopenfile(mode='r', filetypes=[(
        'Pickle Files', '*.pkl'), ("Joblib Files", '*.joblib'), ("Keras Files", '*.h5'), ("Tensorflow Files", '*.h5')])
    path = file_path.name
    file_path2_entry.config(state="normal")
    # Displaying the file path in the entry widget
    file_path2_entry.delete(0, tk.END)
    file_path2_entry.insert(0, path)
    file_path2_entry.config(state="readonly")

    if model_train_status_var.get() == "Trained":
        custom_model = joblib.load(file_path2_entry.get())
    else:
        print("training model")
        custom_model = train_model(joblib.load(file_path2_entry.get()))


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
    if model_var.get() == "Random Forest" and model_type_var.get() == "Built-in Models":
        values = model1.predict_proba(X)
    elif model_var.get() == "Logistic Regression" and model_type_var.get() == "Built-in Models":
        values = model2.predict_proba(X)
    elif model_type_var.get() == "Upload Custom Models":
        values = custom_model.predict_proba(X)
    else:
        values = [[0, 0]]
    # round values to 2 places
    values = [[round(i, 2) for i in values[0]]]
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
    if model_var.get() == "Random Forest" and model_type_var.get() == "Built-in Models":
        values = model1.predict_proba(X)
    elif model_var.get() == "Logistic Regression" and model_type_var.get() == "Built-in Models":
        values = model2.predict_proba(X)
    elif model_type_var.get() == "Upload Custom Models":
        values = custom_model.predict_proba(X)
    else:
        values = [[0, 0]]
    # round values to 2 places
    values = [[round(i, 2) for i in values[0]]]
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
    if model_var.get() == "Random Forest" and model_type_var.get() == "Built-in Models":
        values = model1.predict_proba(X)
    elif model_var.get() == "Logistic Regression" and model_type_var.get() == "Built-in Models":
        values = model2.predict_proba(X)
    elif model_type_var.get() == "Upload Custom Models":
        values = custom_model.predict_proba(X)
    else:
        values = [[0, 0]]
    # round values to 2 places
    values = [[round(i, 2) for i in values[0]]]
    print(values)
    time_progressed = nearest_rows['Time Elapsed (minutes:seconds)'].values[0]
    # get frame value and store in i
    i = nearest_rows['Frame'].values[0]

    live_frames_label.config(text="Frame: " + str(i) +
                             "\nTime Elapsed : " + str(time_progressed) + " Minutes")

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


def update_widgets(event):
    selected_value = combobox_model2.get()
    if selected_value == "Built-in Models":
        combobox_model.grid(pady=5, row=6, column=1)
        browse_model_button.grid_remove()
        file_path2_entry.grid_remove()
    else:
        combobox_model.grid_remove()
        browse_model_button.grid(pady=5, row=6, column=1)
        file_path2_entry.grid(pady=5, row=6, column=2)
        file_path2_entry.delete(0, tk.END)
        file_path2_entry.insert(0, "Select a File To View Path")
        file_path2_entry.config(state="disabled")
        combobox_model3.grid(pady=5, row=5, column=2)


def train_model(model):
    # model_train_status_var

    data = pd.read_csv('150 Game Training Data.csv')
    # Drop zero winner rows
    data = data.drop(data[data['Winner'] == 0].index)
    data.value_counts("ReplayID").count()
    data["Time Elapsed (minutes:seconds)"]
    # Label encode replayID
    le = labelEncoder.LabelEncoder()
    data['ReplayID'] = le.fit_transform(data['ReplayID'])
    data['Player'] = le.fit_transform(data['Player'])
    data['Enemy Player'] = le.fit_transform(data['Enemy Player'])
    X = data.drop(['Winner', 'Time Elapsed (minutes:seconds)'], axis=1)
    y = data['Winner']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42)
    # get non integer columns
    non_int_columns = X.select_dtypes(include=['object']).columns
    non_int_columns
    clf = model

    clf.fit(X, y)

    return model


# Creating the main window
root = tk.Tk()

# Setting the title and size of the window
root.title("Winner Prediction Tool")
root.geometry("705x325")

# Create a canvas to hold the background image
canvas = tk.Canvas(root, width=700, height=320)
# canvas on full grid
canvas.grid(row=0, column=0, rowspan=9, columnspan=3)

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
heading_label = tk.Label(root, text="StarCraft Winner Prediction v3",
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

model_var = tk.StringVar(value="Select ML Model")
model_type_var = tk.StringVar(value="Select ML Model Type")
model_train_status_var = tk.StringVar(value="Select Model Train Status")

# Model Type Selector
label_model_selector = ttk.Label(root, text="Model Type", font=(
    "Arial", 10, "bold"), foreground="white", background="black")
label_model_selector.grid(pady=5, row=5, column=0)

# Model Selection Combobox
combobox_model2 = ttk.Combobox(root, textvariable=model_type_var, values=[
    "Built-in Models", "Upload Custom Models"])
combobox_model2.grid(pady=5, row=5, column=1)
combobox_model2.bind("<<ComboboxSelected>>", update_widgets)

combobox_model3 = ttk.Combobox(root, textvariable=model_train_status_var, values=[
    "Trained", "Not Trained"])
# incrase width of combobox
combobox_model3.config(width=25)

# Creating a button to browse the file
browse_model_button = tk.Button(root, text="Browse Model File",
                                command=browse_model_file, width=16)

# Creating an entry widget to display the file path
file_path2_entry = tk.Entry(root, width=30)


# Model Selector
label_model_selector = ttk.Label(root, text="Prediction Model Selector", font=(
    "Arial", 10, "bold"), foreground="white", background="black")
label_model_selector.grid(pady=5, row=6, column=0)

# Model Selection Combobox
combobox_model = ttk.Combobox(root, textvariable=model_var, values=[
                              "Random Forest", "Logistic Regression"])
combobox_model.grid(pady=5, row=6, column=1)


winner_label = ttk.Label(root, text="Winner % of Player")
winner_label.grid(pady=5, row=8, column=0)

# Creating a label for the win percentage of player 1
player1_win_percentage_label = ttk.Label(root, text="Player 1 Win Percentage")
player1_win_percentage_label.grid(
    pady=5, row=7, column=1)  # Place in row 0, column 0

# Creating an entry widget to display the win percentage of player 1
player1_win_percentage = tk.Entry(root)
# Place in row 0, column 1
player1_win_percentage.grid(pady=7, row=8, column=1)
player1_win_percentage.config(state="disabled")

# Creating a label for the win percentage of player 2
player2_win_percentage_label = ttk.Label(root, text="Player 2 Win Percentage")
player2_win_percentage_label.grid(
    pady=5, row=7, column=2)  # Place in row 0, column 2

# Creating an entry widget to display the win percentage of player 2
player2_win_percentage = tk.Entry(root)
# Place in row 0, column 3
player2_win_percentage.grid(pady=5, row=8, column=2)
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
