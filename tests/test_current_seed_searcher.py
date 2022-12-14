import unittest

from xddb import PlayerTeam, EnemyTeam, XDDBClient, QuickBattleSeedSearcher
from xdrngtool import CurrentSeedSearcher

from mocks import MockOperationReturnsTeamPair

class TestCurrentSeedSearcher(unittest.TestCase):
    def test_current_seed_searcher(self):
        test_case = [
            # 2回で見つかるもの
            (
                [
                    ((PlayerTeam.Rayquaza, 346, 235), (EnemyTeam.Zapdos, 313, 317)),
                    ((PlayerTeam.Mewtwo, 395, 346), (EnemyTeam.Kangaskhan, 350, 335))
                ],
                None,
                0x4d8483e7
            ),
            # 3回で見つかるもの
            (
                [
                    ((PlayerTeam.Mewtwo, 362, 349), (EnemyTeam.Articuno, 320, 388)),
                    ((PlayerTeam.Mewtwo, 342, 352), (EnemyTeam.Articuno, 325, 384)),
                    ((PlayerTeam.Mewtwo, 335, 382), (EnemyTeam.Articuno, 331, 361)),
                ],
                None,
                0xd9202593
            ),
            # 4回（以上）で見つかるもの
            # 途中で見失うもの
        ]
        for sequence, tsv, expected in test_case:
            
            client = XDDBClient()
            searcher = QuickBattleSeedSearcher(client, tsv) if tsv is not None else QuickBattleSeedSearcher(client)
            operation = MockOperationReturnsTeamPair(sequence)
            current_seed_searcher = CurrentSeedSearcher(searcher, operation)

            with self.subTest(sequence=sequence, tsv=tsv, expected=f"{expected:X}"):
                current_seed = current_seed_searcher.search()
                self.assertEqual(expected, current_seed)

if __name__ == "__main__":
    unittest.main()
