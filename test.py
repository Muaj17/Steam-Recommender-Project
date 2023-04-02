import pytest
import game_graph


class TestReadCsv:
    def test_read_data_csv(self):
        games = game_graph.read_data_csv('datasets/games.csv')
        for game in games:
            print(games[game].game_id, games[game].name, games[game].genres,
                  games[game].price)

    def test_read_metadata_csv(self):
        result = game_graph.read_metadata_json('datasets/games_metadata.json')
        print(result)
        assert type(result[0][0]) == int


if __name__ == '__main__':
    pytest.main()
