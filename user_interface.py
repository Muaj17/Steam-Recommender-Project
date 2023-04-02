import tkinter as tk
from tkinter import messagebox


class GameIDSelector:
    """Allows the user to input game IDs."""

    def __init__(self, games) -> None:
        self.root = tk.Tk()
        self.games = games
        self.game_ids = []

        self.root.title("Steam Game Recommender")
        self.root.geometry("1920x1080")

        # Create a label for the intro text
        intro_text = tk.Label(self.root,
                              text="Welcome to the Steam Game Recommender!\nThis program will recommend the top 5"
                                   " steam games"
                                   " you should play based on games you've played in the past and your preference of "
                                   "genre.\nPlease input the game ids of steam games you've played before.\n To find "
                                   "the id of the game, you can use a website like https://steamdb.info/apps/.",
                              font=("Arial", 14))
        intro_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Create a label and entry for entering game IDs
        self.game_id_label = tk.Label(self.root, text="Enter a game ID:", font=("Arial", 12))
        self.game_id_label.grid(row=1, column=0, padx=10, pady=10)

        self.game_id_entry = tk.Entry(self.root, font=("Arial", 12))
        self.game_id_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create "Add" and "Done" buttons
        self.add_button = tk.Button(self.root, text="Add", command=self.add_game_id, font=("Arial", 12), bg="#4CAF50",
                                    fg="white")
        self.add_button.grid(row=2, column=0, padx=10, pady=10)

        self.done_button = tk.Button(self.root, text="Done", command=self.submit, font=("Arial", 12), bg="#008CBA",
                                     fg="white")
        self.done_button.grid(row=2, column=1, padx=10, pady=10)

        self.root.mainloop()

    def add_game_id(self) -> None:
        """Adds a game ID to the list."""
        try:
            game_id = int(self.game_id_entry.get())
            if game_id in self.games and game_id not in self.game_ids:
                self.game_ids.append(game_id)
                self.game_id_entry.delete(0, tk.END)
            else:
                tk.messagebox.showwarning("Invalid Game ID", "The game ID you entered is not valid.")
        except ValueError:
            tk.messagebox.showwarning("Invalid Input", "Please enter a valid integer.")

    def submit(self) -> None:
        """Destroys the window."""
        if len(self.game_ids) == 0:
            tk.messagebox.showwarning("No Game IDs Added", "Please add at least one game ID.")
        else:
            self.root.destroy()
            # GenreSelector(tk.Tk())

    def get_game_ids(self) -> list[int]:
        """Returns the list of game IDs."""
        return self.game_ids


class GenreSelector:
    """Allows the user to select genres they are interested in."""

    def __init__(self):
        self.root = tk.Tk()
        self.genres = []

        self.root.title("Steam Game Recommender")
        self.root.geometry("1920x1080")

        # Create a label for instructions
        instructions_text = tk.Label(self.root,
                                     text="Please select the genres you're interested in.",
                                     font=("Arial", 14))
        instructions_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Create a frame to hold the checkboxes
        self.checkbox_frame = tk.Frame(self.root)
        self.checkbox_frame.grid(row=1, column=0, padx=10, pady=10)

        # Create genre checkboxes
        self.action_var = tk.BooleanVar()
        self.action_checkbox = tk.Checkbutton(self.checkbox_frame, text="Action", variable=self.action_var,
                                              font=("Arial", 12))
        self.action_checkbox.grid(row=0, column=0, padx=10, pady=10)

        self.adventure_var = tk.BooleanVar()
        self.adventure_checkbox = tk.Checkbutton(self.checkbox_frame, text="Adventure", variable=self.adventure_var,
                                                 font=("Arial", 12))
        self.adventure_checkbox.grid(row=0, column=1, padx=10, pady=10)

        self.rpg_var = tk.BooleanVar()
        self.rpg_checkbox = tk.Checkbutton(self.checkbox_frame, text="RPG", variable=self.rpg_var, font=("Arial", 12))
        self.rpg_checkbox.grid(row=0, column=2, padx=10, pady=10)

        self.stealth_var = tk.BooleanVar()
        self.stealth_checkbox = tk.Checkbutton(self.checkbox_frame, text="Stealth", variable=self.stealth_var,
                                               font=("Arial", 12))
        self.stealth_checkbox.grid(row=1, column=0, padx=10, pady=10)

        self.puzzle_var = tk.BooleanVar()
        self.puzzle_checkbox = tk.Checkbutton(self.checkbox_frame, text="Puzzle", variable=self.puzzle_var,
                                              font=("Arial", 12))
        self.puzzle_checkbox.grid(row=1, column=1, padx=10, pady=10)

        self.coop_var = tk.BooleanVar()
        self.coop_checkbox = tk.Checkbutton(self.checkbox_frame, text="Co-op", variable=self.coop_var,
                                            font=("Arial", 12))
        self.coop_checkbox.grid(row=1, column=2, padx=10, pady=10)

        # Create "Submit" button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit, font=("Arial", 14), bg="#4CAF50",
                                       fg="white", pady=10)
        self.submit_button.grid(row=2, column=0, pady=10)

        self.root.mainloop()

    def submit(self):
        """Stores selected genres in a list."""
        if not any([self.action_var.get(), self.adventure_var.get(), self.rpg_var.get(),
                    self.stealth_var.get(), self.puzzle_var.get(), self.coop_var.get()]):
            # Display an error message if no genres are selected
            error_text = tk.Label(self.root,
                                  text="Please select at least one genre.",
                                  font=("Arial", 14),
                                  fg="red")
            error_text.grid(row=3, column=0, pady=10)
            return

        # Add selected genres to the list
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
        self.root.destroy()

    def get_genres(self) -> list[str]:
        """Returns the list of game IDs."""
        return self.genres


class MaxPrice:
    """Asks the user to input the maximum amoount of money they are willing to spend on a steam game."""

    def __init__(self):
        self.price = 0.0

        self.root = tk.Tk()
        self.root.title("Steam Game Recommender")
        self.root.geometry("1920x1080")

        self.label = tk.Label(self.root, text="Please enter the maximum amount of dollars you're willing to spend (in "
                                              "USD):", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.button = tk.Button(self.root, text="Submit", command=self.submit)
        self.button.pack(pady=10)

        self.root.mainloop()

    def submit(self):
        """This method submits the inputted value."""
        try:
            max_price = float(self.entry.get())
            # Handle edge cases
            if max_price < 0:
                raise ValueError("Maximum price cannot be negative")
            self.price = max_price
            self.root.destroy()
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid maximum price (in USD)")
