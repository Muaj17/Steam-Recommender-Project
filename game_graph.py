"""Code for the game graph"""
from __future__ import annotations
from typing import Optional
from genreselector import GenreSelector
import tkinter as tk
import csv
import json


class Game:
    """A steam game and its various attributes
    Instance Attributes:
    - name:
        The name of the game.
    - game_id:
        The id of the game.
    - date_release:
        The date for when the game was released.
    - price:
        the price of the game, in US dollars.
    - positive_ratio:
        An official ratio for the game. It is used in part of our metascore calculation.
    - rating:
        The metascore of the game, which is dependent on the relationship between the game's attributes and the
        user's preferences.
    """
    name: str
    game_id: int  # added
    genres: list[str]
    price: float
    positive_ratio: int
    rating: Optional[float]  # meta-score

    def __init__(self, name: str, game_id: int, genres: list[str], price: float, positive_ratio: int,
                 rating: float) -> None:
        """Initializes the game instance"""
        self.name = name
        self.game_id = game_id
        self.genres = genres
        self.price = price
        self.positive_ratio = positive_ratio
        self.rating = rating

    def genre_count(self, user_genres: list[str]) -> int:
        """Counts the number of user preferenced genres and the game genres that are similar"""
        return len(self.genre_list(user_genres))

    def same_num_game(self, other_game: Game, total_needed: int) -> bool:
        """Compares self to another game and determines if they have a certain number of games, depending on what is
        inputted into the total_needed paramter
        Preconditions:
        - total_needed >= 0
        """
        other_game_genres = other_game.genres
        return self.genre_count(other_game_genres) >= total_needed

    def genre_list(self, genre_collection: list[str]) -> list[str]:
        """Returns a list of all the similar genres between self and the given genre collection"""
        list_so_far = []
        for genre in self.genres:
            if genre in genre_collection:
                list_so_far.append(genre)
        return list_so_far


class GameNode:
    """A node in a game graph"""
    game: Game
    neighbours: list[GameNode]

    def __init__(self, game: Game) -> None:
        """Intializes the game node"""
        self.game = game
        self.neighbours = []

    def top_similar_games(self) -> list[GameNode]:
        """Returns a sorted list of all the node's neighbour's game score in descending order.
        """
        games = self.neighbours.copy()
        if len(games) != 0:
            for index1 in range(0, len(games) - 1):
                if games[index1].game.rating < games[index1 + 1].game.rating:
                    games[index1], games[index1 + 1] = games[index1 + 1], games[index1]
                    for index2 in range(index1, 0, -1):
                        if games[index2].game.rating > games[index2 - 1].game.rating:
                            games[index2], games[index2 - 1] = games[index2 - 1], games[index2]
        return games


class GameGraph:
    """A graph containing nodes that represent a game. Nodes are connected depending on the number of genres that they
    have in common with another game and the user's preferred genres.
    Instance Attributes:
    - self.user_games is a list of all the games that the user has played/or wants recommendations to be based on.

    Representation Invariants:
    - all(self._nodes[game_id].game_id = game_id for game_id in self._nodes)
    - self.min_edge_genre >= 0
    """
    # Private Instance Attibutes:
    # - _nodes: A mapping from game ids to GameNode objects in the GameGraph.

    min_edge_genre: int
    user_games: list[str]
    _nodes: dict[int, GameNode]
    _user_nodes: dict[int, GameNode]

    def __init__(self, user_games: list[str], min_edge_genre: int) -> None:
        """Initializes the game graph"""
        self._nodes = {}
        self.user_games = user_games
        self.min_edge_genre = min_edge_genre

    def add_game(self, game: Game) -> None:
        """Adds a game node into the graph"""
        game_id = game.game_id
        game_node = GameNode(game)
        self._nodes[game_id] = game_node
        if game.name.lower() in self.user_games:
            self._user_nodes[game_id] = game_node

    def add_all_edges(self) -> None:
        """Creates all the edge that need to be made in the graph"""
        for user_id in self._user_nodes:
            for other_id in self._nodes:
                user_node = self._user_nodes[user_id]
                other_node = self._user_nodes[other_id]
                if user_node != other_node:
                    self.add_edge(other_node, user_node)

    def add_edge(self, game1: GameNode, user_node: GameNode) -> None:
        """Creates an edge between two game nodes if they have the minimum amount of intersecting genres
        Preconditions:
        - game1 in self._nodes and user_game in self._nodes
        - user_game.game.name in [game.lower for game in self.user_games]
        """
        similar_games = game1.game.genre_count(user_node.game.genres)
        if similar_games >= self.min_edge_genre:
            game1.neighbours.append(user_node)
            user_node.neighbours.append(game1)

    def top_games(self, total: int) -> list[Game]:
        """Returns a list of the top recommended games depending on the inputted parameter. The returned list of games
        are in descending order in terms of their score.
        Preconditions:
        - total >= 0
        """
        possible_suggestions = []
        for user_id in self._user_nodes:
            neighbour_game_list = []
            for neighbour in self._nodes[user_id].neighbours:
                neighbour_game_list.append(neighbour.game)
            possible_suggestions.extend(neighbour_game_list)
        sort_games(possible_suggestions)
        top_games = []
        index_so_far = 0
        while index_so_far == total - 1 or index_so_far == len(possible_suggestions) - 1:
            top_games.append(possible_suggestions[index_so_far])
            index_so_far += 1
        return top_games

    def all_user_node_neighbours(self, node: GameNode) -> list[GameNode]:
        """Returns a list of all node's neighbours that are also in self._user_nodes"""
        list_so_far = []
        for neighbour in node.neighbours:
            if neighbour in self._user_nodes:
                list_so_far.append(neighbour)
        return list_so_far

    def max_price(self) -> float:
        """Returns the highest price out of all the games in self"""
        max_so_far = 0.0
        for id in self._nodes:
            node = self._nodes[id]
            if node.game.price > max_so_far:
                max_so_far = node.game.price
        return max_so_far

    def max_rating(self) -> int:
        """Returns the highest rating out of all the games in self"""
        max_so_far = 0
        for id in self._nodes:
            node = self._nodes[id]
            if node.game.rating > max_so_far:
                max_so_far = node.game.rating
        return max_so_far

    def compute_score(self, game_node: GameNode) -> None:
        """Computes the game recommendation score for the given game and mutates the game's metascore for the
        given game node.

        Preconditions:
        - game_node in self._nodes
        """
        rating_price_weight = 0.7
        neighbour_weight = 0.3
        assert rating_price_weight + neighbour_weight == 1.0
        game = game_node.game
        max_price = self.max_price()
        max_rating = self.max_rating()
        rating_price_score = (game.rating / max_rating) * ((max_price - game.price) / max_price)
        user_game_neighbours = self.all_user_node_neighbours(game_node)
        neighbour_score = (len(user_game_neighbours) / len(self._user_nodes))
        game.score = rating_price_score * rating_price_weight + neighbour_score * neighbour_weight


def read_data_csv(csv_file: str) -> dict[int, Game]:
    """Load data from a CSV file and output the data as a mapping between game ids and their corresponding Game object.
    Preconditions:
        - csv_file refers to a valid CSV file
    """
    result = {}

    with open(csv_file, encoding='utf-8') as f:
        reader = csv.reader(f)

        next(reader)  # skip headers

        for row in reader:
            game_id = int(row[0])
            name = row[1]
            genres = []
            operating_systems = {'win': bool(row[3]),
                                 'mac': bool(row[4]),
                                 'linux': bool(row[5])}
            # 6 is skipped for rating(all words)
            positive_ratio = int(row[7])
            # 8 is skipped for user_reviews
            price_final = float(row[9])
            # Last 3 are price_original,discount,steam_deck, they are skipped
            curr_game = Game(name, game_id, genres, operating_systems, price_final, positive_ratio, 0.0)
            result[game_id] = curr_game
    return result


def read_metadata_json(json_file: str) -> list[tuple]:
    """Load data from a JSON file and output the data as a list of tuples. The tuple contains the game_id(index 0, int)
    and the tags(index 1, list[str]).
    Preconditions:
        - json_file refers to a valid JSON file
    """
    result = []

    with open(json_file, encoding='utf-8') as f:
        for line in [str.strip(line.lower()) for line in f]:
            curr_full_metadata = json.loads(line)
            relevant_metadata = (int(curr_full_metadata.get('app_id')), curr_full_metadata.get('tags'))
            result.append(relevant_metadata)

    return result


def generate_graph(game_file: str, json_file: str, user_games: list, genre_edge: int) -> GameGraph:
    """Creates a game graph
    Notes:
    -game_file refers to a csv file consisting of games and their attributes.
    -json_file is a json file that consists of the every game's genre in.
    -user_games refers to a list of games that the user has inputted.

    """
    json_result = read_metadata_json(json_file)
    csv_result = read_data_csv(game_file)
    game_graph = GameGraph(user_games, genre_edge)
    for metadata in json_result:
        # Adds the nodes to the graph
        game = csv_result[metadata[0]]
        game.genres = metadata[1]
        game_graph.add_game(game)
    # Creates edges between each node if applicable.
    game_graph.add_all_edges()
    return game_graph


def sort_games(games: list[Game]) -> None:
    """Sorts a list of games in the given list in descending order of their rating by mutating the list.
    """
    for index1 in range(0, len(games) - 1):
        if games[index1].rating < games[index1 + 1].rating:
            games[index1], games[index1 + 1] = games[index1 + 1], games[index1]
            for index2 in range(index1, 0, -1):
                if games[index2].rating > games[index2 - 1].rating:
                    games[index2], games[index2 - 1] = games[index2 - 1], games[index2]


def graph_list(user_games: list, total_min_edge: int, csv_file: str, json_file: str) -> dict[GameGraph, int]:
    """Creates a dictionary of game graphs and their corresponding minimum genre edge requirement.

    Notes:
        -genres is a list of game genres that the user likes.
        -total_min_edge refers to a range of values from 0 (inclusive) to total_min_edge - 1. Each integer in the range
        will be the minimum genre edge requirement for a graph added into the game graph list.
    Preconditions:
    - total >= 1
    """
    game_graphs = {}
    for min_edge in range(0, total_min_edge):
        game_graph = generate_graph(csv_file, json_file, user_games, min_edge)
        game_graphs[game_graph] = min_edge
    return game_graphs


def highest_scoring_games(graph_list: list[GameGraph], total_games: int) -> list[Game]:
    """Creates a list of the top scored games that will be recommended to the user. The total games recommended
    is based on the vaue of total_games.

    Preconditions:
    - total_games > 0
    """
    list_so_far = []
    # NEEDS TO BE IMPLEMENTED
    return list_so_far


def runner(game_file: str, game_metadata_file: str) -> None:
    """Run a simulation based on the data from the given csv file."""
    # Part 1: Read datasets
    games = read_data_csv(game_file)
    games_metadata = read_metadata_json(game_metadata_file)

    for metadata in games_metadata:
        game_id, genres = metadata

        if game_id in games:
            games[game_id].genres = genres

    # Part 2: Tkinter interface(ask for preferred genres)
    # Create a new tkinter window
    root = tk.Tk()
    root.title("Genre Selector")
    root.geometry("400x300")

    # Information for user
    intro_text = tk.Label(root,
                          text="Welcome to the Steam Game Recommender!\nThis program will recommend the top 5 games "
                               "you should play based on your preference of genre.\nPlease select the genres you're "
                               "interested in"
                               "below.", font=("Arial", 14))
    intro_text.grid(pady=20)

    # Call the GenreSelector class within the tkinter window
    selector = GenreSelector(root)

    # Run the tkinter mainloop
    root.mainloop()

    # Get selected genres from genre selector
    selected_genres = selector.genres

    # Part 3: Calculate meta score

    # Part 4: Give recommendations(top 5 only)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['genreselector', 'tkinter', 'csv', 'json'],
    })
