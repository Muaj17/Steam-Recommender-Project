"""
Group Project for CSC111 made by Mikhael Orteza, Muaj Ahmed, Cheng Peng, and Ari Casas Nassar

The program consists of the game graph class and all its associated functions with regards to loading in the data from
a given dataset, the computations for scoring each game, and the provision of the top recommended games based on the
user's inputs of games that they played and genres that they like.
"""
from __future__ import annotations
from typing import Optional
import csv
import json
import user_interface


class Game:
    """A steam game and its various attributes
    Instance Attributes:
    - name:
        The name of the game.
    - game_id:
        The id of the game.
    - genres:
        All the genres that the game has.
    - price:
        the price of the game, in US dollars.
    - positive_ratio:
        An official ratio for the game. It is used in part of our metascore calculation.
    - rating:
        The metascore of the game, which is dependent on the relationship between the game's attributes and the
        user's preferences.
    Representation Invariants:
    - self.name != ''
    - self.price >= 0.0
    - self.genres != []
    - 0 <= self.positive_ratio and self.positive_ratio <= 100
    - 0.0 <= self.rating and self.rating <= 1.0
    """
    name: str
    game_id: int
    genres: list[str]
    price: float
    positive_ratio: int
    rating: Optional[float]

    def __init__(self, game_info: tuple[int, str], genres: list[str], price: float, positive_ratio: int) -> None:
        """Initializes the game instance"""
        self.name = game_info[1]
        self.game_id = game_info[0]
        self.genres = genres
        self.price = price
        self.positive_ratio = positive_ratio

    def genre_count(self, genre_collection: list[str]) -> int:
        """Counts the number of user preferenced genres and the game genres that are similar"""
        lowered_list = [genre_str.lower() for genre_str in genre_collection]
        list_so_far = []
        for genre in self.genres:
            if genre.lower() in lowered_list:
                list_so_far.append(genre)
        return len(list_so_far)


class GameNode:
    """A node in a game graph
    Instance Attributes:
    - game:
        The game that the node refers to.
    - neighbours:
        All the game nodes that self shares a genre with. At least one node in the edge pair is a game that the user
        has played.
    Representation Invariants:
    - all(self in neighbour.neighbours for neighbour in self.neighbours)
    """
    game: Game
    neighbours: list[GameNode]

    def __init__(self, game: Game) -> None:
        """Intializes the game node"""
        self.game = game
        self.neighbours = []


class GameGraph:
    """A graph containing nodes that represent a game. Nodes are connected depending on the number of genres that they
    have in common with another game and the user's preferred genres.

    Instance Attributes:
    - self.user_games is a list of all the games that the user has played/or wants recommendations to be based on.
    - user_max_price is the maximum price that the user is willing to pay for a game.

    Representation Invariants:
    - all(self._nodes[game_id].game_id = game_id for game_id in self._nodes)
    - self.user_max_price >= 0.0
    - all(game_id in self._nodes for game_id in self._user_nodes)
    """
    # Private Instance Attibutes:
    # - _nodes: A mapping from game ids to GameNode objects in the GameGraph.
    # - _user_nodes: Similar to _nodes, but only consists of nodes whose game has been played by the user.

    user_game_ids: list[int]
    user_game_genres: list[str]
    user_max_price: float
    _nodes: dict[int, GameNode]
    _user_nodes: dict[int, GameNode]

    def __init__(self, user_game_ids: list[int], user_game_genres: list[str], user_max_price: float) -> None:
        """Initializes the game graph"""
        self._nodes = {}
        self._user_nodes = {}
        self.user_game_ids = user_game_ids
        self.user_game_genres = user_game_genres
        self.user_max_price = user_max_price

    def add_game(self, game: Game) -> None:
        """Adds a game node into the graph"""
        game_id = game.game_id
        game_node = GameNode(game)
        self._nodes[game_id] = game_node
        if game.game_id in self.user_game_ids:
            self._user_nodes[game_id] = game_node

    def add_all_edges(self) -> None:
        """Creates all the edge that need to be made in the graph. Edges are only formed between game nodes whose
        game is a game that the user has played and any other game node.
        """
        for user_id in self._user_nodes:
            for other_id in self._nodes:
                user_node = self._user_nodes[user_id]
                other_node = self._nodes[other_id]
                if user_node != other_node:
                    self.add_edge(other_node, user_node)

    def add_edge(self, game1: GameNode, user_node: GameNode) -> None:
        """Creates an edge between two game nodes.
        Preconditions:
        - game1 in self._nodes and user_node in self._nodes
        - user_node in [self._nodes[user_id] for user_id in self.user_game_ids]
        """
        game1.neighbours.append(user_node)
        user_node.neighbours.append(game1)

    def max_price(self) -> float:
        """Returns the highest price out of all the games in self"""
        max_so_far = 0.0
        for game_id in self._nodes:
            node = self._nodes[game_id]
            if node.game.price > max_so_far:
                max_so_far = node.game.price
        return max_so_far

    def max_positive_ratio(self) -> int:
        """Returns the highest rating out of all the games in self"""
        max_so_far = 0
        for game_id in self._nodes:
            node = self._nodes[game_id]
            if node.game.positive_ratio > max_so_far:
                max_so_far = node.game.positive_ratio
        return max_so_far

    def user_genres(self) -> list[str]:
        """Returns the amount of genres that the user has played based on their inputted games"""
        list_so_far = []
        for game_id in self._user_nodes:
            node = self._user_nodes[game_id]
            for genre in node.game.genres:
                if genre not in list_so_far:
                    list_so_far.append(genre)
        return list_so_far

    def assign_all_scores(self) -> None:
        """Computes and assigns all the scores for each node's associated game."""
        for game_id in self._nodes:
            self.compute_score(self._nodes[game_id])

    def compute_score(self, game_node: GameNode) -> None:
        """Computes and assigns the score of each node's associated game. The type of score computation algorithm is
        dependent on whether the user has inputted a list of games to base the recommendations on.
        """
        if self.user_game_ids == []:
            self.compute_score_genre(game_node)
        else:
            self.compute_score_game(game_node)

    def compute_score_game(self, game_node: GameNode) -> None:
        """Computes the game recommendation score for the given game and mutates the game's metascore for the
        given game node. This function is specifically used for computing the score of game nodes when the user has
        inputted games to make recommendations from.

        Preconditions:
        - game_node in {self._nodes[game_id] for game_id in self._nodes}
        - self.user_game_ids != []
        """
        # Weights of various factors on the game and how it will influence the score.
        rate_price_weight = 0.6
        neighbour_weight = 0.3
        genre_weight = 0.1

        user_genres = self.user_genres()
        game = game_node.game
        max_price = self.max_price()
        max_ratio = self.max_positive_ratio()

        if max_price in {game.price, 0.0}:
            rate_price = (game.positive_ratio / max_ratio)
        else:
            rate_price = (game.positive_ratio / max_ratio) * ((max_price - game.price) / max_price) * rate_price_weight

        neighbour_score = (len(game_node.neighbours) / len(self._user_nodes)) * neighbour_weight
        genre_score = (game.genre_count(user_genres) / len(user_genres)) * genre_weight

        if game.price > self.user_max_price or game.genre_count(self.user_game_genres) != len(self._user_nodes):
            # The game is too expensive for the user so there is not a point of recommending the game to them.
            # Also, the game does not satisfy all the genre requirements that the user wants in recommended game.
            game.rating = 0.0
        else:
            game.rating = rate_price + neighbour_score + genre_score

    def compute_score_genre(self, game_node: GameNode) -> None:
        """Computes the scores of each node if the user has not inputted any games to base recommendations on.

        Preconditions:
        - game_node in {self._nodes[game_id] for game_id in self._nodes}
        - self.user_game_ids == []
        """
        genre_weight = 0.4
        rate_price_weight = 0.6

        max_price = self.max_price()
        max_ratio = self.max_positive_ratio()
        game = game_node.game
        genre_score = 0.0

        if len(self.user_game_genres) != []:
            # Prevents division by zero
            genre_score = (game.genre_count(self.user_game_genres) / len(self.user_game_genres)) * genre_weight

        if max_price in {game.price, 0.0}:
            rate_price = (game.positive_ratio / max_ratio)
        else:
            rate_price = (game.positive_ratio / max_ratio) * ((max_price - game.price) / max_price) * rate_price_weight

        if game.price > self.user_max_price:
            game.rating = 0.0
        else:
            game.rating = genre_score + rate_price

    def top_games(self, total: int) -> list[Game]:
        """Returns a list of the top recommended games depending on the inputted parameter. The returned list of games
        are in descending order in terms of their score. This function will be used to compute the top games when
        the user has not inputted any games.

        Preconditions:
        - total >= 0
        - self.user_game_ids == []
        """
        # Set is used for constant time operations in terms of adding and removing elements.
        possible_suggestions = set()

        for game_id in self._nodes:
            possible_suggestions.add(self._nodes[game_id].game)
        actual_suggestions = []

        while len(actual_suggestions) != total or len(possible_suggestions) == 0:
            game = highest_scoring_game(possible_suggestions)
            possible_suggestions.remove(game)
            actual_suggestions.append(game)
        sort_games(actual_suggestions)
        return actual_suggestions

    def highest_scoring_games(self, total_games: int) -> list[Game]:
        """Creates a list of the top scored games that will be recommended to the user. The total games recommended
        is based on the vaue of total_games.

        Preconditions:
        - total_games >= 0
        """
        possible_suggestions = set()

        for game_id in self._user_nodes:
            for neighbour in self._user_nodes[game_id].neighbours:
                if neighbour not in possible_suggestions:
                    possible_suggestions.add(neighbour.game)

        actual_suggestions = []
        if possible_suggestions != set():
            while possible_suggestions != set() and len(actual_suggestions) != total_games:
                highest_game = highest_scoring_game(possible_suggestions)
                possible_suggestions.remove(highest_game)
                if highest_game not in [self._user_nodes[key].game for key in self._user_nodes]:
                    actual_suggestions.append(highest_game)
            sort_games(actual_suggestions)
            return actual_suggestions
        else:
            # When the user has not inputted any games, i.e., self.user_game_ids == []
            return self.top_games(total_games)


def read_data_csv(csv_file: str, total_rows: int) -> dict[int, Game]:
    """Load data from a CSV file and output the data as a mapping between game ids and their corresponding Game object.

    Preconditions:
    - csv_file refers to a valid CSV file, meaning that it consists of all the characteristics of every steam game.
    - total_rows >= 0
    """
    result = {}

    with open(csv_file, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip headers
        rows_so_far = 0
        for row in reader:
            if rows_so_far != total_rows:
                game_id = int(row[0])
                name = row[1]
                genres = []
                # 6 is skipped for rating(all words)
                positive_ratio = int(row[7])
                # 8 is skipped for user_reviews
                price_final = float(row[9])
                curr_game = Game((game_id, name), genres, price_final, positive_ratio)
                result[game_id] = curr_game
                rows_so_far += 1
    return result


def read_metadata_json(json_file: str) -> list[tuple]:
    """Load data from a JSON file and output the data as a list of tuples. The tuple contains the game_id(index 0, int)
    and the tags(index 1, list[str]).
    Preconditions:
        - json_file refers to a valid JSON file in terms of its format, meaning that it consists of the game id,
        description, and genres of all the games.
    """
    result = []

    with open(json_file, encoding='utf-8') as f:
        for line1 in [str.strip(line2.lower()) for line2 in f]:
            curr_full_metadata = json.loads(line1)
            relevant_metadata = (int(curr_full_metadata.get('app_id')), curr_full_metadata.get('tags'))
            result.append(relevant_metadata)
    return result


def generate_graph(game_file: str, json_file: str, user_info: tuple, max_price: float, total_nodes: int) -> GameGraph:
    """Creates a game graph
    Preconditions:
    -game_file refers to a csv file consisting of games and their attributes.
    -json_file is a json file that consists of the every game's genre in.
    -user_games refers to a list of games that the user has inputted.
    -len(user_info) == 2
    -total_nodes >= 0
    """
    json_result = read_metadata_json(json_file)
    csv_result = read_data_csv(game_file, total_nodes)
    game_graph = GameGraph(user_info[0], user_info[1], max_price)
    for index in range(0, total_nodes):
        metadata = json_result[index]
        game = csv_result[metadata[0]]
        game.genres = metadata[1]
        game_graph.add_game(game)

    # Creates edges between each node if applicable.
    game_graph.add_all_edges()
    # Computes all the scores and assigns the score to each node's associated game.
    game_graph.assign_all_scores()

    return game_graph


def sort_games(games: list[Game]) -> None:
    """Sorts a list of games in the given list in descending order of their metascore by mutating the list.
    """
    for index in range(0, len(games) - 1):
        if games[index].rating < games[index + 1].rating:
            games[index], games[index + 1] = games[index + 1], games[index]
            sort_games_helper(games, index)


def sort_games_helper(games: list[Game], current_index: int) -> None:
    """A helper function for sort_games that sorts an element from a given index in games[0:current_index]

    Preconditions:
    - 0 <= current_index and current_index <= len(games) - 1
    - games[:current_index] is sorted
    """
    for index in range(current_index, 0, -1):
        if games[index].rating > games[index - 1].rating:
            games[index], games[index - 1] = games[index - 1], games[index]


def highest_scoring_game(game_list: set[Game]) -> Optional[Game]:
    """Returns the highest scoring game from a set of games"""
    highest_score_so_far = 0
    game_so_far = None
    for game in game_list:
        if game.rating >= highest_score_so_far:
            highest_score_so_far = game.rating
            game_so_far = game
    return game_so_far


def runner(game_file: str, game_metadata_file: str) -> None:
    """Run a simulation based on the data from the given csv file."""
    total_nodes = 10000  # Maximum number of nodes is 46068
    # Part 1: Read datasets
    games = read_data_csv(game_file, total_nodes)
    valid_ids = list(games)  # List of all the game ids only

    # Part 2: Tkinter interface(ask for preferred genres)

    # Call the GameIDSelector class
    id_selector = user_interface.GameIDSelector(games, valid_ids)
    game_ids = id_selector.get_game_ids()

    # Call the GenreSelector class
    genre_selector = user_interface.GenreSelector()
    selected_genres = genre_selector.genres

    # Call the MaxPrice class
    input_price = user_interface.MaxPrice()
    max_price = input_price.price

    # Part 3: Build graph and compute scores
    game_graph = generate_graph(game_file, game_metadata_file, (game_ids, selected_genres), max_price, total_nodes)

    # Part 4: Give recommendations
    num_games_recommended = 5
    # Note: the returned list of games are in sorted order in terms
    top_games = game_graph.highest_scoring_games(num_games_recommended)

    for game in top_games:
        # Note: If all the game scores are 0 in the recommended games, it means that there were no games that satisfied
        # all the filters.
        print(game.name, game.price, game.rating)


if __name__ == '__main__':
    import python_ta
    runner('data/games.csv', 'data/games_metadata.json')
    python_ta.check_all(config={
        'extra-imports': ['genreselector', 'tkinter', 'csv', 'json', 'user_interface'],
        'allowed-io': [],
        'max-line-length': 120,
        'disable': ['forbidden-IO-function']
    })
