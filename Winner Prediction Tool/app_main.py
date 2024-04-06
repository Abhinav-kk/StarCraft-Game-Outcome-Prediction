import tkinter as tk
from tkinter import ttk
from tkinter import END
from ai_model import predict_simple, predict_gameState
import os
from tkinter import font as tkFont
from PIL import ImageTk, Image
from tkinter import filedialog

# Create the main window
root = tk.Tk()
root.title("StarCraft Winner Prediction")
root.geometry("1000x517+0+0")

# Create a canvas to hold the background image
canvas = tk.Canvas(root, width=1000, height=517)
canvas.pack(fill="both", expand=True)

# Load the background image with PIL
bg_image_path = os.getcwd() + "/starcraft-wallpaper.jpg"  # Change to the path of your image file
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1000, 517))  # Resize the image to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Add image to the Canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create a frame to hold the widgets
frame0 = ttk.Frame(canvas)  # Define the size of frame0

# Place the frame on the canvas; this allows for easy placement and layering
canvas.create_window(500, 258.5, window=frame0, anchor='center')

# Create a custom font style
customFont = tkFont.Font(family="Helvetica", size=20, weight="bold")

heading_label = tk.Label(root, text="StarCraft Winner Prediction", font=customFont, bg='black', fg='white')
heading_label.place(width=500, height=50, x=200, y=20)

# Variables
model_var = tk.StringVar(value="Select")
feature_var = tk.StringVar(value="Select")
player1_race_var = tk.StringVar(value="Player 1 Race")
player2_race_var = tk.StringVar(value="Player 2 Race")

# Race Selector Label
label_race_selector = ttk.Label(root, text="Race Selector", font=("Arial", 10,"bold"), foreground="white", background="black")
label_race_selector.place(width=105, height=25, x=38, y=80)

# Player 1 Race Combobox
combobox_player1_race = ttk.Combobox(root, textvariable=player1_race_var, values=["Protoss", "Terran", "Zerg"])
combobox_player1_race.place(width=118, height=25, x=150, y=80)

# Player 2 Race Combobox
combobox_player2_race = ttk.Combobox(root, textvariable=player2_race_var, values=["Protoss", "Terran", "Zerg"])
combobox_player2_race.place(width=118, height=25, x=286, y=80)

# Model Selector
label_model_selector = ttk.Label(root,text="Model Selector", font=("Arial", 10,"bold"), foreground="white", background="black")
label_model_selector.place(width=100, height=25, x=430, y=80)

# Model Selection Combobox
combobox_model = ttk.Combobox(root, textvariable=model_var, values=["Random Forest", "K-Nearest Neighbors", "Support Vector Classification", "Logistic Regression", "Decision Trees"])
combobox_model.place(width=160, height=25, x=550, y=80)

# Input Features Selector
label_input_features = ttk.Label(root, text="Input Features", font=("Arial", 10,"bold"), foreground="white", background="black")
label_input_features.place(width=121, height=25, x=725, y=80)

# Input Features Combobox
combobox_input_features = ttk.Combobox(root,textvariable=feature_var, values=["Simple", "Game State"])
combobox_input_features.place(width=118, height=25, x=852, y=80)
combobox_input_features.bind('<<ComboboxSelected>>', lambda event: show_frame(combobox_input_features.get()))

s = ttk.Style()

root.wm_attributes('-transparentcolor', '#ab23ff')
# Create style used by default for all Frames
s.configure('TFrame', background='black')
s.configure('TLabel', background='black', foreground="white", font=("Arial",10,"bold") )

# Creating two frames as an example
frame1 = ttk.Frame(frame0, width=1000, height=50)
frame2 = ttk.Frame(frame0, width=1000, height=50)

# Storing the frames in a dict makes it easier to switch between them
frames = {'Simple': frame1, 'Game State': frame2}

def show_frame(name):
    frame0.config(width=800, height=300)
    # Unpack all frames
    for frame in frames.values():
        frame.place_forget()
    # Place the selected frame
    frame = frames[name]
    frame.place(x=50, y=10, width=1170, height=717)
    print("Showing frame", name)


##################################### FRAME 1 ############################################
# Create Entries
entries = {
    'p1_alive_units': ttk.Entry(frame1),
    'p2_alive_units': ttk.Entry(frame1),
    'p1_supply_used': ttk.Entry(frame1),
    'p2_supply_used': ttk.Entry(frame1),
    'p1_gas': ttk.Entry(frame1),
    'p2_gas': ttk.Entry(frame1),
    'p1_minerals': ttk.Entry(frame1),
    'p2_minerals': ttk.Entry(frame1),
    'p1_winner_percent': ttk.Entry(frame1),
    'p2_winner_percent': ttk.Entry(frame1),
}

# Label for Player 1 and Player 2 above their race Comboboxes
label_player1 = ttk.Label(frame1, text="Player 1")
# label_player1.place(width=91, height=28, x=150, y=50)
label_player1.grid(row=0, column=1, padx=5, pady=5)

label_player2 = ttk.Label(frame1, text="Player 2")
# label_player2.place(width=91, height=28, x=286, y=50)
label_player2.grid(row=0, column=2, padx=5, pady=5)

# Labels for the entry fields
labels_text = [
    "Alive Units", "Supply Used", "Gas", "Minerals", "Winner %"
]

# Calculate placement for labels
for i, text in enumerate(labels_text):
    row = i + 1
    label = ttk.Label(frame1, text=text)
    # label.place(x=30, y=100 + 30*row, height=25)
    label.grid(row=row, column=0, padx=5, pady=5)

# Place Entries on the screen with calculated positions
for i, (name, entry) in enumerate(entries.items()):
    row = i // 2 + 1
    col = i % 2 + 1
    entry.grid(row=row, column=col, padx=5, pady=5)
    # entry.place(width=85, height=25, x=150 + 135*col, y=100 + 30*row)

entries["p1_winner_percent"].config(state= "disabled")
entries["p2_winner_percent"].config(state= "disabled")

def print_values1():
    # Print ComboBox values
    print("Player 1 Race:", combobox_player1_race.get())
    print("Player 2 Race:", combobox_player2_race.get())
    print("Selected Model:", combobox_model.get())
    print("Input Features:", combobox_input_features.get())

    inputs = [combobox_player1_race.get(), combobox_player2_race.get()]
    # Print Entry values
    for name, entry in entries.items():
        print(f"{name}: {entry.get()}")
        inputs.append(entry.get())

    # call predict winner with data as input as pandas input
    # with columns ["Player1_Race","Player2_Race","Player1_AliveUnits","Player2_AliveUnits","Player1_SupplyUsed","Player2_SupplyUsed","Player1_Gas","Player1_Gas", "Player1_Minerals", "Player2_Minerals"]
    # return the winner percentage for player 1 and player 2

    result = predict_simple(inputs,combobox_model.get())
    print("recieved results", result)
    update_winner_percent(entries,result[0], result[1])

def update_winner_percent(entry,a,b):
    entry["p1_winner_percent"].config(state=tk.NORMAL)

    entry["p1_winner_percent"].delete(0, tk.END)
    entry["p1_winner_percent"].insert(0, a)


    entry["p2_winner_percent"].config(state=tk.NORMAL)

    entry["p2_winner_percent"].delete(0, tk.END)
    entry["p2_winner_percent"].insert(0, b)

    entry["p1_winner_percent"].config(state=tk.DISABLED)
    entry["p2_winner_percent"].config(state=tk.DISABLED)

# Predict Winner Button
button_predict_winner = ttk.Button(frame1, text="Predict Winner", command=print_values1)
button_predict_winner.place(width=159, height=57, x=433, y=73)

##################################### FRAME 2 ############################################

def search(event):
    value = event.widget.get()
    if value == "":
        map_entries['MapName']['values'] = list(map_names.values())
    
    else:
        data = []
        for item in map_names.values():
            test_str = ''.join(letter for letter in str(item) if letter.isalnum())
            if value.lower() in test_str.lower():
                data.append(item)
            map_entries['MapName']['values'] = data

map_names = {0: '\x01(4)\x03NsP Clan \x07Lost Temple',
  1: '\x01Neo \x06Vertigo',
  2: '\x01sG Vertigo',
  3: '\x02G\x06orky \x02I\x06sland',
  4: '\x02G\x06orky \x02P\x06ark',
  5: '\x03Another \x07Day',
  6: '\x03B\x04yzantium \x02II \x052.2',
  7: '\x03B\x04yzantium \x051.0',
  8: '\x03Circuit Breakers \x051.0',
  9: '\x03Gaia 1.0',
  10: '\x03Guillotine',
  11: '\x03KiSaDan\x04T\x07em\x01p\x07le\x01',
  12: '\x03Korhal \x06of \x07Ceres',
  13: '\x03L\x04o\x03s\x04t \x03Te\x03m\x04p\x03l\x04e \x04SaSi',
  14: '\x03L\x04o\x03s\x04t \x03Te\x03m\x04p\x03l\x04e \x06[WHI',
  15: '\x03L\x04una',
  16: '\x03L\x04una \x06the \x07Final',
  17: '\x03Loki \x05II',
  18: '\x03Lost \x07Temple \x04- JoyDoM',
  19: '\x03Lu\x04na',
  80: '\x03Monty \x02Hall\x06_SE \x052.1',
  21: '\x03Monty \x02Hall \x051.1',
  22: '\x03N\x04eo \x06Aztec\x052.0',
  23: '\x03Neo\x06MoonGlaive\x052.1',
  24: '\x03Neo \x04Bifrost',
  25: '\x03Neo \x06Silent \x04Vortex',
  26: '\x03Rush Hour 3.03',
  27: '\x03T\x04h\x04e \x03L\x04o\x03s\x04t \x03Te\x03m\x04p\x03l\x04',
  28: '\x03T\x04he \x03L\x04ost \x03T\x04emple\x06\x02 [g',
  29: '\x03T\x06roy \x051.0',
  30: '\x03Tau \x06Cross \x051.1',
  31: '\x03The \x06Lost \x04T\x07em\x01p\x07le\x01_\x03Ch',
  32: '\x03The \x06Lost \x04T\x07em\x01p\x07le\x01_\x03Ga',
  33: "\x03Un'\x06Goro \x07Crater \x051.2",
  34: '\x03WCG_Longinus (ob)',
  35: '\x03X-L_\x06LunaTheFinal\x05_2.1',
  36: '\x03제 1회 \x07B\x06S\x03L \x05파이썬',
  37: '\x03청풍명월 \x050.93',
  38: '\x04(2)Neo \x03LiBerTy',
  39: '\x04Acheron',
  40: '\x04Andromeda \x051.0',
  41: '\x04B\x01litz',
  42: '\x04B\x01litz X',
  43: '\x04Blue \x07S\x06torm \x051.1',
  44: '\x04Blue \x07S\x06torm \x051.16',
  45: '\x04Blue \x07S\x06torm \x051.2',
  46: '\x04Blue \x07S\x06torm \x051.2 \x06 with ',
  47: '\x04Chow \x03Chow',
  48: '\x04Dahlia \x06of \x03Jungle',
  49: '\x04Enter the dragon2004',
  50: '\x04Gaema \x05Gowon',
  51: '\x04Hitch\x03hiker\x051.0',
  52: '\x04Hitch\x03hiker\x051.1',
  53: '\x04M\x03E\x04R\x03C\x04U\x03R\x04Y',
  54: '\x04M\x06atch\x04Point \x050.91',
  55: '\x04M\x06atch\x04Point \x051.1',
  56: '\x04M\x06atch\x04Point \x051.2',
  57: '\x04M\x06atch\x04Point \x051.3',
  58: '\x04NSL_\x07Ride \x06of Valkyries',
  59: '\x04Neo\x07Medusa\x052.1',
  60: '\x04Neo\x07Medusa\x052.2',
  61: '\x04Neo \x06The Lost Temple',
  62: '\x04Neo \x07F\x05orte 2.1',
  63: '\x04Neo Hall of Valhalla',
  64: '\x04Para\x06doxxx',
  65: '\x04Para\x06doxxx \x07ll',
  66: '\x04S\x02i\x03G\x07L\x06ost \x07T\x06emple \x02Gam',
  67: '\x04SCCL\x06_S1_\x07815\x05(o)',
  68: '\x04SCCL\x06_S1_\x07Estrella\x05(o)',
  69: '\x04SCCL\x06_S1_\x07Gaia\x05(o)',
  70: '\x04SCCL\x06_S1_\x07R_-_Point',
  71: '\x04SCCL\x06_S1_\x07R_-_Point\x05(o)',
  72: '\x04SCCL\x06_S1_\x07R_o_Valks\x05(o)',
  73: '\x04SCCL\x06_S1_\x07Rush_Hour\x05(o)',
  74: '\x04T\x03he \x04E\x03ye',
  75: '\x04T\x06h\x03e \x04L\x06o\x03st \x04T\x06e\x03mple \x07',
  76: '\x04The Bifrost',
  77: '\x04The Lost Temple\x06_\x07Nal',
  78: '\x04The Lost Temple \x06AKUTA',
  79: '\x04The Lost Temple \x07Sharky',
  80: '\x04The Lost Temple \x07[\x06fOu\x07] ',
  81: '\x04The Lost Temple_Gamei\x06(\x07O',
  82: '\x04[gm] \x06투혼 \x071.3',
  83: '\x04ì‹\xa0 \x01815 \x052.0',
  84: '\x04몽\x03환 \x06Ⅱ \x052.0',
  85: '\x04신 \x03청풍명월 \x052.1',
  86: '\x04신 \x07단장의 \x06능선 \x052.1',
  87: '\x04은빛날개 \x050.90',
  88: '\x05Forbidden Zone',
  89: '\x05Python 1.1',
  90: '\x05Python 1.2',
  91: '\x05Python 1.3',
  92: '\x05Python 1.3 \x07with PKM ㅋ',
  93: '\x05팔진도 1.1',
  94: '\x06(2)\x03Enter the dragon',
  95: '\x06815\x04â…¢ \x053.1',
  96: '\x06A\x07byss \x02Longinus \x06[\x0703\x06]',
  97: '\x06A\x07byss \x02Tau Cross \x06[\x0703\x06]',
  98: '\x06B\x05e\x06n\x05z\x06e\x05n\x06e\x051.1',
  99: '\x06DTR\x03[\x07������ �ɼ� 1.0\x03]\x06A',
  100: '\x06DTR.\x07X\x06[\x07D\x06estinatioN]\x07Sa',
  101: '\x06DTR.\x07X \x01[\x04M\x06e\x01d\x06u\x04S\x06a\x01] \x07',
  102: '\x06Gaia\x051.0',
  103: '\x06Incubus \x072004',
  104: '\x06Martian \x05Cross',
  105: '\x06Namja \x05Iyagi',
  106: '\x06Neo \x03Baekdu Daegan \x052.4',
  107: '\x06Neo \x03Guillotine',
  108: '\x06Neo \x05Forbidden Zone',
  109: '\x06Neo \x07Requiem \x052.0',
  110: '\x06NeoThe Lost Temple',
  111: '\x06Plains to Hill \x07Desert',
  112: '\x06R\x04ide of \x06V\x04alkyries \x051.0',
  113: '\x06Silent \x04Vortex',
  114: '\x06The \x03KORHAL',
  115: '\x06The Fortress SE \x052.0',
  116: '\x06The Lost Temple\x04_GaMax',
  117: '\x06Z\x05odiAc',
  118: '\x06[LoOz] \x07\x05LoTem\x04\x05 (\x03 OB\x05)',
  119: '\x06[S.G] \x04Lost Temple',
  120: '\x06[SaSin] \x07Blue Storm  \x041.2',
  121: '\x06ì‹\xa0 \x03ë°±ë‘\x90ëŒ€ê°„ \x052.2',
  122: '\x06ì‹\xa0 \x03ë°±ë‘\x90ëŒ€ê°„ \x052.4',
  123: '\x06신 \x03백두대간 \x052.4',
  124: '\x06신 \x03백두대간 \x052.41',
  125: '\x06폭풍의 \x04언덕 \x050.95',
  126: '\x06폭풍의 \x04언덕 \x051.0',
  127: '\x07\x07WGTOUR \x01\x07Plains to Hill',
  128: '\x07\x07WGTOUR \x01\x07Temple WCG',
  129: '\x07)Is( \x05Lost \x03Temple\x02\x03',
  130: '\x07A\x06rcadia',
  131: '\x07A\x06rcadia II',
  132: '\x07Athena \x051.0',
  133: '\x07BWCL S-22\x06 Sin 815 2.0',
  134: '\x07C\x06olosseum\x050.93',
  135: '\x07C\x06olosseum\x051.0',
  136: '\x07CEG - \x03L\x04una',
  137: '\x07CEG - \x06A\x04rcadia \x04II',
  138: '\x07CEG - \x07R\x06ush \x04Hour \x02III',
  139: '\x07Clan \x06E\x02v\x06e\x02r \x05Lost Templ',
  140: '\x07Colosseum\x06II\x052.0',
  141: '\x07DAHLIA',
  142: '\x07DTR\x03[\x04Destination1.1\x03]\x06Ar',
  143: '\x07DTR.\x02U \x04Blue\x02S\x06torm \x07[S\x06a',
  144: '\x07Desert \x06Lost Temple \x03<ghe',
  145: '\x07Destination \x051.1',
  146: '\x07Detonation-F',
  147: '\x07F\x05orte 1.0',
  148: '\x07G\x03aia \x050.90',
  149: '\x07G\x06rand\x07L\x06ine\x05_SE 2.0',
  150: '\x07G\x06rand\x07L\x06ine\x05_SE 2.2',
  151: '\x07I\x06nto \x02The \x07D\x06arkness',
  152: '\x07IEF\x06_\x03BlueStorm 1.2',
  153: '\x07IEF\x06_\x03Python 1.3',
  154: '\x07IEF\x06_\x03Tau Cross 1.1',
  155: '\x07IEF \x03Chupung Ryeong 2.1',
  156: '\x07IEST\x04_\x03Longinus II',
  157: '\x07IEST\x04_\x03Monty Hall 1.1',
  158: '\x07Into \x06The \x07D\x06arkness \x02Par',
  159: '\x07K\x06atrina\x051.3',
  160: '\x07K\x06atrina_SE\x051.90',
  161: '\x07K\x06atrina_SE\x052.0',
  162: '\x07L\x05onginus',
  163: '\x07L\x05onginusâ…¡',
  164: '\x07L\x05onginusⅡ',
  165: '\x07L\x06ost \x07T\x06emple \x07SaSin \x07X',
  166: '\x07LoveStarTV\x02&\x06SaSin \x03Blue\x04',
  167: '\x07Luna - \x04MBCgame',
  168: '\x07Medusa\x051.0',
  169: '\x07Medusa\x051.1',
  170: '\x07Neo Legacy of Char',
  171: '\x07Neo Legacy of Char_OS',
  172: '\x07Nostalgia',
  173: '\x07OGCL1 -\x04 Into the Darknes',
  174: '\x07Othello \x050.991',
  175: '\x07Othello \x051.1',
  176: '\x07Outsider \x051.0',
  177: '\x07Outsider SE \x052.0',
  178: '\x07Outsider SE \x052.2',
  179: '\x07P\x06lasma \x051.0',
  180: '\x07PGL\x04_\x03Arcadia II',
  181: '\x07PGL\x04_\x03BlitzX 2.0',
  182: '\x07PGL\x04_\x03Longinus II',
  183: '\x07PGL\x04_\x03Reverse Temple',
  184: '\x07PLU\x06_\x03Andromeda 1.0',
  185: '\x07PLU\x06_\x03Arcadia II',
  186: '\x07PLU\x06_\x03Arcadia II M',
  187: '\x07PLU\x06_\x03Bakdu 2.4',
  188: '\x07PLU\x06_\x03Longinus II',
  189: '\x07PLU\x06_\x03Luna The Final',
  190: '\x07PLU\x06_\x03LunaTheFinal 2.1',
  191: '\x07PLU\x06_\x03Reverse Lost Temple',
  192: '\x07PLU\x06_\x03Rush Hour \x053.03',
  193: '\x07PLU\x06_\x03Rush Hour 3.03',
  194: '\x07PLU\x06_\x03Sin 815',
  195: '\x07R\x06ush \x04Hour',
  196: '\x07R\x06ush \x04Hour \x02â…¡',
  197: '\x07R\x06ush \x04Hour \x02â…¢',
  198: '\x07R\x06ush \x04Hour \x02Ⅱ',
  199: '\x07R\x06ush \x04Hour \x02Ⅲ',
  200: '\x07R\x06ush \x07H\x06our \x053.1',
  201: '\x07Requiem',
  202: '\x07Reverse \x04Temple \x051.0',
  203: '\x07SIM \x06K\x03orhal of Ceres',
  204: '\x07STL\x06_\x03Arcadia II',
  205: '\x07STL\x06_\x03LunaTheFinal 2.1',
  206: '\x07STL\x06_\x03New Peaks of Baekdu',
  207: '\x07STL\x06_\x03Python 1.3',
  208: '\x07Sin \x04Gaema \x05Gowon',
  209: '\x07WCG \x03A\x04zalea \x051.0',
  210: '\x07WCG \x03G\x06aia \x051.0',
  211: '\x07WCG \x03G\x06aia \x051.1',
  212: '\x07WCG \x03P\x06aranoid \x04A\x06ndroid ',
  213: '\x07WCG \x04Estrella \x051.0',
  214: '\x07[Nyx] \x05��ȥ \x051.3 (������)',
  215: '\x07[SaSin] \x05Python 1.3 \x06_v.D',
  216: '\x07luna-MBCgame',
  217: '\x07nG-i \x03Lost Temple 2.3',
  218: '\x07nG-i \x03Lost Temple Gamei',
  219: '\x07nG-i \x03Nostalgia 1.3',
  220: '\x07단장의 \x06능선 \x051.0',
  221: '\x07단장의 \x06능선 \x051.1',
  222: '\x07심판의 날 \x050.90',
  223: '\x07아크로 \x050.91',
  224: '\x07용\x03오\x04름 \x050.93',
  225: '\x07용\x03오\x04름 \x050.95',
  226: '\x07태양의 제국 \x051.3',
  227: '\x07투혼 \x051.1',
  228: '\x07투혼 \x051.3',
  229: ' \x07BKC-8 \x06Gaia\x051.0',
  230: ' Rivarly_gamebugs',
  231: '(3)Universal Tripod.(R)-KP',
  232: '(4) Illusion',
  233: '(4)The Lost Temple-KPGA',
  234: '(OB)\x04Neo \x06The Lost Temple',
  235: 'Asgard0.90',
  236: 'Astral Eclipse (Ob)',
  237: 'Avant-garde II',
  238: 'Blade Storm',
  239: 'CDF Enter The Dragon',
  240: 'CDF Lost Temple - gameTV',
  241: 'CL16 - Python 1.1 (Ob)',
  242: 'CL18 - Nostalgia 1.3',
  243: 'Coulee',
  244: 'Desert FoX',
  245: 'Dire Straits + 4 Observers',
  246: 'Dream Tour - Temple Gamei',
  247: 'Eldritch Lake',
  248: 'Enmity (Ob)',
  249: 'GGL Dahlia of Jungle',
  250: 'GGL Lost Temple',
  251: 'Gauntlet2003',
  252: 'Indian Lament',
  253: "Jim Raynor's Memory",
  254: 'Jungle story',
  255: 'King of the Abyss',
  256: 'King of the Abyss (Ob)',
  257: 'Longinus II',
  258: 'MoonGlaive0.91',
  259: 'MoonGlaive0.92',
  260: 'MoonGlaive1.2',
  261: 'Neo Jungle story',
  262: 'Nightlight(Ob)',
  263: 'P\x06olaris\x02Rh\x06apsody\x05 1.0',
  264: 'PGT - Arcadia 1.03 [08]\r\x1f',
  265: 'PGT - Arcadia II [10]',
  266: 'PGT - Arena [06]\r\x1f',
  267: 'PGT - Bifrost lll [01]\r\x1f',
  268: 'PGT - Blade Storm [02]\n\x1f',
  269: 'PGT - Enter the D. 2004 [0',
  270: 'PGT - Gaia 0.90 [03]\n\x1f',
  271: 'PGT - Gaia 1.0 [05]\r\x1f',
  272: 'PGT - Gaia 1.0 [07]\n\x1f',
  273: 'PGT - Gaia 1.0 [08]\n\x1f',
  274: 'PGT - Gaia 1.0 [10]',
  275: 'PGT - Incubus 2004 [02]\n\x1f',
  276: 'PGT - Lost Temple 2.35 [01',
  277: 'PGT - Lost Temple 2.4 [02]',
  278: 'PGT - Lost Temple 2.4 [04]',
  279: 'PGT - Lost Temple 2.4 [05]',
  280: 'PGT - Luna 2.01 [02]\n\x1f',
  281: 'PGT - Luna 2.01 [02]\r\x1f',
  282: 'PGT - Luna The Final [03]\r',
  283: 'PGT - Luna The Final [04]\n',
  284: 'PGT - Luna The Final [05]\n',
  285: 'PGT - Luna The Final [05]\r',
  286: 'PGT - Luna The Final [06]\n',
  287: 'PGT - Luna The Final [06]\r',
  288: 'PGT - Luna The Final [07]\n',
  289: 'PGT - Luna The Final [07]\r',
  290: 'PGT - Luna the Final [08]\r',
  291: 'PGT - Luna the Final [09]\r',
  292: 'PGT - Memory Cell [10]',
  293: 'PGT - Namja Iyagi [01]\r\x1f',
  294: 'PGT - Neo Forte 2.1 [04]\n\x1f',
  295: 'PGT - Neo Forte 2.1 [06]\n\x1f',
  296: 'PGT - Neo Forte 2.1 [06]\r\x1f',
  297: 'PGT - Neo Forte 2.1 [07]\n\x1f',
  298: 'PGT - Neo Forte 2.1 [07]\r\x1f',
  299: 'PGT - Neo Forte 2.1 [08]\n\x1f',
  300: 'PGT - Neo Requiem 2.0 [03]',
  301: 'PGT - Neo Requiem 2.0 [07]',
  302: 'PGT - Nostalgia [01]\n\x1f',
  303: 'PGT - Nostalgia [01]\r\x1f',
  304: 'PGT - Nostalgia [02]\n\x1f',
  305: 'PGT - Nostalgia [02]\r\x1f',
  306: 'PGT - ParanoidAndroid1.0 [',
  307: 'PGT - R - Point 1.0 [04]\n\x1f',
  308: 'PGT - R - Point 1.0 [05]\r\x1f',
  309: 'PGT - R - Point 1.0 [06]\n\x1f',
  310: 'PGT - R - Point 1.0 [06]\r\x1f',
  311: 'PGT - R - Point 1.0 [07]\n\x1f',
  312: 'PGT - R - Point 1.0 [07]\r\x1f',
  313: 'PGT - Ride of Valkyries [0',
  314: 'PGT - Rush Hour 2.0 [05]\n\x1f',
  315: 'PGT - Rush Hour 2.0 [05]\r\x1f',
  316: 'PGT - Rush Hour 2.0 [06]\n\x1f',
  317: 'PGT - Rush Hour 2.0 [06]\r\x1f',
  318: 'PGT - Rush Hour 2.0 [07]\n\x1f',
  319: 'PGT - Rush Hour 2.0 [07]\r\x1f',
  320: 'PGT - Rush Hour III [08]\n\x1f',
  321: 'PGT - Rush Hour III [08]\r\x1f',
  322: 'PGT - Rush Hour III [09]\n\x1f',
  323: 'PGT - Rush Hour III [09]\r\x1f',
  324: 'PGT - Rush Hour III [10]',
  325: 'PGT - Sin Gaema Gowon [01]',
  326: 'Paranoid Android 1.0',
  327: 'Plains to Hill',
  328: 'Plains to Hill-KPGA',
  329: 'R - \x04Point',
  330: 'Rivalry',
  331: 'Rivalry - Ghemtv',
  332: 'River of Flames',
  333: 'Roadrunner0.91',
  334: 'RodeoWalk Star League',
  335: 'S ignal(Ob)',
  336: 'Showdown',
  337: 'Snowbound',
  338: 'TLT - Blade Storm 1.5',
  339: 'TLT - Blade Storm 1.5 (Ob)',
  340: 'TLT - Isles of Siren (Ob)',
  341: 'TLT - Lost Temple 2.4',
  342: 'TLT - Lost Temple 2.4 (Ob)',
  343: 'TLT - Namja Iyagi (Ob)',
  344: 'TLT - Sin Gaema Gowon',
  345: 'TLT - Sin Gaema Gowon (Ob)',
  346: 'Tau Cross 1.1',
  347: 'The Lord of The Ring',
  348: 'The Lost Temple',
  349: 'The Lost Temple Gamei',
  350: 'The Lost Temple game-i\x04(ob',
  351: 'The Lost Temple_\x07K\x02T\x07F\x06.\x02s',
  352: 'The Lost Temple_(R)',
  353: 'The Lost Temple_Gamei',
  354: 'The Lost Temple_Itv Game',
  355: 'The Lost Temple_gembc',
  356: 'WCG Neo Jungle story V2',
  357: 'WCG The Lost Temple V2',
  358: 'WCG_Neo Hall of Valhalla',
  359: 'WCG_Neo Hall of Valhalla \x05',
  360: 'WCG_Neo Jungle story',
  361: 'WCG_Neo Legacy of Char',
  362: 'WCG_Rivalry',
  363: 'WCG_The Lost Temple',
  364: 'WGT10 - Bifrost lll (Ob)',
  365: 'WGT10 - Enter the D 2004 (',
  366: 'WGT10 - Incubus 2004 (Ob)',
  367: 'WGT10 - Luna (Ob)',
  368: 'WGT10 - Martian Cross (Ob)',
  369: 'WGT10 - Mercury 1.0 (Ob)',
  370: 'WGT10 - Namja Iyagi (Ob)',
  371: 'WGT10 - Nostalgia 1.3 B (O',
  372: 'WGT10 - Parallel Lines 3',
  373: 'WGT10 - Sin Gaema Gowon B ',
  374: 'WGT10 - Xeno Sky 1.0 (Ob)',
  375: 'WGT10 -- Lost Temple 2.4',
  376: 'WGT10 -- Lost Temple 2.4 (',
  377: 'WGT11 - Luna (Ob)',
  378: 'WGT11 - Martian Cross',
  379: 'WGT11 - Nostalgia 1.3',
  380: 'WGT11 - Nostalgia 1.3 B (O',
  381: 'WGT11 - Sin Gaema Gowon B ',
  382: 'WGT11 - Xeno Sky 1.0 (Ob)',
  383: 'WGT11 -- Lost Temple 2.4',
  384: 'WGT11 -- Lost Temple 2.4 (',
  385: 'WGT11 -- Lost Temple Gamei',
  386: 'WGT12 - Coulee (Ob)',
  387: 'WGT12 - Desolate Platform ',
  388: 'WGT12 - Estrella 0.90',
  389: 'WGT12 - Estrella 0.90 (Ob)',
  390: 'WGT12 - Forte 1.0 (Ob)',
  391: 'WGT12 - Gaia 0.90',
  392: 'WGT12 - Gaia 0.90 (Ob)',
  393: 'WGT12 - Luna The Final (Ob',
  394: 'WGT12 - Nostalgia 1.3 B (O',
  395: 'WGT12 - Raid - Assault 2.0',
  396: 'WGT12 - Sin Gaema Gowon B ',
  397: 'WGT12 -- Lost Temple 2.4',
  398: 'WGT12 -- Lost Temple 2.4 (',
  399: 'WGT12 -- Lost Temple Gamei',
  400: 'WGT13 - Azalea 1.0 (Ob)',
  401: 'WGT13 - Blade Storm 1.5 (O',
  402: 'WGT13 - Blitz X 2.0',
  403: 'WGT13 - Enmity 1.1',
  404: 'WGT13 - Estrella 1.0',
  405: 'WGT13 - Gaia 1.0 (Ob)',
  406: 'WGT13 - IntoTheDarkness II',
  407: 'WGT13 - Longinus',
  408: 'WGT13 - Longinus 2.0',
  409: 'WGT13 - Longinus 2.0 (Ob)',
  410: 'WGT13 - Luna the Final (Ob',
  411: 'WGT13 - Neo Forte 2.1',
  412: 'WGT13 - Nostalgia 1.3 (Ob)',
  413: 'WGT13 - ParanoidAndroid1.0',
  414: 'WGT13 - PeaksOfBaekdu 2.2',
  415: 'WGT13 - R - Point 1.0',
  416: 'WGT13 - Reverse Temple 1.0',
  417: 'WGT13 - Ride of Valkyries ',
  418: 'WGT13 - Rush Hour 2.0 (Ob)',
  419: 'WGT13 - Rush Hour III',
  420: 'WGT13 - Rush Hour III (Ob)',
  421: 'WGT13 - Tau Cross 1.1',
  422: 'WGT13 - Tau Cross 1.1 (Ob)',
  423: 'WGT13 -- Lost Temple 2.4 (',
  424: 'WGT14 - Arcadia II (Ob)',
  425: 'WGT14 - Blitz X 2.0 (Ob)',
  426: 'WGT14 - Blue Storm 1.1 (Ob',
  427: 'WGT14 - Fantasy 1.1 (Ob)',
  428: 'WGT14 - Gaia 1.0 (Ob)',
  429: 'WGT14 - Lost Temple 2.4 (O',
  430: 'WGT14 - ParanoidAndroid1.0',
  431: 'WGT14 - PeaksOfBaekdu 2.4 ',
  432: 'WGT14 - Python 1.3 (Ob)',
  433: 'WGT14 - Tau Cross 1.1 (Ob)',
  434: 'WGT14 - ZodiAc 1.01',
  435: 'WGT14 - ZodiAc 1.01 (Ob)',
  436: 'WGT9 - Bifrost lll (Ob)',
  437: 'WGT9 - Dahlia of Jungle',
  438: 'WGT9 - Dahlia of Jungle (O',
  439: 'WGT9 - Gorky Island (Ob)',
  440: 'WGT9 - Into the Darkness 1',
  441: 'WGT9 - Korhal of Ceres',
  442: 'WGT9 - Lost Temple 2.3',
  443: 'WGT9 - Lost Temple 2.3 (Ob',
  444: 'WGT9 - Luna (Ob)',
  445: 'WGT9 - Neo Forbidden Zone ',
  446: 'WGT9 - Neo Lost Temple',
  447: 'WGT9 - Neo Lost Temple (Ob',
  448: 'WGT9 - Nostalgia B (Ob)',
  449: 'WGT9 - Xeno Sky (Ob)',
  450: 'WGTOUR (2) Neo Valhalla',
  451: 'WGTOUR (2) Plains to Hill',
  452: 'WGTOUR (3) Neo Legacy of C',
  453: 'WGTOUR (3) Neo Valhalla',
  454: 'WGTOUR (3) Temple Gamei',
  455: 'WGTOUR (4) Neo Jungle Stor',
  456: 'WGTour (4) Plains to Hill',
  457: 'WGTour (4) Temple Gamei',
  458: 'WGTour (5) Enter The Drago',
  459: 'WGTour (5) Gaema Gowon B',
  460: 'WGTour (5) Gaema Gowon B (',
  461: 'WGTour (5) JR Memory Jungl',
  462: 'WGTour (5) Lost Temple 2.1',
  463: 'WGTour (5) Nostalgia B (Ob',
  464: 'WGTour (6) DAHLIA',
  465: 'WGTour (6) Enter the drago',
  466: 'WGTour (6) Gaema Gowon B (',
  467: 'WGTour (6) Legacy of Char ',
  468: 'WGTour (6) Lost Temple 2.2',
  469: 'WGTour (6) Lost Temple_Gam',
  470: 'WGTour (6) Neo Lost Temple',
  471: 'WGTour (6) Nostalgia B (Ob',
  472: 'WGTour (6) Plains to Hill ',
  473: 'WGTour (6) Vertigo (Ob)',
  474: 'WGTour (7) Detonation (Ob)',
  475: 'WGTour (7) Enter the D 200',
  476: 'WGTour (7) Enter the drago',
  477: 'WGTour (7) Gaema Gowon B',
  478: 'WGTour (7) Lost Temple 2.3',
  479: 'WGTour (7) Lost Temple_Gam',
  480: 'WGTour (7) Neo Forbidden Z',
  481: 'WGTour (7) Neo Guillotine ',
  482: 'WGTour (7) Neo Lost Temple',
  483: 'WGTour (7) Nostalgia B',
  484: 'WGTour (7) Nostalgia B (Ob',
  485: 'WGTour (7) The KORHAL (Ob)',
  486: 'WGTour (8) DAHLIA (Ob)',
  487: 'WGTour (8) Enter the D 200',
  488: 'WGTour (8) Gorky Park (Ob)',
  489: 'WGTour (8) Lost Temple 2.3',
  490: 'WGTour (8) Lost Temple_Gam',
  491: 'WGTour (8) Neo Bifrost 2.0',
  492: 'WGTour (8) Neo Lost Temple',
  493: 'WGTour (8) Nostalgia 1.3',
  494: 'WGTour (8) The KORHAL (Ob)',
  495: 'WSL Dahlia',
  496: 'WSL Lost Temple 2.1',
  497: 'WSL Nostalgia B (Ob)',
  498: 'WSL Plains to Hill Desert ',
  499: "['-'v]Clan Lost_Temple(oB)",
  500: '[4] Lost Temple - gameTV',
  501: '[SaSin]\x05Python 1.3_(DTR)',
  502: '[SaSin] \x04Andromeda \x051.0 \x04v',
  503: '[WGTour4]Neo Hall of Valha',
  504: '| ICCup | Troy 1.0',
  505: '| iCCup | Andromeda 1.0',
  506: '| iCCup | Andromeda 1.0 OB',
  507: '| iCCup | Athena II 2.0',
  508: '| iCCup | Athena II 2.0 OB',
  509: '| iCCup | Azalea',
  510: '| iCCup | Blue Storm 1.1',
  511: '| iCCup | Blue Storm 1.2',
  512: '| iCCup | Blue Storm 1.2 O',
  513: '| iCCup | Byzantium II 2.2',
  514: '| iCCup | Chupung-Ryeung 1',
  515: '| iCCup | ColosseumII 2.0',
  516: '| iCCup | ColosseumII 2.0 ',
  517: '| iCCup | Destination 1.1',
  518: '| iCCup | Destination 1.1 ',
  519: '| iCCup | Eye of the Storm',
  520: '| iCCup | Fighting Spirit ',
  521: '| iCCup | Gaia',
  522: '| iCCup | Gods Garden',
  523: '| iCCup | Heartbreak Ridge',
  524: '| iCCup | Heatbreak Ridge',
  525: '| iCCup | Heatbreak Ridge ',
  526: '| iCCup | Judgement Day 1.',
  527: '| iCCup | Katrina 1.3',
  528: '| iCCup | Loki II',
  529: '| iCCup | Longinus',
  530: '| iCCup | Longinus OBs',
  531: '| iCCup | Match Point 1.1 ',
  532: '| iCCup | Match Point 1.2',
  533: '| iCCup | Medusa 1.1',
  534: '| iCCup | Medusa 1.1 OBs',
  535: '| iCCup | Monty Hall 1.1 o',
  536: '| iCCup | MoonGlaive 1.2',
  537: '| iCCup | MoonGlaive 2.1',
  538: '| iCCup | NeoMedusa 2.1',
  539: '| iCCup | NeoMedusa 2.1 OB',
  540: '| iCCup | NeoMedusa2.0 OBs',
  541: '| iCCup | Othello 1.1',
  542: '| iCCup | Othello 1.1 OBS',
  543: '| iCCup | Othello 1.1 OBs',
  544: '| iCCup | Outsider',
  545: '| iCCup | Outsider OBs',
  546: '| iCCup | Paranoid Android',
  547: '| iCCup | PeaksOfBeakdu',
  548: '| iCCup | Python 1.1',
  549: '| iCCup | Python 1.2 obs',
  550: '| iCCup | Python 1.3',
  551: '| iCCup | Python 1.3 OBs',
  552: '| iCCup | River of Flames ',
  553: '| iCCup | Shine obs',
  554: '| iCCup | Sin Chupung Ryeo',
  555: '| iCCup | Tau Cross',
  556: '| iCCup | Tau Cross OBs',
  557: '| iCCup | The Fortress 1.1',
  558: '| iCCup | Tornado',
  559: '| iCCup | UnGoro Crater 1.',
  560: '| iCCup | Wuthering H 1.0',
  561: '| iCCup | ZodiAc',
  562: '| sc2tv | Destination 1.1',
  563: "\x7f \x04Lost Temple \x7f NaDa'-'v",
  564: '신 \x03개척\x06시대 \x052.1',
  565: '틼WCL� Python 1.3',
  566: '틼WCL� Rush Hour',
  567: '�\x07[\x02p\x04G\x07]\x04�\x06-=\x02T\x07e\x04M\x07p\x02L\x04e'}

# print(list(map_names.values()))

map_entries = {
    'MapName': ttk.Combobox(frame2, values=list(map_names.values())),
    'MapWidth': ttk.Combobox(frame2, values=[128,96,112]),
    'MapHeight': ttk.Combobox(frame2, values=[128,96]),
}

# Labels for the entry fields
map_labels_text = [
    "Map Name", "Map Width", "Map Height"
]

map_entries['MapName'].bind("<KeyRelease>", search)

# Calculate placement for labels
for i, text in enumerate(map_labels_text):
    col = i + 1
    label = ttk.Label(frame2, text=text)
    # label.place(x=30, y=100 + 30*row, height=25)
    label.grid(row=0, column=col, padx=5, pady=5)

# Place Entries on the screen with calculated positions
for i, (name, entry) in enumerate(map_entries.items()):
    row = 1
    col = i + 1
    entry.grid(row=row, column=col, padx=5, pady=5)
    # entry.place(width=85, height=25, x=150 + 135*col, y=100 + 30*row)


# Create Entries
entries2 = {
    'p1_eapm': ttk.Entry(frame2),
    'p2_eapm': ttk.Entry(frame2),
    'p1_ecmd': ttk.Entry(frame2),
    'p2_ecmd': ttk.Entry(frame2),
    'p1_totalUnits': ttk.Entry(frame2),
    'p2_totalUnits': ttk.Entry(frame2),
    'p1_aliveUnits': ttk.Entry(frame2),
    'p2_aliveUnits': ttk.Entry(frame2),
    'p1_winner_percent': ttk.Entry(frame2),
    'p2_winner_percent': ttk.Entry(frame2),
}

# Label for Player 1 and Player 2 above their race Comboboxes
label_player1 = ttk.Label(frame2, text="Player 1")
# label_player1.place(width=91, height=28, x=150, y=50)
label_player1.grid(row=2, column=1, padx=5, pady=5)

label_player2 = ttk.Label(frame2, text="Player 2")
# label_player2.place(width=91, height=28, x=286, y=50)
label_player2.grid(row=2, column=2, padx=5, pady=5)

# Labels for the entry fields
labels_text = [
     'EAPM', 'ECmdCount', 'TotalUnits', 'AliveUnits', 'Winner %'
]

# Calculate placement for labels
for i, text in enumerate(labels_text):
    row = i + 3
    label = ttk.Label(frame2, text=text)
    # label.place(x=30, y=100 + 30*row, height=25)
    label.grid(row=row, column=0, padx=5, pady=5)

# Place Entries on the screen with calculated positions
for i, (name, entry) in enumerate(entries2.items()):
    row = i // 2 + 3
    col = i % 2 + 1
    entry.grid(row=row, column=col, padx=5, pady=5)
    # entry.place(width=85, height=25, x=150 + 135*col, y=100 + 30*row)

entries2["p1_winner_percent"].config(state= "disabled")
entries2["p2_winner_percent"].config(state= "disabled")

def print_values2():
    # Print ComboBox values
    print("Player 1 Race:", combobox_player1_race.get())
    print("Player 2 Race:", combobox_player2_race.get())
    print("Selected Model:", combobox_model.get())
    print("Input Features:", combobox_input_features.get())

    inputs = [combobox_player1_race.get(), combobox_player2_race.get()]
    # Print Entry values
    
    for name, entry in map_entries.items():
        print(f"{name}: {entry.get()}")
        inputs.append(entry.get())

    for index, name in map_names.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if name == inputs[2]:
            print("Map Name:", name, index)
            inputs[2] = index
            break

    for name, entry in entries2.items():
        print(f"{name}: {entry.get()}")
        inputs.append(entry.get())

    # call predict winner with data as input as pandas input
    # with columns ["Player1_Race","Player2_Race","Player1_AliveUnits","Player2_AliveUnits","Player1_SupplyUsed","Player2_SupplyUsed","Player1_Gas","Player1_Gas", "Player1_Minerals", "Player2_Minerals"]
    # return the winner percentage for player 1 and player 2
    result = predict_gameState(inputs,combobox_model.get())
    print("recieved results", result)
    update_winner_percent(entries2,result[0]*100, result[1]*100)

# Predict Winner Button
button_predict_winner = ttk.Button(frame2, text="Predict Winner", command=print_values2)
button_predict_winner.place(width=159, height=57, x=433, y=73)

root.mainloop()
