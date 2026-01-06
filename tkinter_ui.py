from tkinter import Tk, Label, Text, Button, END, LEFT
import winsound

BACKGROUND = "#EBCFA7"

# Morse mapping (A–Z + space)
MORSE_MAP = {
    "a": ".-",    "b": "-...",  "c": "-.-.",  "d": "-..",   "e": ".",
    "f": "..-.",  "g": "--.",   "h": "....",  "i": "..",    "j": ".---",
    "k": "-.-",   "l": ".-..",  "m": "--",    "n": "-.",    "o": "---",
    "p": ".--.",  "q": "--.-",  "r": ".-.",   "s": "...",   "t": "-",
    "u": "..-",   "v": "...-",  "w": ".--",   "x": "-..-",  "y": "-.--",
    "z": "--..",
    " ": "/",     # word separator
}

# --- Beep settings (tweak these if you want) ---
FREQ = 750          # Hz
DOT_MS = 120        # dot beep length
DASH_MS = DOT_MS * 3
SYMBOL_GAP_MS = DOT_MS      # gap between dots/dashes in same letter
LETTER_GAP_MS = DOT_MS * 3  # gap between letters
WORD_GAP_MS = DOT_MS * 7    # gap between words


def text_to_morse(text: str) -> str:
    cleaned = text.lower().strip()
    encoded = [MORSE_MAP[ch] for ch in cleaned if ch in MORSE_MAP]
    # Join letters with spaces; words separated by "/"
    return " ".join(encoded)


class MorsePlayer:
    """
    Plays Morse code using non-blocking scheduling (Tk 'after'),
    so the UI stays responsive.
    """
    def __init__(self, root: Tk):
        self.root = root
        self._events = []          # list of (action, duration_ms)
        self._event_index = 0
        self._is_playing = False
        self._after_id = None

    def stop(self):
        self._is_playing = False
        self._events = []
        self._event_index = 0
        if self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except Exception:
                pass
        self._after_id = None
        status_label.config(text="Status: Stopped")

    def build_events_from_morse(self, morse: str):
        """
        Convert a morse string like ".- -... / ..." into a sequence
        of beep/silence events.
        """
        events = []

        # morse is space-separated tokens, where each token is a letter's morse
        # and "/" indicates a word break.
        tokens = morse.split()

        for token_i, token in enumerate(tokens):
            if token == "/":
                # word gap (silence)
                events.append(("silence", WORD_GAP_MS))
                continue

            # token is a letter like ".-" or "--.."
            for sym_i, sym in enumerate(token):
                if sym == ".":
                    events.append(("beep", DOT_MS))
                elif sym == "-":
                    events.append(("beep", DASH_MS))

                # gap between symbols inside the same letter
                if sym_i < len(token) - 1:
                    events.append(("silence", SYMBOL_GAP_MS))

            # letter gap after each letter (unless next token is a word break or end)
            if token_i < len(tokens) - 1 and tokens[token_i + 1] != "/":
                events.append(("silence", LETTER_GAP_MS))

        return events

    def play(self, morse: str):
        if not morse.strip():
            status_label.config(text="Status: Nothing to play")
            return

        self.stop()  # reset any previous playback
        self._events = self.build_events_from_morse(morse)
        self._event_index = 0
        self._is_playing = True
        status_label.config(text="Status: Playing…")

        self._play_next_event()

    def _play_next_event(self):
        if not self._is_playing:
            return

        if self._event_index >= len(self._events):
            self.stop()
            status_label.config(text="Status: Finished")
            return

        action, duration = self._events[self._event_index]
        self._event_index += 1

        if action == "beep":
            # winsound.Beep is blocking for 'duration' ms, so we keep beeps short.
            winsound.Beep(FREQ, duration)
            # schedule next event immediately after
            self._after_id = self.root.after(1, self._play_next_event)
        else:
            # silence: just wait duration, then continue
            self._after_id = self.root.after(duration, self._play_next_event)


def on_convert():
    user_text = input_box.get("1.0", END)
    morse = text_to_morse(user_text)
    display_label.config(text=morse)
    status_label.config(text="Status: Converted")


def on_play():
    morse = display_label.cget("text")
    player.play(morse)


def on_clear():
    player.stop()
    input_box.delete("1.0", END)
    display_label.config(text="")
    status_label.config(text="Status: Cleared")


# --- UI setup ---
root = Tk()
root.title("Text to Morse")
root.configure(background=BACKGROUND)
root.minsize(400, 600)
root.maxsize(400, 600)

player = MorsePlayer(root)

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

status_label = Label(
    root,
    text="Status: Ready",
    font=("Courier", 10, "bold"),
    background=BACKGROUND
)

input_box = Text(root, width=30, height=5)

convert_button = Button(
    root,
    text="Convert",
    command=on_convert,
    font=("Courier", 10, "bold"),
    background="#C6A27E"
)

play_button = Button(
    root,
    text="Play Beeps",
    command=on_play,
    font=("Courier", 10, "bold"),
    background="#C6A27E"
)

stop_button = Button(
    root,
    text="Stop",
    command=player.stop,
    font=("Courier", 10, "bold"),
    background="#C6A27E"
)

clear_button = Button(
    root,
    text="Clear",
    command=on_clear,
    font=("Courier", 10, "bold"),
    background="#C6A27E"
)

# Layout
title_label.grid(column=0, row=0, columnspan=3, pady=25, padx=20)
display_label.grid(column=0, row=1, columnspan=3, pady=10, padx=10)
status_label.grid(column=0, row=2, columnspan=3, pady=5)

input_box.grid(column=0, row=3, columnspan=3, pady=10, padx=10)

convert_button.grid(column=0, row=4, pady=10, padx=8)
play_button.grid(column=1, row=4, pady=10, padx=8)
stop_button.grid(column=2, row=4, pady=10, padx=8)
clear_button.grid(column=1, row=5, pady=10, padx=8)

root.mainloop()
