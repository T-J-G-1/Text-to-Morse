from tkinter import *

BACKGROUND = "#EBCFA7"

root = Tk()
root.title("Text to Morse")
root.configure(background=BACKGROUND)
root.minsize(400, 600)
root.maxsize(400, 600)

alphabet = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z"
]
morse_code = [
    ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---",
    "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-",
    "..-", "...-", ".--", "-..-", "-.--", "--.."
]
alph = []
morse = []

def onclick_input():
    inputz = input_box.get("1.0", END).lower().strip()  # Get and clean input text
    alph.clear()  # Clear lists before re-use
    morse.clear()
    
    for letter in inputz:
        if letter in alphabet:
            alph.append(letter)

    for letters in alph:
        letter_index = alphabet.index(letters)
        morse.append(morse_code[letter_index])

    # Update display_label with the Morse code as a space-separated string
    display_label.config(text=" ".join(morse))

# Create all widgets before calling mainloop
title_label = Label(root, text="Text to Morse code Translator", font=("Courier", 14,"bold"), background=BACKGROUND)
display_label = Label(root, text="", font=("Courier", 10), wraplength=380, justify=LEFT, background=BACKGROUND)
input_box = Text(root, width=30, height=5)
input_button = Button(root, text="Morse Me!", command=onclick_input, font=("Courier", 10,"bold"), background="#C6A27E")

# Use Grid to position the widgets, also use padding
title_label.grid(column=1, row=0, pady=30, padx=30)
display_label.grid(column=0, row=1, columnspan=3, rowspan=2, pady=10, padx=10)
input_box.grid(column=0, row=3, rowspan=2, columnspan=2, pady=10, padx=10)
input_button.grid(column=1, row=5, pady=10)

# Start Tkinter loop
root.mainloop()