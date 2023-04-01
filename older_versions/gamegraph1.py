"""Code for the game graph"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable
import csv
import json


@dataclass
class Game:
    """A steam game and its various attributes
    Instance Attributes:
    - name:
        The name of the game.
    - game_id:
        The id of the game.
    - date_release:
        The date for when the game was released.
    - operating_systems:
        A dictionary consisting of a mapping between various operating systems and the game's
        compatibility with them.(str : bool)
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
    date_release: str  # swap it to str, make it easier to load
    operating_systems: dict[str, bool]
    price: float
    positive_ratio: int
    rating: Optional[float]  # meta-score

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

    def top_similar_games(self, total: int) -> list[Game]:
        """Returns a list of at most 'total' length containing the most similar games of genre to self.game
        Preconditions:
        - total >= 0
        """
        return self._helper_top_similar_games(total, set())

    def _helper_top_similar_games(self, total: int, visited_so_far: set[Game]) -> list[Game]:
        """Returns a list of at most 'total' length containing the most similar games of genre to self.game
        Doesn't visit any games included in 'visited_so_far'
        Preconditions:
        - total >= 0
        """
        if total > len(self.neighbours):
            total = len(self.neighbours)
        if total == 0:
            return []
        else:
            list_so_far = []
            max_genres_so_far = 0
            most_similar_game = None
            for neighbour in self.neighbours:
                total_genres = self.game.genre_count(neighbour.game.genres)
                if neighbour.game not in visited_so_far and total_genres > max_genres_so_far:
                    most_similar_game = neighbour.game
            list_so_far.append(most_similar_game)
            visited_so_far.add(most_similar_game)
            return list_so_far + self._helper_top_similar_games(total - 1, visited_so_far)


class GameGraph:
    """A graph containing nodes that represent a game. Nodes are connected depending on the number of genres that they
    have in common with another game and the user's preferred genres.
    Instance Attributes:
    - min_genres_game:
        The minimum number of genres that a game in the graph must have in common with the user's preferred genres.
    - min_genres_edge:
        The minimum number of genres that two nodes must have in order for an edge to be formed between them.
    - user_genres:
        A set containing the user's preferred genres.
    NOTE:
    - the min_genres_game and min_genres_edge were added in order to create a purpose of the graph data structure.
    Otherwise, we are solely using the nodes for their scores, which does not take advantage of the edges formed between
    nodes. Thus, the min_genres_game and min_genres_edge can be used as a way of filtering
    Private Instance Attibutes:
    - _nodes:
        A mapping from game ids to GameNode objects in the GameGraph.
    Representation Invariants:
    - all(self._nodes[game_id].game_id = game_id for game_id in self_nodes)
    - self_total >= 0
    - min_genres_game >= 0
    - min_genres_edge >= 0
    """
    min_genres_game: int
    min_genres_edge: int
    user_genres: list[str]
    _nodes: dict[int, GameNode]

    def __init__(self, min_genres_game: int, min_genres_edge: int, user_genres: list[str]) -> None:
        """Initializes the game graph"""
        self._nodes = {}
        self.min_genres_game = min_genres_game
        self.min_genres_edge = min_genres_edge
        self.user_genres = user_genres

    def add_game(self, game: Game) -> None:
        """Adds a game node into the graph if they have the minimum amount of intersecting genres with the
        user (i.e. self.min_genres_game)"""
        game_count = game.genre_count(self.user_genres)
        game_id = game.game_id
        if game_count >= self.min_genres_game:
            self._nodes[game_id] = GameNode(game)

    def add_edge(self, game1: GameNode, game2: GameNode) -> None:
        """Creates an edge between two game nodes if they have the minimum amount of intersecting genres
        Preconditions:
        - game1 in self._nodes and game2 in self._nodes
        """
        similar_games = game1.game.genre_count(game2.game.genres)
        if similar_games >= self.min_genres_edge:
            game1.neighbours.append(game2)
            game2.neighbours.append(game1)

    def top_games(self, total: int, recorded_games: set[Game]) -> list[Game]:
        """Returns a list of the top recommended games depending on the inputted parameter
        Preconditions:
        - total >= 0
        """
        if total == 0:
            return []
        else:
            list_so_far = []
            max_game = None
            max_score_so_far = 0
            for game in self._nodes:
                node = self._nodes[game]
                if node.game not in recorded_games and node.game.rating > max_score_so_far:
                    max_game = node.game
                    max_score_so_far = node.game.rating
            recorded_games.add(max_game)
            list_so_far.append(max_game)
            rec_result = self.top_games(total - 1, recorded_games)
            return list_so_far + rec_result

    def node_list(self) -> list[GameNode]:
        """Returns a list of all the game nodes in self"""
        list_so_far = []
        for game_id in self._nodes:
            list_so_far.append(self._nodes[game_id])
        return list_so_far


def read_data_csv(csv_file: str) -> dict[int, Game]:
    """Load data from a CSV file and output the data as a mapping between game ids and their corresponding Game object.
    Preconditions:
        - csv_file refers to a valid CSV file
    """
    result = {}

    with open(csv_file) as f:
        reader = csv.reader(f)

        next(reader)  # skip headers

        for row in reader:
            game_id = int(row[0])
            name = row[1]
            date_release = row[2]
            genres = []
            operating_systems = {'win': bool(row[3]),
                                 'mac': bool(row[4]),
                                 'linux': bool(row[5])}
            # 6 is skipped for rating(all words)
            positive_ratio = int(row[7])
            # 8 is skipped for user_reviews
            price_final = float(row[9])
            # Last 3 are price_original,discount,steam_deck, they are skipped
            curr_game = Game(name, game_id, genres, date_release, operating_systems, price_final, positive_ratio, None)
            result[game_id] = curr_game
    return result


def read_metadata_json(json_file: str) -> list[tuple]:
    """Load data from a JSON file and output the data as a list of tuples. The tuple contains the game_id(index 0, int)
    and the tags(index 1, list[str]).
    Preconditions:
        - json_file refers to a valid JSON file
    """
    result = []

    with open(json_file) as f:
        for line in [str.strip(line.lower()) for line in f]:
            curr_full_metadata = json.loads(line)
            relevant_metadata = (int(curr_full_metadata.get('app_id')), curr_full_metadata.get('tags'))
            result.append(relevant_metadata)

    return result


def generate_graph(game_file: str, json_file: str, genres: list, genre_edge: int, min_genre: int) -> GameGraph:
    """Creates a game graph
    Notes:
    -game_file refers to a csv file consisting of games and their attributes.
    -json_file is a json file that consists of the every game's genre in.
    -min_genre refers to the min_genre_game attribute in the game graph.
    -genre_edge refers to the min_genres_edge attribute in the game graph
    """
    json_result = read_metadata_json(json_file)
    csv_result = read_data_csv(game_file)
    game_graph = GameGraph(min_genre, genre_edge, genres)
    for metadata in json_result:
        # Adds the nodes to the graph
        game = csv_result[metadata[0]]
        game.genres = metadata[1]
        game_graph.add_game(game)
    node_list = game_graph.node_list()
    # Creates edges between each node if applicable.
    for node1 in node_list:
        for node2 in node_list:
            if node1 != node2:
                game_graph.add_edge(node1, node2)
    return game_graph


def sort_games(games: list[Game]) -> None:
    """Sorts a list of games in the given list in descending order of their rating by mutating the list.
    Note:
    - This sorting function uses the iterative insert method.
    """
    for index1 in range(0, len(games) - 1):  # len(games) - 1 to prevent index out of bounds error
        if games[index1].rating < games[index1 + 1].rating:
            games[index1], games[index1 + 1] = games[index1 + 1], games[index1]
            for index2 in range(index1, 0, -1):
                if games[index2].rating > games[index2 - 1].rating:
                    games[index2], games[index2 - 1] = games[index2 - 1], games[index2]


def graph_list(genres: list, total_min_genre: int, total_min_edge: int, csv_file: str, json_file: str) \
        -> list[GameGraph]:
    """Creates a list of game graphs that vary in the amount commonly shared genres that the graph games
    have with the user.
    Notes:
        -genres is a list of game genres that the user likes.
        -total_min_genre refers to the range of values min_genre values hat a game graph could have.
        This range is from 0 (inclusive) to total_min_genre (non-inclusive).
        -total_min_edge refers to the range of
    Preconditions:
    - total >= 1
    """
    game_graphs = []
    for min_genre in range(0, total_min_genre):
        for min_edge in range(0, total_min_edge):
            game_graph = generate_graph(csv_file, json_file, genres, min_edge, min_genre)
            game_graphs.append(game_graph)
    return game_graphs


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

    # Part 3: Calculate meta score

    # Part 4: Give recommendations(top 5 only)
