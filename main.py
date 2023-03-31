import game_graph_csv


def run() -> None:
    """Run the program."""
    game_file = 'datasets/games.csv'
    game_metadata_file = 'datasets/games_metadata.json'
    game_graph_csv.runner(game_file, game_metadata_file)


if __name__ == '__main__':
    run()
