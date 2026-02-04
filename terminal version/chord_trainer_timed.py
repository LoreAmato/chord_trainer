import random
import os
import time
from mingus.core import chords as mingus_chords
from mingus.core import notes

chord_types = ['maj7', 'm7', '7', 'm7b5', '7b5']
root_notes = ['A', 'A', 'A#', 'Bb', 'B', 'B', 'C', 'C', 'C#', 'Db', 'D', 'D', 'D#', 'Eb', 'E', 'E', 'F', 'F', 'F#', 'Gb', 'G', 'G', 'G#', 'Ab']

def generate_chord():
    root = random.choice(root_notes)
    chord_type = random.choice(chord_types)
    symbol = f"{root}{chord_type}"
    try:
        chord_notes = mingus_chords.from_shorthand(symbol)
    except:
        chord_notes = []
    return symbol, chord_notes

def format_notes(notes_list):
    labels = ['root', '3rd', '5th', '7th']
    return ", ".join([f"{labels[i]}={notes.reduce_accidentals(n)}" 
                     for i, n in enumerate(notes_list)])

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Get interval from user
    while True:
        try:
            interval = int(input("Enter interval in seconds: "))
            if interval <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer\n")

    # Main loop
    try:
        while True:
            clear_screen()
            symbol, notes_list = generate_chord()
            print(f"Play: {symbol}")
            print(f"Notes: {format_notes(notes_list)}")
            print(f"\nNext chord in {interval} seconds...")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nTraining session ended!")

if __name__ == "__main__":
    main()