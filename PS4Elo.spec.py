import unittest
import PS4Elo

class TestPS4Elo(unittest.TestCase):
    def test_expected_score(self):
        def calc_score(ranking, other_ranking):
            return round(PS4Elo.expected_score(ranking, other_ranking), 4)
        self.assertEqual(calc_score(1500, 1500), 0.5)
        self.assertEqual(calc_score(1500, 1490), 0.5144)
        self.assertEqual(calc_score(1490, 1500), 0.4856)
        self.assertEqual(calc_score(1800, 1000), 0.9901)
        self.assertEqual(calc_score(1000, 2000), 0.0032)
        self.assertEqual(calc_score(1000, 3000), 0.0000)

    def test_ranking_delta(self):
        rank_delta = PS4Elo.ranking_delta
        self.assertEqual(rank_delta(1500, 1500, PS4Elo.Result.win, 32), 16)
        self.assertEqual(rank_delta(1500, 1500, PS4Elo.Result.loss, 32), -16)
        self.assertEqual(rank_delta(2000, 1500, PS4Elo.Result.win, 32), 2)
        self.assertEqual(rank_delta(1000, 1500, PS4Elo.Result.win, 32), 30)
        self.assertEqual(rank_delta(3000, 1000, PS4Elo.Result.win, 32), 1)
        self.assertEqual(rank_delta(3000, 1000, PS4Elo.Result.loss, 32), -32)
        self.assertEqual(rank_delta(1000, 3000, PS4Elo.Result.loss, 32), -1)

    def test_ranking_delta_for_game(self):
        game_rankdelta = PS4Elo.ranking_delta_for_game

        team1 = [1, 2]
        team2 = [3, 4]
        teams = [team1, team2]
        players = {
            1: PS4Elo.Player(1, 2000),
            2: PS4Elo.Player(1, 1500),
            3: PS4Elo.Player(1),
            4: PS4Elo.Player(1),
            5: PS4Elo.Player(1, 1000),
            6: PS4Elo.Player(1, 3000),
        }
        game1 = PS4Elo.Game(teams, 0, {})
        result1 = {
            1: 1,
            2: 10,
            3: -4,
            4: -4
        }
        self.assertDictEqual(game_rankdelta(game1, players), result1)

        team3 = [2, 3]
        team4 = [5, 6]
        teams2 = [team3, team4]
        game2 = PS4Elo.Game(teams2, 1, {})
        result2 = {
            2: -1,
            3: -1,
            5: 19,
            6: 1
        }
        self.assertDictEqual(game_rankdelta(game2, players), result2)

        game3 = PS4Elo.Game(teams2, 0, {})
        result3 = {
            2: 19,
            3: 19,
            5: -1,
            6: -20
        }
        self.assertDictEqual(game_rankdelta(game3, players), result3)

    def test_ranking_delta_for_game_multi_team(self):
        game_rankdelta = PS4Elo.ranking_delta_for_game

        team1 = [1, 2]
        team2 = [3, 4]
        team3 = [5, 6]
        teams = [team1, team2, team3]
        players = {
            1: PS4Elo.Player(1, 2000),
            2: PS4Elo.Player(1, 1500),
            3: PS4Elo.Player(1),
            4: PS4Elo.Player(1),
            5: PS4Elo.Player(1, 1000),
            6: PS4Elo.Player(1, 3000),
        }
        game = PS4Elo.Game(teams, 0, {})

        result = {
            1:4,
            2:16,
            3:-4,
            4:-4,
            5:-1,
            6:-20
        }

        self.assertDictEqual(game_rankdelta(game, players), result)

    def test_calculate_scrub_ranking(self):
        scrub_mod = PS4Elo.calculate_scrub_modifier

        team1 = [1, 2]
        team2 = [3, 4]
        teams = [team1, team2]
        scrubs = {
            1: 1,
            2: 2,
            3: 3,
            4: 0
        }
        player1 = PS4Elo.Player(1)
        player2 = PS4Elo.Player(2)
        player3 = PS4Elo.Player(3)
        player4 = PS4Elo.Player(4)
        game = PS4Elo.Game(teams, 0, scrubs)

        self.assertEqual(scrub_mod(player1, game), 1.1)
        self.assertEqual(round(scrub_mod(player2, game), 4), 1.21)
        self.assertEqual(round(scrub_mod(player3, game), 4), 1.331)
        self.assertEqual(round(scrub_mod(player4, game), 4), 1)

    def test_calculate_ranking(self):
        calc_ranks = PS4Elo.calculate_rankings
        Game = PS4Elo.Game

        team1 = [1, 2]
        team2 = [3, 4]
        team3 = [1, 3]
        team4 = [2, 4]

        teams = [team1, team2]
        scrubs = { 3: 4 }
        game1 = Game(teams, 0, scrubs)
        game2 = Game(teams, 1, {})

        games1 = [game1, game2]

        result1 = calc_ranks(games1)

        self.assertEqual(result1[1].ranking, 1499)
        self.assertEqual(result1[2].ranking, 1499)
        self.assertEqual(result1[3].ranking, 1501)
        self.assertEqual(result1[4].ranking, 1501)

        games2 = [game2, game2, game2]

        result2 = calc_ranks(games2)
        self.assertEqual(result2[1].ranking, 1472)
        self.assertEqual(result2[2].ranking, 1472)
        self.assertEqual(result2[3].ranking, 1528)
        self.assertEqual(result2[4].ranking, 1528)

if __name__ == '__main__':
    unittest.main()
