"""Timed trainer - display chord for a set duration then auto-advance."""

import os
import time
from .trainer import ChordTrainer


class TimedTrainer(ChordTrainer):
    """Timed chord trainer - automatically advances after interval."""
    
    def __init__(self, interval=3, **kwargs):
        """Initialize timed trainer.
        
        Args:
            interval: Duration in seconds to show each chord
        """
        super().__init__(**kwargs)
        self.interval = interval
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def run(self):
        """Run the timed training session."""
        try:
            while True:
                self.clear_screen()
                symbol, notes_list = self.generate_chord()
                print(f"\n{'='*50}")
                print(f"Play: {symbol}")
                print(f"Notes: {self.format_notes(notes_list)}")
                print(f"{'='*50}")
                print(f"\nNext chord in {self.interval} seconds...\n(Ctrl+C to exit)")
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\n\nTraining session ended!")
    
    @staticmethod
    def get_interval_from_user():
        """Get training interval from user input.
        
        Returns:
            int: Interval in seconds
        """
        while True:
            try:
                interval = int(input("Enter interval in seconds: "))
                if interval <= 0:
                    raise ValueError
                return interval
            except ValueError:
                print("Please enter a positive integer\n")


if __name__ == "__main__":
    interval = TimedTrainer.get_interval_from_user()
    trainer = TimedTrainer(interval=interval)
    trainer.run()
