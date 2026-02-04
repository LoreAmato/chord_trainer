"""Core trainer logic for chord generation and management."""

import random
from mingus.core import chords as mingus_chords
from mingus.core import notes


class ChordTrainer:
    """Base class for chord training utilities."""
    
    # Default chord types and root notes
    CHORD_TYPES = ['maj7', 'm7', '7', 'm7b5', '7b5']
    ROOT_NOTES = ['A', 'A', 'A#', 'Bb', 'B', 'B', 'C', 'C', 'C#', 'Db', 'D', 'D', 
                  'D#', 'Eb', 'E', 'E', 'F', 'F', 'F#', 'Gb', 'G', 'G', 'G#', 'Ab']
    
    def __init__(self, chord_types=None, root_notes=None):
        """Initialize trainer with optional custom chord types and root notes."""
        self.chord_types = chord_types or self.CHORD_TYPES
        self.root_notes = root_notes or self.ROOT_NOTES
    
    def generate_chord(self):
        """Generate a random chord symbol and its notes.
        
        Returns:
            tuple: (chord_symbol, list of notes)
        """
        root = random.choice(self.root_notes)
        chord_type = random.choice(self.chord_types)
        symbol = f"{root}{chord_type}"
        
        try:
            chord_notes = mingus_chords.from_shorthand(symbol)
        except Exception:
            chord_notes = []
        
        return symbol, chord_notes
    
    @staticmethod
    def format_notes(notes_list):
        """Format notes with their scale degrees.
        
        Args:
            notes_list: List of note names
            
        Returns:
            str: Formatted string like "root=C, 3rd=E, 5th=G, 7th=B"
        """
        labels = ['root', '3rd', '5th', '7th']
        return ", ".join([f"{labels[i]}={notes.reduce_accidentals(n)}" 
                         for i, n in enumerate(notes_list)])
