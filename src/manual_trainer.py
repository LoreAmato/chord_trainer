"""Manual trainer - display chord and wait for user to press next."""

import os
from .trainer import ChordTrainer


class ManualTrainer(ChordTrainer):
    """Manual chord trainer - user controls when to advance."""
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def run(self):
        """Run the manual training session."""
        try:
            while True:
                self.clear_screen()
                symbol, notes_list = self.generate_chord()
                print(f"\n{'='*50}")
                print(f"Play: {symbol}")
                print(f"Notes: {self.format_notes(notes_list)}")
                print(f"{'='*50}")
                print("\nPress ENTER for next chord (Ctrl+C to exit)")
                input()
        except KeyboardInterrupt:
            print("\n\nTraining session ended!")


if __name__ == "__main__":
    trainer = ManualTrainer()
    trainer.run()
