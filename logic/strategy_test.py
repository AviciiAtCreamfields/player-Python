import unittest
import uuid

import pandas as pd
import random

from logic.strategy import decide, euclid, get_base_level, filter_bases, survivors, defendersAtTime, add_population_of_enemy_at_start, get_base_distance, iterate_bases, get_enemy_values, get_enemy_distance, generate_base_costs, add_death_rate, add_gain_of_enemy
from models.base import Base
from models.base_level import BaseLevel
from models.board_action import BoardAction
from models.game import Game
from models.game_config import GameConfig, PathConfig
from models.base_level import BaseLevel
from models.base import Base

from models.game_state import GameState
from models.player_action import PlayerAction
from models.position import Position
from models.progress import Progress

from timeit import default_timer as timer

class TestStrategy(unittest.TestCase):

    our_player = 1
    def test_decide(self):
        test_base = Base(0, "test base", 1, 100, 1, 200, Position(0, 0, 0))

        test_game_state = GameState(
            [BoardAction(uuid.uuid4(), 0, 1, 2, 100, Progress(10, 4))],
            [test_base],
            GameConfig([BaseLevel(0, 0, 0)], PathConfig(0, 0)),
            Game(0, 0, 2, 2, 0),
        )

    base_levels = [
        BaseLevel(max_population=20,
            upgrade_cost=10,
            spawn_rate=1
        ),
        BaseLevel(
            max_population=40,
            upgrade_cost=20,
            spawn_rate=2
        ),
        BaseLevel(
            max_population=80,
            upgrade_cost=30,
            spawn_rate=3
        ),
        BaseLevel(
            max_population=100,
            upgrade_cost=40,
            spawn_rate=4
        ),
        BaseLevel(
            max_population=200,
            upgrade_cost=50,
            spawn_rate=5
        ),
        BaseLevel(
            max_population=300,
            upgrade_cost=100,
            spawn_rate=6
        ),
        BaseLevel(
            max_population=400,
            upgrade_cost=200,
            spawn_rate=7
        ),
        BaseLevel(
            max_population=500,
            upgrade_cost=400,
            spawn_rate=8
        ),
        BaseLevel(
            max_population=600,
            upgrade_cost=600,
            spawn_rate=9
        ),
        BaseLevel(
            max_population=700,
            upgrade_cost=800,
            spawn_rate=10
        ),
        BaseLevel(
            max_population=800,
            upgrade_cost=1000,
            spawn_rate=15
        ),
        BaseLevel(
            max_population=900,
            upgrade_cost=1500,
            spawn_rate=20
        ),
        BaseLevel(
            max_population=1000,
            upgrade_cost=2000,
            spawn_rate=25
        ),
        BaseLevel(
            max_population=2000,
            upgrade_cost=3000,
            spawn_rate=50
        )
    ]

    game_config = GameConfig(
        base_levels=base_levels,
        paths=PathConfig(
            grace_period=10,
            death_rate=1
        )
    )

    # game = Game({
    #     'uid': uid,
    #     'tick': tick,
    #     'player_count': playerCount,
    #     'remaining_players': remainingPlayers,
    #     'player': player
    # })
    
    enemy_bases = [
        # Base.fromAttributes(Position.fromAttributes(5, 0, 1), 0, 2, 2, 0, 0), 
        # Base.fromAttributes(Position.fromAttributes(7, 1, 2), 0, 3, 2, 0, 0), 
        Base(uid=0, name='Enemy_1', player=1, population=100, level=0, units_until_upgrade=1, position=Position(5, 0, 1)),
        Base(uid=0, name='Enemy_2', player=1, population=100, level=0, units_until_upgrade=1, position=Position(7, 1, 2))
    ]
    our_bases = [
        # Base.fromAttributes(Position.fromAttributes(4, 0, 1), 0, our_player, 2, 0, 0), 
        # Base.fromAttributes(Position.fromAttributes(3, 0, 2), 0, our_player, 2, 0, 0),
        Base(uid=0, name='Ally_1', player=our_player, population=100, level=0, units_until_upgrade=1, position=Position(4, 0, 1)),
        Base(uid=0, name='Ally_2', player=our_player, population=100, level=0, units_until_upgrade=1, position=Position(3, 0, 2))
    ]

    # def test_decide(self):
    #     test_base = Base.fromAttributes(Position.fromAttributes(0, 0, 0), 0, 0, 0, 0, 0)
    #     test_game_state = GameState.fromAttributes([BoardAction.fromAttributes(uuid.uuid4(), 0, Progress.fromAttributes(0, 0))], [test_base], GameConfig.fromAttributes([BaseLevel.fromAttributes(0, 0, 0)], PathsConfig.fromAttributes(0, 0)), Game.fromAttributes(0, 0, 0, 0, 0))

    #     want = PlayerAction(0, 0, 0)

    #     result = decide(test_game_state)
    #     self.assertEqual(str(want), str(result))

    def test_euclid(self):
        want = 1
        result = euclid(0, 0, 0, 1, 0, 0)
        self.assertEqual(want, result)
        
        want = 10
        result = euclid(7, 4, 3, 17, 6, 0)
        self.assertEqual(want, result)
    

    def test_get_base_level(self):
        want = self.base_levels[0]

        base = Base(uid=0, name='1', player=self.our_player, population=100, level=0, units_until_upgrade=1, position=Position(5, 0, 1))
        result = get_base_level(base, self.base_levels)

        self.assertEqual(want, result)


    # def test_filter_bases(self):
    #     result_our, result_other, result_empty = filter_bases(self.enemy_bases, self.our_player)
    #     self.assertEqual(str([]), str(result_our))
    #     self.assertEqual(str(self.enemy_bases), str(result_other))
    #     self.assertEqual(str([]), str(result_empty))
        
    #     result_our, result_other, result_empty = filter_bases(self.our_bases + self.enemy_bases, self.our_player)
    #     self.assertEqual(str(self.our_bases), str(result_our))
    #     self.assertEqual(str(self.enemy_bases), str(result_other))
    #     self.assertEqual(str([]), str(result_empty))


    # def test_survivors(self):
    #     bits = 10
    #     # our_base = Base.fromAttributes(Position.fromAttributes(18, 0, 1), 0, self.our_player, 2, 0, 0)
    #     our_base = Base(uid=0, name='Our Base', player=self.our_player, population=100, level=0, units_until_upgrade=1, position=Position(18, 0, 1))
    #     # target_base = Base.fromAttributes(Position.fromAttributes(8, 0, 1), 0, 0, 2, 0, 0)
    #     target_base = Base(uid=0, name='1', player=self.our_player, population=100, level=0, units_until_upgrade=1, position=Position(8, 0, 1))
    #     # surv = survivors(our_base, target_base,self.game_config, bits)
    #     # our_base = Base.fromAttributes(Position.fromAttributes(20, 0, 1), 0, self.our_player, 2, 0, 0)
    #     surv = survivors(our_base, target_base, self.game_config, bits)
    #     self.assertEqual(8, surv)


    # def test_defendersAtTime(self):
    #     # base_level 1 --> spawn_rate 2
    #     # population 20
    #     # base = Base.fromAttributes(Position.fromAttributes(5, 0, 1), 0, 2, 20, 1, 0)
    #     base = Base(uid=0, name='Our Base', player=self.our_player, population=100, level=0, units_until_upgrade=1, position=Position(5, 0, 1))
    #     want = 24
    #     result = defendersAtTime(2, base, self.game_config)
    #     self.assertEqual(want, result)

    def test_get_enemy_values(self):
        other_bases = [
            Base(uid=0, name='A', player=1, population=100, level=1, units_until_upgrade=1, position=Position(5, 0, 1)),
            Base(uid=1, name='B', player=1, population=100, level=14, units_until_upgrade=1, position=Position(5, 0, 1))
        ]

        enemy_values = get_enemy_values(other_bases, self.game_config)

        expected = {
            'index': [0, 1],
            'growth_rate': [
                self.game_config.base_levels[other_bases[0].level - 1].spawn_rate,
                self.game_config.base_levels[other_bases[1].level - 1].spawn_rate
            ],
            'max_population': [
                self.game_config.base_levels[other_bases[0].level - 1].max_population,
                self.game_config.base_levels[other_bases[1].level - 1].max_population
            ],
            'population': [100, 100]
        }

        self.assertEqual(enemy_values, expected)

    def test_get_enemy_distance(self):
        our_bases = [
            Base(uid=0, name='A', player=1, population=100, level=0, units_until_upgrade=1, position=Position(5, 0, 1)),
            Base(uid=1, name='B', player=1, population=100, level=0, units_until_upgrade=1, position=Position(5, 0, 1))
        ]

        other_bases = [
            Base(uid=2, name='A', player=1, population=100, level=0, units_until_upgrade=1, position=Position(5, 0, 1)),
            Base(uid=3, name='B', player=1, population=100, level=0, units_until_upgrade=1, position=Position(5, 0, 1))
        ]

        data = get_enemy_values(other_bases, self.game_config)

        data = get_enemy_distance(data, other_bases, our_bases)

        expected_data = data.copy()
        expected_data[0] = [
            get_base_distance(our_bases[0], other_bases[0]),
            get_base_distance(our_bases[0], other_bases[1]),
        ]
        expected_data[1] = [
            get_base_distance(our_bases[1], other_bases[0]),
            get_base_distance(our_bases[1], other_bases[1]),
        ]

        self.assertEqual(data, expected_data)

    def test_generate_base_costs(self):
        test_dict = {
            "index": [0, 1, 2, 3, 4],
            "growth_rate": [1, 1, 3, 10, 10],
            "max_population": [20, 20, 80, 700, 400],
            "population": [10, 20, 75, 3, 3],
            5: [5, 5, 10, 12, 20],
            6: [10, 12, 12, 3, 1]
        }

        data = generate_base_costs(test_dict)

        #print(data)
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(data.index.shape, (5,))
        self.assertEqual(len(data.index[0]), 4)
        self.assertEqual(data.index.names[0], "index")
        self.assertEqual(data.index.names[3], "population")
        self.assertEqual(data.index.get_level_values("max_population")[3], 700)
        self.assertEqual(data[5].values[0], 5)
        self.assertEqual(data[5].values[4], 20)
        self.assertEqual(data[6].values[0], 10)
        self.assertEqual(data[6].values[4], 1)

    def test_interate_bases(self):
        start_size = 10
        step_size = 100
        end_size = 1000
        max_level = 14
        max_xyz = 100

        our_bases = []
        other_bases = []
        for size in range(start_size, end_size + 1, step_size):
            for i in range(0, size):
                rand_lvl = random.randint(1, max_level)
                our_bases.append(Base(uid=i,
                                      name='Ally_' + str(i + 1),
                                      player=self.our_player,
                                      population=random.randint(1, self.base_levels[rand_lvl - 1].max_population),
                                      level=rand_lvl,
                                      units_until_upgrade=random.randint(0, self.base_levels[rand_lvl - 1].upgrade_cost - 1),
                                      position=Position(random.randint(0, max_xyz), random.randint(0, max_xyz), random.randint(0, max_xyz))))
                rand_lvl = random.randint(1, max_level)
                other_bases.append(Base(uid=size + i,
                                      name='Enemy_' + str(size + i + 1),
                                      player=size + i,
                                      population=random.randint(1, self.base_levels[rand_lvl - 1].max_population),
                                      level=rand_lvl,
                                      units_until_upgrade=random.randint(0, self.base_levels[rand_lvl - 1].upgrade_cost - 1),
                                      position=Position(random.randint(0, max_xyz), random.randint(0, max_xyz), random.randint(0, max_xyz))))
        
            start = timer()
            player_actions = iterate_bases(other_bases, our_bases, self.game_config)
            end = timer()
            self.assertTrue(isinstance(player_actions, list))
            self.assertTrue(isinstance(player_actions[0], PlayerAction))
            # iterate_bases must be fast (execution time less than 1 sec.)
            self.assertLess(end - start, 1)

    def test_add_death_rate(self):
        test_dict = {
            "index": [0, 1, 2, 3, 4],
            "growth_rate": [1, 1, 3, 10, 10],
            "max_population": [20, 20, 80, 700, 400],
            "population": [10, 20, 75, 3, 3],
            5: [5, 5, 10, 12, 20],
            6: [10, 12, 12, 3, 1]
        }
        test_df = generate_base_costs(test_dict)
        data = add_death_rate(test_df, self.game_config)
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(data[5].values[0], 0)
        self.assertEqual(data[6].values[0], 0)
        self.assertEqual(data[6].values[1], 2)
    
    def test_add_gain_of_enemy(self):
        test_dict = {
            "index": [0, 1, 2, 3, 4],
            "growth_rate": [1, 1, 3, 10, 10],
            "max_population": [20, 20, 80, 700, 400],
            "population": [10, 20, 75, 3, 3],
            5: [5, 5, 10, 12, 20],
            6: [10, 12, 12, 3, 1]
        }
        allBases = generate_base_costs(test_dict)
        test_df = add_death_rate(allBases, self.game_config)
        data = add_gain_of_enemy(test_df, allBases)

        gain_df = data - test_df
        
        self.assertEqual(allBases[5].values[0] * allBases.index.get_level_values("growth_rate")[0], gain_df[5].values[0])
        self.assertEqual(allBases[6].values[4] * allBases.index.get_level_values("growth_rate")[4], gain_df[6].values[4])

    def test_add_population_of_enemy_at_start(self):
        test_dict = {
            "index": [0, 1, 2, 3, 4],
            "growth_rate": [1, 1, 3, 10, 10],
            "max_population": [20, 20, 80, 700, 400],
            "population": [10, 20, 75, 3, 3],
            5: [5, 5, 10, 12, 20],
            6: [10, 12, 12, 3, 1]
        }
        all_bases = generate_base_costs(test_dict)
        all_bases_distance_costs = all_bases.copy()
        data = add_population_of_enemy_at_start(all_bases_distance_costs, all_bases)
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(data[5].values[0], 15)
        self.assertEqual(data[6].values[0], 20)
        self.assertEqual(data[6].values[1], 32)
        
    def test_attack(self):
        other_bases = self.enemy_bases[1]
        our_bases = self.our_bases[1]
        # attack(other_bases, our_bases, self.game_config)



if __name__ == "__main__":
    unittest.main()
