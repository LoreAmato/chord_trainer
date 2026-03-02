"""GUI application for the Chord Trainer."""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from src.trainer import ChordTrainer
from src.manual_trainer import ManualTrainer
from src.timed_trainer import TimedTrainer
from src.metronome_trainer import MetronomeTrainer


class ChordTrainerGUI:
    """Main GUI application for chord training."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Chord Trainer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style: prefer a native/clean theme and ensure white background
        style = ttk.Style()
        available = style.theme_names()
        if 'vista' in available:
            style.theme_use('vista')
        elif 'clam' in available:
            style.theme_use('clam')
        else:
            # fallback to the first available theme
            style.theme_use(available[0])

        # Ensure consistent white background for root and ttk widgets
        self.root.configure(bg='white')
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white', foreground='#111827')
        style.configure('TButton', padding=6)
        # Spinbox/Entry backgrounds may be platform dependent
        try:
            style.configure('TSpinbox', fieldbackground='white', background='white')
        except Exception:
            pass
        
        self.training_active = False
        self.trainer = None
        self.current_chord = None
        self.current_notes = None
        self.time_remaining = 0
        self.metronome_running = False
        self.metronome_beat_count = 0
        
        self.show_main_menu()
    
    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Display the main menu."""
        self.clear_window()
        
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(
            title_frame,
            text="Chord Trainer",
            font=("Arial", 28, "bold")
        )
        title_label.pack()
        
        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=40, expand=True)
        
        # Manual mode button
        manual_btn = ttk.Button(
            button_frame,
            text="Manual Training",
            command=self.show_manual_config,
            width=30
        )
        manual_btn.pack(pady=15)
        
        # Timed mode button
        timed_btn = ttk.Button(
            button_frame,
            text="Timed Training",
            command=self.show_timed_config,
            width=30
        )
        timed_btn.pack(pady=15)
        
        # Metronome mode button
        metronome_btn = ttk.Button(
            button_frame,
            text="Metronome Training",
            command=self.show_metronome_config,
            width=30
        )
        metronome_btn.pack(pady=15)
        
        # Info frame
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        info_text = (
            "Manual Mode: Self-paced training. You control when to advance.\n\n"
            "Timed Mode: Automatic progression. Chords change at set intervals.\n\n"
            "Metronome Mode: Chords change every 4 beats with metronome sound.\n\n"
            "Chord Types: maj7, m7, 7, m7b5, 7b5 | Keys: All 12 chromatic notes"
        )
        
        info_label = ttk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 10),
            justify=tk.LEFT
        )
        info_label.pack()
    
    def show_manual_config(self):
        """Show configuration for manual training."""
        self.clear_window()
        
        # Back button
        back_btn = ttk.Button(
            self.root,
            text="← Back",
            command=self.show_main_menu,
            width=15
        )
        back_btn.pack(anchor=tk.NW, padx=10, pady=10)
        
        # Title
        title = ttk.Label(
            self.root,
            text="Manual Training",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # Info
        info = ttk.Label(
            self.root,
            text="Self-paced chord training.\nPress NEXT or SPACE to advance to the next chord.",
            font=("Arial", 11),
            justify=tk.CENTER
        )
        info.pack(pady=10)
        
        # Start button
        start_btn = ttk.Button(
            self.root,
            text="Start Training",
            command=self.start_manual_training,
            width=30
        )
        start_btn.pack(pady=30)
    
    def show_timed_config(self):
        """Show configuration for timed training."""
        self.clear_window()
        
        # Back button
        back_btn = ttk.Button(
            self.root,
            text="← Back",
            command=self.show_main_menu,
            width=15
        )
        back_btn.pack(anchor=tk.NW, padx=10, pady=10)
        
        # Title
        title = ttk.Label(
            self.root,
            text="Timed Training",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # Info
        info = ttk.Label(
            self.root,
            text="Automatic chord progression at set intervals.",
            font=("Arial", 11)
        )
        info.pack(pady=10)
        
        # Configuration frame
        config_frame = ttk.Frame(self.root)
        config_frame.pack(pady=30)
        
        # Interval label
        interval_label = ttk.Label(
            config_frame,
            text="Interval (seconds):",
            font=("Arial", 11)
        )
        interval_label.pack()
        
        # Interval spinbox
        self.interval_var = tk.IntVar(value=3)
        interval_spinbox = ttk.Spinbox(
            config_frame,
            from_=1,
            to=30,
            textvariable=self.interval_var,
            width=10,
            font=("Arial", 12)
        )
        interval_spinbox.pack(pady=10)
        
       
        # Start button
        start_btn = ttk.Button(
            self.root,
            text="Start Training",
            command=self.start_timed_training,
            width=30
        )
        start_btn.pack(pady=30)
    
    def start_manual_training(self):
        """Start manual training session."""
        self.trainer = ManualTrainer()
        self.training_active = True
        self.show_manual_training()
    
    def start_timed_training(self):
        """Start timed training session."""
        interval = self.interval_var.get()
        self.trainer = TimedTrainer(interval=interval)
        self.training_active = True
        self.show_timed_training()
    
    def show_manual_training(self):
        """Display the manual training interface."""
        self.clear_window()
        
        # Top button frame
        top_frame = ttk.Frame(self.root)
        top_frame.pack(anchor=tk.NW, padx=10, pady=10)
        
        exit_btn = ttk.Button(
            top_frame,
            text="Exit Training",
            command=self.exit_training
        )
        exit_btn.pack()
        
        # Main display frame
        display_frame = ttk.Frame(self.root)
        display_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Chord display
        self.chord_label = ttk.Label(
            display_frame,
            text="Ready",
            font=("Arial", 48, "bold"),
            foreground="#2563eb"
        )
        self.chord_label.pack(pady=20)
        
        # Notes display
        self.notes_label = ttk.Label(
            display_frame,
            text="Press SPACE or click NEXT to start",
            font=("Arial", 14),
            foreground="#666666"
        )
        self.notes_label.pack(pady=10)
        
        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        next_btn = ttk.Button(
            button_frame,
            text="NEXT CHORD",
            command=self.manual_next_chord,
            width=20
        )
        next_btn.pack()
        
        # Bind space bar to next chord (use bind_all so focus doesn't matter)
        self.root.bind_all("<space>", lambda e: self.manual_next_chord())
        
        # Display initial chord
        self.manual_next_chord()
    
    def show_timed_training(self):
        """Display the timed training interface."""
        self.clear_window()
        
        # Top button frame
        top_frame = ttk.Frame(self.root)
        top_frame.pack(anchor=tk.NW, padx=10, pady=10)
        
        exit_btn = ttk.Button(
            top_frame,
            text="Exit Training",
            command=self.exit_training
        )
        exit_btn.pack()
        
        # Main display frame
        display_frame = ttk.Frame(self.root)
        display_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Chord display
        self.chord_label = ttk.Label(
            display_frame,
            text="Ready",
            font=("Arial", 48, "bold"),
            foreground="#2563eb"
        )
        self.chord_label.pack(pady=20)
        
        # Notes display
        self.notes_label = ttk.Label(
            display_frame,
            text="Get ready...",
            font=("Arial", 14),
            foreground="#666666"
        )
        self.notes_label.pack(pady=10)
        
        # Timer display
        self.timer_label = ttk.Label(
            display_frame,
            text="",
            font=("Arial", 28),
            foreground="#dc2626"
        )
        self.timer_label.pack(pady=20)
        
        # Start timed loop in background
        self.timed_loop()
    
    def manual_next_chord(self):
        """Display next chord in manual mode."""
        symbol, notes_list = self.trainer.generate_chord()
        self.chord_label.config(text=symbol)
        formatted_notes = self.trainer.format_notes(notes_list)
        self.notes_label.config(text=formatted_notes)
    
    def timed_loop(self):
        """Run the timed training loop."""
        if not self.training_active:
            return
        
        # Generate chord
        symbol, notes_list = self.trainer.generate_chord()
        self.chord_label.config(text=symbol)
        formatted_notes = self.trainer.format_notes(notes_list)
        self.notes_label.config(text=formatted_notes)
        
        # Show countdown
        interval = self.trainer.interval
        
        def countdown():
            for remaining in range(interval, 0, -1):
                if not self.training_active:
                    return
                self.timer_label.config(text=str(remaining))
                self.root.update()
                time.sleep(1)
            
            if self.training_active:
                self.timer_label.config(text="")
                self.timed_loop()
        
        # Run countdown in separate thread
        thread = threading.Thread(target=countdown, daemon=True)
        thread.start()
    
    def exit_training(self):
        """Exit training and return to main menu."""
        self.training_active = False
        self.metronome_running = False
        self.trainer = None
        # Remove global space binding to avoid interference when not training
        try:
            self.root.unbind_all("<space>")
        except Exception:
            pass
        self.show_main_menu()
    
    def show_metronome_config(self):
        """Show configuration for metronome training."""
        self.clear_window()
        
        # Back button
        back_btn = ttk.Button(
            self.root,
            text="← Back",
            command=self.show_main_menu,
            width=15
        )
        back_btn.pack(anchor=tk.NW, padx=10, pady=10)
        
        # Title
        title = ttk.Label(
            self.root,
            text="Metronome Training",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # Info
        info = ttk.Label(
            self.root,
            text="Practice with a metronome. Chords change every 4 beats.\nTwo chords are shown: current (left/highlighted) and next (right).",
            font=("Arial", 11),
            justify=tk.CENTER
        )
        info.pack(pady=10)
        
        # Configuration frame
        config_frame = ttk.Frame(self.root)
        config_frame.pack(pady=30)
        
        # BPM label
        bpm_label = ttk.Label(
            config_frame,
            text="BPM (Beats Per Minute):",
            font=("Arial", 11)
        )
        bpm_label.pack()
        
        # BPM spinbox
        self.bpm_var = tk.IntVar(value=120)
        bpm_spinbox = ttk.Spinbox(
            config_frame,
            from_=30,
            to=300,
            textvariable=self.bpm_var,
            width=10,
            font=("Arial", 12)
        )
        bpm_spinbox.pack(pady=10)
        
        # Start button
        start_btn = ttk.Button(
            self.root,
            text="Start Training",
            command=self.start_metronome_training,
            width=30
        )
        start_btn.pack(pady=30)
    
    def start_metronome_training(self):
        """Start metronome training session."""
        bpm = self.bpm_var.get()
        self.trainer = MetronomeTrainer(bpm=bpm)
        self.training_active = True
        self.metronome_running = True
        self.metronome_beat_count = 0
        self.show_metronome_training()
    
    def show_metronome_training(self):
        """Display the metronome training interface."""
        self.clear_window()
        
        # Top button frame
        top_frame = ttk.Frame(self.root)
        top_frame.pack(anchor=tk.NW, padx=10, pady=10)
        
        exit_btn = ttk.Button(
            top_frame,
            text="Exit Training",
            command=self.exit_training
        )
        exit_btn.pack()
        
        # BPM info
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=10)
        
        bpm_info = ttk.Label(
            info_frame,
            text=f"BPM: {self.trainer.bpm} | Chord changes every 4 beats",
            font=("Arial", 11),
            foreground="#666666"
        )
        bpm_info.pack()
        
        # Main display frame with two chords side by side
        display_frame = ttk.Frame(self.root)
        display_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Create two columns
        left_frame = ttk.Frame(display_frame)
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        
        right_frame = ttk.Frame(display_frame)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10)
        
        # Left side - CURRENT chord (highlighted)
        left_label = ttk.Label(
            left_frame,
            text="CURRENT",
            font=("Arial", 12, "bold"),
            foreground="#2563eb"
        )
        left_label.pack(pady=10)
        
        self.metronome_current_chord = ttk.Label(
            left_frame,
            text="Ready",
            font=("Arial", 56, "bold"),
            foreground="#2563eb"
        )
        self.metronome_current_chord.pack(pady=10)
        
        self.metronome_current_notes = ttk.Label(
            left_frame,
            text="",
            font=("Arial", 11),
            foreground="#666666",
            justify=tk.CENTER,
            wraplength=200
        )
        self.metronome_current_notes.pack(pady=10)
        
        # Divider
        divider = ttk.Frame(display_frame, height=2)
        divider.pack(side=tk.LEFT, fill=tk.Y, padx=20)
        
        # Right side - NEXT chord
        right_label = ttk.Label(
            right_frame,
            text="NEXT",
            font=("Arial", 12),
            foreground="#999999"
        )
        right_label.pack(pady=10)
        
        self.metronome_next_chord = ttk.Label(
            right_frame,
            text="Ready",
            font=("Arial", 56),
            foreground="#cccccc"
        )
        self.metronome_next_chord.pack(pady=10)
        
        self.metronome_next_notes = ttk.Label(
            right_frame,
            text="",
            font=("Arial", 11),
            foreground="#999999",
            justify=tk.CENTER,
            wraplength=200
        )
        self.metronome_next_notes.pack(pady=10)
        
        # Beat indicator at bottom
        self.metronome_beat_indicator = ttk.Label(
            self.root,
            text="♩",
            font=("Arial", 28),
            foreground="#dc2626"
        )
        self.metronome_beat_indicator.pack(pady=10)
        
        # Initialize chords
        self.trainer.current_chord_symbol, self.trainer.current_chord_notes = self.trainer.generate_chord()
        self.trainer.next_chord_symbol, self.trainer.next_chord_notes = self.trainer.generate_chord()
        self.update_metronome_display()
        
        # Start metronome loop in background
        self.metronome_loop()
    
    def update_metronome_display(self):
        """Update the metronome display with current and next chords."""
        if not self.training_active:
            return
        
        # Update current chord (left)
        self.metronome_current_chord.config(
            text=self.trainer.current_chord_symbol
        )
        if self.trainer.current_chord_notes:
            formatted = self.trainer.format_notes(self.trainer.current_chord_notes)
            self.metronome_current_notes.config(text=formatted)
        
        # Update next chord (right)
        self.metronome_next_chord.config(
            text=self.trainer.next_chord_symbol
        )
        if self.trainer.next_chord_notes:
            formatted = self.trainer.format_notes(self.trainer.next_chord_notes)
            self.metronome_next_notes.config(text=formatted)
    
    def metronome_loop(self):
        """Run the metronome training loop."""
        if not self.training_active or not self.metronome_running:
            return
        
        beat_duration = self.trainer.beat_duration
        last_beat_time = time.time()
        
        def metronome_worker():
            nonlocal last_beat_time
            
            while self.training_active and self.metronome_running:
                current_time = time.time()
                elapsed = current_time - last_beat_time
                
                if elapsed >= beat_duration:
                    self.metronome_beat_count += 1

                    # Play metronome sound for this beat (downbeat every 4th beat)
                    try:
                        is_downbeat = (self.metronome_beat_count % 4 == 0)
                        # call trainer's play_beep which will print/debug and play sound
                        if hasattr(self.trainer, 'play_beep'):
                            self.trainer.play_beep(is_downbeat=is_downbeat)
                    except Exception:
                        # Keep GUI responsive if sound playback fails
                        pass

                    # Visual metronome beat indication
                    self.metronome_beat_indicator.config(foreground="#dc2626")
                    self.root.update()
                    time.sleep(0.1)
                    self.metronome_beat_indicator.config(foreground="#999999")
                    self.root.update()
                    
                    # Change chord every 4 beats
                    if self.metronome_beat_count % 4 == 0:
                        self.trainer.current_chord_symbol = self.trainer.next_chord_symbol
                        self.trainer.current_chord_notes = self.trainer.next_chord_notes
                        self.trainer.next_chord_symbol, self.trainer.next_chord_notes = self.trainer.generate_chord()
                        self.update_metronome_display()
                    
                    last_beat_time = current_time
                
                time.sleep(0.01)
        
        # Run metronome in separate thread
        thread = threading.Thread(target=metronome_worker, daemon=True)
        thread.start()


def main():
    """Run the chord trainer GUI."""
    root = tk.Tk()
    app = ChordTrainerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
