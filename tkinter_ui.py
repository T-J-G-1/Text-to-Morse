from tkinter import Tk, Label, Text, Button, END, LEFT

BACKGROUND = "#EBCFA7"

MORSE_MAP = {
    "a": ".-",    "b": "-...",  "c": "-.-.",  "d": "-..",   "e": ".",
    "f": "..-.",  "g": "--.",   "h": "....",  "i": "..",    "j": ".---",
    "k": "-.-",   "l": ".-..",  "m": "--",    "n": "-.",    "o": "---",
    "p": ".--.",  "q": "--.-",  "r": ".-.",   "s": "...",   "t": "-",
    "u": "..-",   "v": "...-",  "w": ".--",   "x": "-..-",  "y": "-.--",
    "z": "--..",
    " ": "/",  # word separator (optional but nice)
}

def text_to_morse(text: str) -> str:
    cleaned = text.lower().strip()
    encoded = [MORSE_MAP[ch] for ch in cleaned if ch in MORSE_MAP]
    return " ".join(encoded)

def on_convert():
    user_text = input_box.get("1.0", END)
    display_label.config(text=text_to_morse(user_text))

root = Tk()
root.title("Text to Morse")
root.configure(background=BACKGROUND)
root.minsize(400, 600)
root.maxsize(400, 600)

title_label = Label(
    root,
    text="Text to Morse Code Translator",
    font=("Courier", 14, "bold"),
    background=BACKGROUND
)

display_label = Label(
    root,
    text="",
    font=("Courier", 10),
    wraplength=380,
    justify=LEFT,
    background=BACKGROUND
)

input_box = Text(root, width=30, height=5)

input_button = Button(
    root,
    text="Morse Me!",
    command=on_convert,
    font=("Courier", 10, "bold"),
    background="#C6A27E"
)

title_label.grid(column=1, row=0, pady=30, padx=30)
display_label.grid(column=0, row=1, columnspan=3, rowspan=2, pady=10, padx=10)
input_box.grid(column=0, row=3, rowspan=2, columnspan=2, pady=10, padx=10)
input_button.grid(column=1, row=5, pady=10)

root.mainloop()
