"""GUI application for the Chord Trainer."""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from src.trainer import ChordTrainer
from src.manual_trainer import ManualTrainer
from src.timed_trainer import TimedTrainer


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
        
        # Info frame
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        info_text = (
            "Manual Mode: Self-paced training. You control when to advance.\n\n"
            "Timed Mode: Automatic progression. Chords change at set intervals.\n\n"
            "Chord Types: maj7, m7, 7, m7b5, 7b5\n"
            "Keys: All 12 chromatic notes"
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
        self.trainer = None
        # Remove global space binding to avoid interference when not training
        try:
            self.root.unbind_all("<space>")
        except Exception:
            pass
        self.show_main_menu()


def main():
    """Run the chord trainer GUI."""
    root = tk.Tk()
    app = ChordTrainerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
