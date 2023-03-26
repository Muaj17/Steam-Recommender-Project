import pytest
import game_graph_1

class Test_read_csv:
    def test_read_data_csv(self):
        games = game_graph_1.read_data_csv('datasets/game_simple.csv')
        print()
        for game in games:
            print(game.game_id, game.name, game.genres, game.operating_systems, game.price, game.date_release, game.rating)

    def test_read_metadata_csv(self):
        result = game_graph_1.read_metadata_csv('datasets/game_metadata_simple.csv')
        print(result)
        assert type(result[0][0]) == int


if __name__ == '__main__':
    pytest.main()
