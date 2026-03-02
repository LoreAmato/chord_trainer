"""Metronome trainer - play chords with metronome beat synchronization."""

import os
import time
import threading
import winsound
try:
    import pygame
except Exception:
    pygame = None

from .trainer import ChordTrainer


class MetronomeTrainer(ChordTrainer):
    """Metronome chord trainer - chords change every 4 beats with metronome."""
    
    def __init__(self, bpm=120, **kwargs):
        """Initialize metronome trainer.
        
        Args:
            bpm: Beats per minute for the metronome
        """
        super().__init__(**kwargs)
        self.bpm = bpm
        self.beat_duration = 60.0 / bpm  # Duration of one beat in seconds
        self.chord_duration = self.beat_duration * 4  # Display each chord for 4 beats
        self.running = False
        self.current_chord_symbol = None
        self.current_chord_notes = None
        self.next_chord_symbol = None
        self.next_chord_notes = None
        self.beat_count = 0  # Track which beat in the measure

        # Try to initialize pygame mixer and preload sounds for low-latency playback
        self.use_pygame = False
        if pygame is not None:
            try:
                # init mixer if not already initialized
                if not pygame.mixer.get_init():
                    pygame.mixer.init()

                base_path = os.path.dirname(os.path.abspath(__file__))
                sound_folder = os.path.join(base_path, "..", "sounds")
                high_path = os.path.join(sound_folder, "click_high.wav")
                low_path = os.path.join(sound_folder, "click_low.wav")

                self.click_high = pygame.mixer.Sound(high_path)
                self.click_low = pygame.mixer.Sound(low_path)
                pygame.mixer.set_num_channels(2)
                self.channel_high = pygame.mixer.Channel(0)
                self.channel_low = pygame.mixer.Channel(1)
                self.use_pygame = True
            except Exception:
                # fallback to winsound if pygame setup fails
                self.use_pygame = False
        
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def play_beep(self, is_downbeat=False):
        # Use pygame mixer if available for lower-latency playback, otherwise fallback to winsound
        if self.use_pygame:
            if is_downbeat:
                # play on reserved channel to avoid allocation latency
                self.channel_high.play(self.click_high)
            else:
                self.channel_low.play(self.click_low)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            sound_folder = os.path.join(base_path, "..", "sounds")
            sound_file = "click_high.wav" if is_downbeat else "click_low.wav"
            full_path = os.path.join(sound_folder, sound_file)
            winsound.PlaySound(full_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    def run_metronome_loop(self):
        """Run the metronome beat loop in a separate thread."""
        # Use perf_counter for more precise timing
        next_beat_time = time.perf_counter()

        while self.running:
            now = time.perf_counter()
            if now >= next_beat_time:
                is_down = (self.beat_count % 4 == 0)
                self.play_beep(is_downbeat=is_down)
                self.beat_count += 1
                # schedule next beat based on precise interval
                next_beat_time += self.beat_duration

                # chord change exactly when beat_count is multiple of 4 (i.e., after the 4th beat)
                if self.beat_count % 4 == 0:
                    self.current_chord_symbol = self.next_chord_symbol
                    self.current_chord_notes = self.next_chord_notes
                    self.next_chord_symbol, self.next_chord_notes = self.generate_chord()

            # sleep a tiny amount to yield CPU, keeping loop responsive
            time.sleep(0.001)
        
    
    def run(self):
        """Run the metronome training session."""
        try:
            self.running = True
            
            # Generate initial chords
            self.current_chord_symbol, self.current_chord_notes = self.generate_chord()
            self.next_chord_symbol, self.next_chord_notes = self.generate_chord()
            
            # Start metronome loop
            metronome_thread = threading.Thread(target=self.run_metronome_loop, daemon=True)
            metronome_thread.start()
            
            # Display loop
            while self.running:
                self.clear_screen()
                print(f"\n{'='*60}")
                print(f"BPM: {self.bpm} | Chord changes every 4 beats")
                print(f"{'='*60}\n")
                
                # Display current chord (highlighted)
                print(f"CURRENT (play this):")
                print(f"  {self.current_chord_symbol}")
                if self.current_chord_notes:
                    print(f"  {self.format_notes(self.current_chord_notes)}")
                
                print(f"\n{'─'*60}\n")
                
                # Display next chord (upcoming)
                print(f"NEXT:")
                print(f"  {self.next_chord_symbol}")
                if self.next_chord_notes:
                    print(f"  {self.format_notes(self.next_chord_notes)}")
                
                print(f"\n{'='*60}")
                print("(Ctrl+C to exit)")
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            self.running = False
            print("\n\nTraining session ended!")
    
    @staticmethod
    def get_bpm_from_user():
        """Get BPM from user input.
        
        Returns:
            int: BPM value
        """
        while True:
            try:
                bpm = int(input("Enter BPM (beats per minute): "))
                if bpm <= 0 or bpm > 300:
                    raise ValueError
                return bpm
            except ValueError:
                print("Please enter a BPM between 1 and 300\n")


if __name__ == "__main__":
    bpm = MetronomeTrainer.get_bpm_from_user()
    trainer = MetronomeTrainer(bpm=bpm)
    trainer.run()
