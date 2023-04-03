"""
CSC111 Winter 2023 Project: Steam Game Recommender

This module consists of the tkinter classes which are used to create an interface that the user can interact
with to find recommended games for them.

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mikhael Orteza, Muaj Ahmed, Cheng Peng, and Ari Casas Nassar
"""
import tkinter as tk
import webbrowser
from tkinter import messagebox
from tkinter import ttk


class GameIDSelector:
    """Allows the user to input game IDs.

    Instance Attributes:
    - root: the root window that displays the user interface
    - games: a list of all the games and their associated id
    - game_ids: all the valid game ids that the user can input
    - game_id_label: a label that suggests the user to input ids
    - game_id_label: a label on top of the list box of game ids and their game names
    - add_button: a button that allows the user to add more games to base recommendations on
    - done_button: a button that allows the user to complete the game selection
    """

    def __init__(self, games, valid_ids: list[int]) -> None:
        self.root = tk.Tk()
        self.games = games
        self.game_ids = []
        self.valid_ids = valid_ids

        self.root.title("Steam Game Recommender")
        self.root.geometry("1920x1080")

        # Create a label for the intro text
        intro_text = tk.Label(self.root,
                              text="Welcome to the Steam Game Recommender!\nThis program will recommend"
                                   " steam games"
                                   " you should play based on games you've played in the past and your preference of "
                                   "genre.\nPlease input the game ids of steam games you have played before (optional)",
                              font=("Arial", 12), wraplength=400)
        intro_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Create a label and entry for entering game IDs
        self.game_id_label = tk.Label(self.root, text="Enter a game ID:", font=("Arial", 12))
        self.game_id_label.grid(row=1, column=0, padx=10, pady=10)

        self.game_id_entry = tk.Entry(self.root, font=("Arial", 12))
        self.game_id_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create a label for the game ID listbox
        self.game_id_listbox_label = tk.Label(self.root, text="Valid Games in Alphabetical Order (with their id)",
                                              font=("Arial", 12))
        self.game_id_listbox_label.grid(row=2, column=0, padx=10, pady=10)

        # Create a scrollbar for the game ID listbox
        self.game_id_scrollbar = tk.Scrollbar(self.root)
        self.game_id_scrollbar.grid(row=3, column=1, sticky="NS")

        # Create a listbox for showing valid game IDs
        self.game_id_listbox = tk.Listbox(self.root, height=10, width=50, font=("Arial", 12))
        self.game_id_listbox.grid(row=3, column=0, padx=10, pady=10)

        # Link the scrollbar to the game ID listbox
        self.game_id_listbox.config(yscrollcommand=self.game_id_scrollbar.set)
        self.game_id_scrollbar.config(command=self.game_id_listbox.yview)

        # Add valid game IDs and their names to the listbox
        game_name_id_list = []
        for game_id in self.valid_ids:
            if game_id in self.games:
                game_name_id_list.append((self.games[game_id].name, game_id))
        game_name_id_list.sort(key=lambda x: x[0])  # sort by game name

        for game_name, game_id in game_name_id_list:
            self.game_id_listbox.insert(tk.END, f"{game_name}: {game_id}")

        # Create "Add" and "Done" buttons
        self.add_button = tk.Button(self.root, text="Add", command=self.add_game_id, font=("Arial", 12), bg="#4CAF50",
                                    fg="white")
        self.add_button.grid(row=1, column=2, padx=10, pady=10)

        self.done_button = tk.Button(self.root, text="Done", command=self.submit, font=("Arial", 12), bg="#008CBA",
                                     fg="white")
        self.done_button.grid(row=1, column=3, columnspan=2, padx=10, pady=10)

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
        self.root.destroy()

    def get_game_ids(self) -> list[int]:
        """Returns the list of game IDs."""
        return self.game_ids


class GenreSelector:
    """Allows the user to select genres they are interested in.

    Instance Attributes:
    - root: the root window that is displayed in the user interface
    - genres: list of all inputted genres
    - check_frame: a frame to hold the checkboxes
    - For any genre, genre_checkbox refers to the checkbox that the user has to click for that genre in order for it
    to be considered in the recommendation. Furthermore, genre_var depicts if the user picked a certain genre or not.
    """

    def __init__(self) -> None:
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

    def submit(self) -> None:
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
    """Asks the user to input the maximum amoount of money they are willing to spend on a steam game.

    Instance Attributes:
    - price: the maximum price that a user is willing to pay for a game.
    - label: a label that suggests the user to pick their price budget for a game.
    - entry: allows the user to enter text
    - button: allows the user to submit their entered text

    """

    def __init__(self) -> None:
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

    def submit(self) -> None:
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


class GameRecommendations:
    """Displays the top recommended games to the user.

    Instance Attributes:
    - top_games: the top games that will be recommended to the user.
    - root: the root window that is displayed on the user interface.
    - label: tells the user about the recommended games that have been displayed with their steam links.

    """

    def __init__(self, top_games: list) -> None:
        self.top_games = top_games
        self.root = tk.Tk()
        self.root.title("Steam Game Recommender")
        self.root.geometry("1920x1080")

        self.display_games()

        self.root.mainloop()

    def display_games(self) -> None:
        """Displays the recommended games to the user."""
        # Creates a label to explain the output
        self.label = tk.Label(self.root, text="Find below the recommended games with their clickable steam links.",
                              font=("Arial", 12))
        self.label.grid(row=0, column=0, pady=10)

        # Create a frame to hold the listbox and scrollbar
        frame = tk.Frame(self.root)
        frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Create a listbox widget inside the frame
        listbox = tk.Listbox(frame, font=("Arial", 12), height=20, width=100)
        listbox.grid(row=0, column=0, sticky="nsew")

        # Create a scrollbar widget and link it to the listbox
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.grid(row=0, column=1, sticky="ns")
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        # Insert game information into the listbox
        for idx, game in enumerate(self.top_games):
            label_text = f"{idx + 1}. {game.name}"
            link_text = f"https://store.steampowered.com/app/{game.game_id}"
            listbox.insert(tk.END, label_text)
            listbox.insert(tk.END, link_text)
            listbox.insert(tk.END, "")  # Add a blank line between games

        # Bind a function to the <Button-1> event of the listbox
        listbox.bind("<Button-1>", self.open_link)

        # Create a button to quit the application
        quit_button = tk.ttk.Button(self.root, text="Quit", command=self.root.destroy)
        quit_button.grid(row=2, column=0, pady=10)

    def open_link(self, event) -> None:
        """Opens the link associated with the clicked game."""
        widget = event.widget
        index = widget.nearest(event.y)
        link = widget.get(index)
        webbrowser.open_new_tab(link)  # Open the link in the default web browser


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'ttk', 'webbrowser'],
        'allowed-io': [],
        'max-line-length': 120,
        'disable': ['forbidden-IO-function', 'W0611', 'R0902', 'E9972', 'E9970']
    })
