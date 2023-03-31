import tkinter as tk


class GenreSelector:
    """Allows the user to select genres they are interested in."""

    def __init__(self, parent):
        self.parent = parent
        self.genres = []

        # Create a frame to hold the checkboxes
        self.checkbox_frame = tk.Frame(parent)
        self.checkbox_frame.grid(row=1, column=0, padx=10, pady=10)

        # Create genre checkboxes
        self.action_var = tk.BooleanVar()
        self.action_checkbox = tk.Checkbutton(self.checkbox_frame, text="Action", variable=self.action_var, font=("Arial", 12))
        self.action_checkbox.grid(row=0, column=0, padx=10, pady=10)

        self.adventure_var = tk.BooleanVar()
        self.adventure_checkbox = tk.Checkbutton(self.checkbox_frame, text="Adventure", variable=self.adventure_var,
                                                 font=("Arial", 12))
        self.adventure_checkbox.grid(row=0, column=1, padx=10, pady=10)

        self.rpg_var = tk.BooleanVar()
        self.rpg_checkbox = tk.Checkbutton(self.checkbox_frame, text="RPG", variable=self.rpg_var, font=("Arial", 12))
        self.rpg_checkbox.grid(row=0, column=2, padx=10, pady=10)

        self.stealth_var = tk.BooleanVar()
        self.stealth_checkbox = tk.Checkbutton(self.checkbox_frame, text="Stealth", variable=self.stealth_var, font=("Arial", 12))
        self.stealth_checkbox.grid(row=1, column=0, padx=10, pady=10)

        self.puzzle_var = tk.BooleanVar()
        self.puzzle_checkbox = tk.Checkbutton(self.checkbox_frame, text="Puzzle", variable=self.puzzle_var, font=("Arial", 12))
        self.puzzle_checkbox.grid(row=1, column=1, padx=10, pady=10)

        self.coop_var = tk.BooleanVar()
        self.coop_checkbox = tk.Checkbutton(self.checkbox_frame, text="Co-op", variable=self.coop_var, font=("Arial", 12))
        self.coop_checkbox.grid(row=1, column=2, padx=10, pady=10)

        # Create "Submit" button
        self.submit_button = tk.Button(parent, text="Submit", command=self.submit, font=("Arial", 14), bg="#4CAF50",
                                       fg="white", pady=10)
        self.submit_button.grid(row=2, column=0, pady=10)

    def submit(self):
        """Stores selected genres in a list."""
        if self.action_var.get():
            self.genres.append("Action")
        if self.adventure_var.get():
            self.genres.append("Adventure")
        if self.rpg_var.get():
            self.genres.append("RPG")
        if self.stealth_var.get():
            self.genres.append("Stealth")
        if self.puzzle_var.get():
            self.genres.append("Puzzle")
        if self.coop_var.get():
            self.genres.append("Co-op")

        # Destroy genre selector window
        self.parent.destroy()
