class AbstractGameGraph:
    """A graph containing nodes that represent a game. Nodes are connected depending on the number of genres that they
    have in common with another game and the user's preferred genres.

    NOTE:
    - the min_genres_game and min_genres_edge were added in order to create a purpose of the graph data structure.
    Otherwise, we are solely using the nodes for their scores, which does not take advantage of the edges formed between
    nodes. Thus, the min_genres_game and min_genres_edge can be used as a way of filtering

    Representation Invariants:
    - all(self._nodes[game_id].game_id = game_id for game_id in self_nodes)
    """
    #  Private Instance Attibutes:
    #  - _nodes: A mapping from game ids to GameNode objects in the GameGraph.

    _nodes: dict[int, GameNode]

    def __init__(self) -> None:
        """Initializes the game graph"""
        self._nodes = {}

    def add_game(self, game: Game) -> None:
        """Adds a game node into the graph if they have the minimum amount of intersecting genres with the
        user (i.e. self.min_genres_game)"""
        raise NotImplementedError

    def add_edge(self, game1: GameNode, game2: GameNode) -> None:
        """Creates an edge between two game nodes if they have the minimum amount of intersecting genres

        Preconditions:
        - game1 in self._nodes and game2 in self._nodes
        """
        raise NotImplementedError

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


class SimilarGameGraph(AbstractGameGraph):
    """Game graph that is formed based specifically based on the games that the user has inputted.

    Instances Attributes:
    - min_genres_edge is the amount of similar genres that the games of two game nodes must have in order for an edge
    to be formed between them.
    - user_game is a list of games that the user has provided in order to make recommendations.

    Representation Invariants:
    - self.user_game != []
    . self.min_genres_edge >= 0
    """
    min_genres_edge: int
    user_game: list[str]

    def __init__(self, similar_genres: int, user_game: list[str]) -> None:
        """Initializes the graph"""
        AbstractGameGraph.__init__(self)
        self.min_genres_edge = similar_genres
        self.user_game = user_game

    def add_game(self, game: Game) -> None:
        """Adds a game into the graph"""
        game_id = game.game_id
        self._nodes[game_id] = GameNode(game)

    def add_edge(self, game1: GameNode, game2: GameNode) -> None:
        """Creates an edge between two nodes in the graph"""
        similar_games = game1.game.genre_count(game2.game.genres)
        if similar_games >= self.min_genres_edge:
            game1.neighbours.append(game2)
            game2.neighbours.append(game1)


class SimilarGenreGraph(AbstractGameGraph):
    """Game graph that is formed specifically based on the genres that the user has inputted

    Instance Attributes:
    - min_genres_game is the minimum number of genres that a game needs to have as a part of the user's genre list.
    - genre_list is a list of genres that the user has provided.

    Representation Invariants:
    - self.genre_list != []
    - min_genres_game >= 0
    """
    genre_list: list[str]
    min_genres_game: int

    def __init__(self, genre_list: list[str], min_genres_game: int) -> None:
        """Initializes the game graph"""
        AbstractGameGraph.__init__(self)
        self.genre_list = genre_list
        self.min_genres_game = min_genres_game

    def add_game(self, game: Game) -> None:
        """Adds a game node into the graph if they have the minimum amount of intersecting genres with the
        user"""
        game_count = game.genre_count(self.genre_list)
        game_id = game.game_id
        if game_count >= self.min_genres_game:
            self._nodes[game_id] = GameNode(game)

    def add_edge(self, game1: GameNode, game2: GameNode) -> None:
        """Creates an edge between two game nodes if they have the minimum amount of intersecting genres
        Preconditions:
        - game1 in self._nodes and game2 in self._nodes
        """
        game1.neighbours.append(game2)
        game2.neighbours.append(game1)
