"""
CSC111 Winter 2023 Project: Steam Game Recommender

This module is the main module used to run the program.

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mikhael Orteza, Muaj Ahmed, Cheng Peng, and Ari Casas Nassar
"""

import game_graph


# To change the number of games recommended, please look at changing the num_games_recommended variable under
# the runner function in game_graph.py

def run() -> None:
    """Run the program."""
    game_file = 'datasets/games.csv'
    game_metadata_file = 'datasets/games_metadata.json'
    game_graph.runner(game_file, game_metadata_file)


if __name__ == '__main__':
    run()
