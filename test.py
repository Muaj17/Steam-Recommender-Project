import pytest
import game_graph_csv


class TestReadCsv:
    def test_read_data_csv(self):
        games = game_graph_csv.read_data_csv('datasets/game_simple.csv')
        print(games)
        for game in games:
            print(games[game].game_id, games[game].name, games[game].genres, games[game].operating_systems,
                  games[game].price, games[game].date_release, games[game].rating)

    def test_read_metadata_csv(self):
        result = game_graph_csv.read_metadata_json('datasets/game_metadata_simple.json')
        print(result)
        assert type(result[0][0]) == int


if __name__ == '__main__':
    pytest.main()
