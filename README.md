# Chord Trainer

A flexible chord training tool for musicians. Ideal for practicing chord chart recognition and muscle memory, with both manual and timed training modes.

This repository is born from my need to improve fretboard memorization on guitar and bass, but can be used on any instrument and for whatever need. In the following, a few tips.

### Practice tips:
- You can limit yourself to roots on a single string or in a certain area of the neck (if on guitar or bass); 
- Rather than playing chords, you can play arpeggios;
- You can choose to play chords not in root position: for instance, have a session where you only play chords in first inversion.
- You should always practice jazz standards too, as chords are not quite in a random sequence in real music!

## Features

- **Manual Mode**: Self-paced training where you control when to advance to the next chord;
- **Timed Mode**: Automatic progression with customizable time intervals between chords;
- **Multiple Chord Types**: Maj7, m7, 7, m7b5, 7b5 (in all keys);
- **Automatic Chord tones breakdown**: Everytime a chord is proposed, you can see its root, 3rd, 5th and 7th.

## Installation

1. Clone the repository:
2. Create a virtual environment (recommended):
3. Install mingus:
```bash
pip install mingus
```

## Usage

### GUI Application (Recommended)
```bash
python main.py
```

The GUI allows you to:
1. Select between Manual or Timed training modes;
2. Configure settings (interval for timed mode);
3. Display chord names and chord tones.


### Command Line

You can also use the command line version of the two training programs, which you can find in the "terminal version" folder.

## Chord Types

The trainer includes the common 7th chord types found in most jazz standards (excluding diminished and the rather uncommon minMaj7):
- **maj7**: Major 7th chord
- **m7**: Minor 7th chord
- **7**: Dominant 7th chord
- **m7b5**: Half-diminished 7th chord
- **7b5**: Diminished 7th chord

You can add other chord types and extensions by editing the `CHORD_TYPES` constant in "src/trainer.py" to include different chord qualities (check the mingus documentation [here](https://bspaans.github.io/python-mingus/) to see the full list).




