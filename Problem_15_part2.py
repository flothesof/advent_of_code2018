from Problem_15_part1 import parse_input, battle_finished, move_and_attack, sum_hit_points, render
from Problem_15_part1 import test_attack_move1, test_battle2, test_battle3, test_battle4, test_battle5


def run_full_battle(lines, elve_attack_power):
    creatures, game_map = parse_input(lines)
    n_turns = 0
    while not battle_finished(creatures):
        creatures, finished_during_turn = move_and_attack(creatures, game_map, elve_attack_power)
        n_turns += 1
    if finished_during_turn:
        n_turns -= 1
    outcome = n_turns * sum_hit_points(creatures)
    winner = creatures[0][0]
    n_winners = len([c for c in creatures if c[0] == winner])
    return winner, n_winners, outcome


winner, n_winners, outcome = run_full_battle(test_attack_move1.split(), elve_attack_power=15)
assert winner == 'E' and outcome == 4988

winner, n_winners, outcome = run_full_battle(test_battle2.split(), elve_attack_power=4)
assert winner == 'E' and outcome == 31284

winner, n_winners, outcome = run_full_battle(test_battle3.split(), elve_attack_power=15)
assert winner == 'E' and outcome == 3478

winner, n_winners, outcome = run_full_battle(test_battle4.split(), elve_attack_power=12)
assert winner == 'E' and outcome == 6474

winner, n_winners, outcome = run_full_battle(test_battle5.split(), elve_attack_power=34)
assert winner == 'E' and outcome == 1140

# part2
elve_attack_power = 3
inp = open('data/input15').read().strip().split()
creatures, _ = parse_input(inp)
n_elves = len([c for c in creatures if c[0] == 'E'])
winner, n_winners, outcome = run_full_battle(inp, elve_attack_power)

while not (winner == 'E' and n_winners == n_elves):
    elve_attack_power += 1
    winner, n_winners, outcome = run_full_battle(inp, elve_attack_power)
    print(f"elve_attack_power: {elve_attack_power}, winner: {winner}, n_winners: {n_winners}, outcome: {outcome}")
print(f"solution for part2: {outcome}")
