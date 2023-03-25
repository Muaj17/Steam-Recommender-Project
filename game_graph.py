"""Code for the game graph"""
from __future__ import annotations


class Game:
    """A steam game and its various attributes

    Instance Attributes:
    - name:
        The name of the game.
    - date_release:
        The date for when the game was released.
    - operating_systems:
        A dictionary consisting of a mapping between various operating systems and the game's
        compatibility with them.
    - price:
        the price of the game.
    - rating:
        The metascore of the game, which is dependent on the relationship between the game's attributes and the
        user's preferences.
    """
    name: str
    genres: set
    date_release: tuple
    operating_systems: dict
    price: float
    rating: float

    def __init__(self, name: str, date: tuple, operating_system: dict, genres: set,
                 price: float, rating: float) -> None:
        """Initializes the game instance"""
        self.name = name
        self.genres = genres
        self.date_release = date
        self.operating_systems = operating_system
        self.price = price
        self.rating = rating

    def genre_count(self, user_genres: set) -> int:
        """Counts the number of user preferenced genres and the game genres that are similar"""
        return len(self.genre_list(user_genres))

    def same_num_game(self, other_game: Game, total_needed: int) -> bool:
        """Compares self to another game and determines if they have a certain number of games, depending on what is
        inputted into the total_needed paramter
        """
        other_game_genres = other_game.genres
        return self.genre_count(other_game_genres) >= total_needed

    def genre_list(self, genre_collection: set) -> set:
        """Returns a list of all the similar genres between self and the given genre collection"""
        new_set = self.genres.intersection(genre_collection)
        return new_set


class GameNode:
    """A node in a game graph"""
    game: Game
    neighbours: list[GameNode]

    def __init__(self, game: Game) -> None:
        """Intializes the game node"""
        self.game = game
        self.neighbours = []


class GameGraph:
    """A graph containing nodes that represent a game. Nodes are connected depending on the number of genres that they
    have in common with another game.

    Instance Attributes:
    - game_total:
        The minimum number of genres that two connected nodes have in common.

    Representation Invariants:
    - all(self._nodes[name].name = name for name in self_nodes)
    - self_total >= 0
    """
    game_total: int
    user_genres: set
    _nodes: dict[str, GameNode]

    def __init__(self, genres: int) -> None:
        """Initializes the game graph"""
        self._nodes = {}
        self.game_total = genres

    def add_game(self, node: GameNode) -> None:
        """Adds a game node into the graph if it contains a certain amount of games of the user's preference"""
        game_count = node.game.genre_count(self.user_genres)
        game_name = node.game.name
        if game_count >= self.game_total:
            self._nodes[game_name] = node

    def add_edge(self, game1: str, game2: str) -> None:
        """Creates an edge between two games

        Preconditions:
        - game1 in self._nodes and game2 in self._nodes
        """
        node1, node2 = self._nodes[game1], self._nodes[game2]
        similar_games = node1.game.genre_count(node2.game.genres)
        if similar_games != 0:
            node1.neighbours.append(node2)
            node2.neighbours.append(node1)
