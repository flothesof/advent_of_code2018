import networkx as nx
from math import inf as INFINITY

test_input1 = """#######
#E..G.#
#...#.#
#.G.#G#
#######"""

test_input2 = """#######
#.E...#
#.....#
#...G.#
#######"""

test_move1 = """#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########"""

test_move2 = """#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########"""

test_move3 = """#########
#..G.G..#
#...G...#
#.G.E.G.#
#.......#
#G..G..G#
#.......#
#.......#
#########"""

test_move4 = """#########
#.......#
#..GGG..#
#..GEG..#
#G..G...#
#......G#
#.......#
#.......#
#########"""

test_attack1 = """G....
..G..
..EG.
..G..
...G."""

test_attack_move1 = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""

test_attack_move2_hps = (200, 197, 197, 200, 197, 197)

test_attack_move2 = """#######
#..G..#
#...EG#
#.#G#G#
#...#E#
#.....#
#######"""

test_attack_move3_hps = (200, 200, 188, 194, 194, 194)

test_attack_move3 = """#######
#...G.#
#..GEG#
#.#.#G#
#...#E#
#.....#
#######"""

test_attack_move23_hps = (200, 200, 131, 131, 131)

test_attack_move23 = """#######
#...G.#
#..G.G#
#.#.#G#
#...#E#
#.....#
#######"""

test_attack_move47_hps = (200, 131, 59, 200)

test_attack_move47 = """#######
#G....#
#.G...#
#.#.#G#
#...#.#
#....G#
#######"""

FOUR_DIRS = [[1, 0], [-1, 0], [0, 1], [0, -1]]
# sort by TRC coords when t=('G', 1, 3, 200)
SORT_BY_TRC = lambda t: t[0:3]


def parse_input(lines):
    game_map = set()
    creatures = []
    for r, row in enumerate(lines):
        row = row.strip()
        for c, tile in enumerate(row):
            if tile in 'GE.':
                game_map.add((r, c))
                if tile in 'GE':
                    creatures.append((tile, r, c, 200))

    return creatures, game_map


# unit tests parse_input
creatures, game_map = parse_input(test_input1.split())
assert all([('E', 1, 1, 200) in creatures, ('G', 1, 4, 200) in creatures, ('G', 3, 2, 200) in creatures])


def in_range(creature, creatures, game_map):
    creature_type, R, C, hp = creature
    occupied_cells = [(r, c) for (t, r, c, hp) in creatures]
    enemies = [c for c in creatures if c[0] != creature_type]
    cells = []
    for enemy in enemies:
        r, c = enemy[1], enemy[2]
        for dr, dc in FOUR_DIRS:
            rc = (r + dr, c + dc)
            if rc not in occupied_cells:
                if rc in game_map:
                    cells.append(rc)
    return cells


# unit tests in_range
creatures, game_map = parse_input(test_input1.split())
cells_in_range = in_range(('E', 1, 1, 200), creatures, game_map)
assert all([rc in cells_in_range for rc in [(1, 3), (1, 5), (2, 2), (3, 1), (3, 3), (2, 5)]])
cells_in_range = in_range(('G', 1, 4, 200), creatures, game_map)
assert all([rc in cells_in_range for rc in [(1, 2), (2, 1)]])


def choose_nearest_reachable(creature, cells_in_range, creatures, game_map):
    # build a graph that includes only empty cells
    G = nx.Graph()
    occupied_cells = [(r, c) for (t, r, c, hp) in creatures]
    G.add_node(creature[1:3])
    G.add_nodes_from([cell for cell in game_map if cell not in occupied_cells])
    for node in G:
        (r, c) = node
        for dr, dc in FOUR_DIRS:
            other = (r + dr, c + dc)
            if other in G:
                G.add_edge(node, other)
    # try to find a path
    reachable_cells = {}
    for cell in cells_in_range:
        try:
            path = nx.shortest_path(G, creature[1:3], cell)
            path_length = len(path) - 1
            reachable_cells[cell] = (path_length, path)
        except nx.NetworkXNoPath:
            pass
    if len(reachable_cells) == 0:
        raise ValueError('There is no path even though there is a free cell in range!')
    min_length = min((reachable_cells[rc][0] for rc in reachable_cells))
    nearest_reachable_cells = [rc for rc in reachable_cells if reachable_cells[rc][0] == min_length]
    assert len(nearest_reachable_cells) > 0
    chosen = sorted(nearest_reachable_cells, key=lambda item: item[0])[0]
    assert min_length > 0
    return list(reachable_cells.keys()), nearest_reachable_cells, chosen


# unit tests choose_nearest_reachable
creatures, game_map = parse_input(test_input1.split())
creature = ('E', 1, 1, 200)
cells_in_range = in_range(creature, creatures, game_map)
reachable_cells, nearest_reachable_cells, chosen = choose_nearest_reachable(creature, cells_in_range,
                                                                            creatures,
                                                                            game_map)
assert chosen == (1, 3)
assert all([rc in reachable_cells for rc in [(1, 3), (2, 2), (3, 1), (3, 3)]])
assert all([rc in nearest_reachable_cells for rc in [(1, 3), (2, 2), (3, 1)]])


def choose_next_pos(chosen, creature, creatures, game_map):
    occupied_cells = [(r, c) for (t, r, c, hp) in creatures]
    dists = {cell: INFINITY for cell in occupied_cells}
    dists[chosen] = 0
    while len(dists) < len(game_map):
        new_dists = {}
        for cell, val in dists.items():
            if val < INFINITY:
                (r, c) = cell
                for dr, dc in FOUR_DIRS:
                    other = (r + dr, c + dc)
                    if other not in dists and other in game_map:
                        new_dists[other] = val + 1
        if len(new_dists) == 0:
            break
        else:
            dists.update(new_dists)

    t, r, c, hp = creature
    adjacent = {(r + dr, c + dc): dists[(r + dr, c + dc)] for dr, dc in FOUR_DIRS
                if (r + dr, c + dc) in dists}
    assert len(adjacent) > 0
    closest_dist = min(adjacent.values())
    closest_cell = sorted({k: v for k, v in adjacent.items() if v == closest_dist})[0]
    return dists, closest_cell


# unit tests choose_next_pos
creatures, game_map = parse_input(test_input2.split())
creature = ('E', 1, 2, 200)
cells_in_range = in_range(creature, creatures, game_map)
reachable_cells, nearest_reachable_cells, chosen = choose_nearest_reachable(creature, cells_in_range,
                                                                            creatures,
                                                                            game_map)
assert chosen == (2, 4)
dists, next_pos = choose_next_pos(chosen, creature, creatures, game_map)
assert next_pos == (1, 3)
assert dists[(1, 1)] == 4


def render(creatures, game_map):
    creature_pos = {c[1:3]: c[0] for c in creatures}
    rendered = {}
    for k in game_map:
        if k in creature_pos:
            rendered[k] = creature_pos[k]
        else:
            rendered[k] = '.'
    R, C = max(rendered, key=lambda item: item[0])[0], max(rendered, key=lambda item: item[1])[1]
    for r in range(R + 1):
        for c in range(C + 1):
            if (r, c) in rendered:
                print(rendered[(r, c)], end='')
            else:
                print("#", end='')
        print()
    print()


def in_contact_with_enemy(creature, creatures):
    t, r, c, hp = creature
    enemies = {cr[1:3]: cr for cr in creatures if cr[0] != t}
    adjacent_enemies = []
    for dr, dc in FOUR_DIRS:
        if (r + dr, c + dc) in enemies:
            adjacent_enemies.append(enemies[(r + dr, c + dc)])
    return len(adjacent_enemies) > 0, adjacent_enemies


def move_only(creatures, game_map):
    new_creatures = creatures[:]
    move_order = sorted(creatures, key=lambda items: (items[1], items[2]))
    for creature in move_order:
        t, r, c, hp = creature
        is_in_contact, enemies_in_contact = in_contact_with_enemy(creature, new_creatures)
        if not is_in_contact:
            cells_in_range = in_range(creature, new_creatures, game_map)
            if len(cells_in_range) > 0:
                reachable_cells, nearest_reachable_cells, chosen = choose_nearest_reachable(creature, cells_in_range,
                                                                                            new_creatures,
                                                                                            game_map)
                dists, next_pos = choose_next_pos(chosen, creature, new_creatures, game_map)
                new_creature = (t, *next_pos, hp)
                new_creatures.remove(creature)
                new_creatures.append(new_creature)
            else:
                # print(f"creature {creature} cannot move since no more cells in range")
                pass
        else:
            # already at contact, no move to do
            # print(f"creature {creature} is in contact")
            pass
    return new_creatures


creatures_step1, game_map = parse_input(test_move1.split())
creatures_step2, game_map = parse_input(test_move2.split())
creatures_step2_pred = move_only(creatures_step1, game_map)
assert sorted(creatures_step2_pred) == sorted(creatures_step2)

creatures_step3, game_map = parse_input(test_move3.split())
creatures_step3_pred = move_only(creatures_step2, game_map)
assert sorted(creatures_step3_pred, key=SORT_BY_TRC) == sorted(creatures_step3, key=SORT_BY_TRC)

creatures_step4, game_map = parse_input(test_move4.split())
creatures_step4_pred = move_only(creatures_step3, game_map)
assert sorted(creatures_step4_pred) == sorted(creatures_step4)


def battle_finished(creatures):
    return len(set(cr[0] for cr in creatures)) == 1


def move_and_attack(creatures, game_map, elve_attack_power=3):
    new_creatures = creatures[:]  # let's work on a copy of creatures
    move_order = sorted(creatures, key=lambda items: (items[1], items[2]))
    dead_creatures = []
    finished_during_turn = False
    for creature in move_order:
        # move phase
        # ==========
        if creature[:3] in dead_creatures:
            continue
        t, r, c, hp = creature
        is_in_contact, enemies_in_contact = in_contact_with_enemy(creature, new_creatures)
        if not is_in_contact:
            cells_in_range = in_range(creature, new_creatures, game_map)
            if len(cells_in_range) > 0:
                try:
                    reachable_cells, nearest_reachable_cells, chosen = choose_nearest_reachable(creature,
                                                                                                cells_in_range,
                                                                                                new_creatures,
                                                                                                game_map)
                    dists, next_pos = choose_next_pos(chosen, creature, new_creatures, game_map)
                    new_creature = (t, *next_pos, hp)
                    new_creatures.remove(creature)
                    new_creatures.append(new_creature)
                    # we overwrite creature for the attack move
                    creature = new_creature
                except ValueError:
                    pass
            else:
                #print(f"[MOVE] creature {creature} cannot move since no more cells in range")
                pass
        else:
            # already at contact, no move to do
            pass
            #print(f"[MOVE] creature {creature} is already in contact with enemy")
        # attack phase
        # ============
        if battle_finished(new_creatures):
            finished_during_turn = True
        is_in_contact, enemies_in_contact = in_contact_with_enemy(creature, new_creatures)
        if is_in_contact:
            #print(f"[ATTACK] creature {creature} can attack {len(enemies_in_contact)} enemies")
            selected_target = min(enemies_in_contact, key=lambda item: (item[3], item[1], item[2]))
            if creature[0] == 'E':
                new_hp = selected_target[3] - elve_attack_power
            else:
                new_hp = selected_target[3] - 3
            new_creatures.remove(selected_target)
            if new_hp > 0:
                new_creatures.append(selected_target[:3] + (new_hp,))
            else:
                dead_creatures.append(selected_target[:3])

    return new_creatures, finished_during_turn


# unit test simple combat
creatures, game_map = parse_input(test_attack1.split())
creatures = [('G', 0, 0, 9), ('G', 1, 2, 4), ('E', 2, 2, 200), ('G', 2, 3, 2),
             ('G', 3, 2, 2), ('G', 4, 3, 1)]
creatures_after_attack, __ = move_and_attack(creatures, game_map)
assert len(creatures_after_attack) == len(creatures) - 1


# unit test complex combat
def parse_input_and_hp(lines, hps):
    creatures, game_map = parse_input(lines)
    creatures = [(t, r, c, hp_new) for (t, r, c, hp_old), hp_new in zip(creatures, hps)]
    return creatures, game_map


creatures, game_map = parse_input(test_attack_move1.split())
creatures_attack2, game_map = parse_input_and_hp(test_attack_move2.split(), test_attack_move2_hps)
creatures_attack2_pred, __ = move_and_attack(creatures, game_map)
assert sorted(creatures_attack2, key=SORT_BY_TRC) == sorted(creatures_attack2_pred, key=SORT_BY_TRC)

creatures_attack3, game_map = parse_input_and_hp(test_attack_move3.split(), test_attack_move3_hps)
creatures_attack3_pred, __ = move_and_attack(creatures_attack2_pred, game_map)
assert sorted(creatures_attack3, key=SORT_BY_TRC) == sorted(creatures_attack3_pred, key=SORT_BY_TRC)

creatures = creatures_attack3_pred[:]
for _ in range(21):
    creatures, __ = move_and_attack(creatures, game_map)

creatures_attack23, game_map = parse_input_and_hp(test_attack_move23.split(), test_attack_move23_hps)
assert sorted(creatures_attack23, key=SORT_BY_TRC) == sorted(creatures, key=SORT_BY_TRC)

for _ in range(24):
    creatures, finished_during_turn = move_and_attack(creatures, game_map)
creatures_attack47, game_map = parse_input_and_hp(test_attack_move47.split(), test_attack_move47_hps)
assert sorted(creatures_attack47, key=SORT_BY_TRC) == sorted(creatures, key=SORT_BY_TRC)

# global tests
test_battle1 = """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######"""



def sum_hit_points(creatures):
    return sum(cr[3] for cr in creatures)


creatures, game_map = parse_input(test_attack_move1.split())
n_turns = 0
while not battle_finished(creatures):
    creatures, finished_during_turn = move_and_attack(creatures, game_map)
    n_turns += 1
outcome = n_turns * sum_hit_points(creatures)
assert n_turns == 47 and outcome == 27730

creatures, game_map = parse_input(test_battle1.split())
n_turns = 0
while not battle_finished(creatures):
    creatures, finished_during_turn = move_and_attack(creatures, game_map)
    n_turns += 1
if finished_during_turn:
    n_turns -= 1
outcome = n_turns * sum_hit_points(creatures)
assert n_turns == 37 and outcome == 36334

test_battle2 = """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"""

creatures, game_map = parse_input(test_battle2.split())
n_turns = 0
while not battle_finished(creatures):
    creatures, finished_during_turn = move_and_attack(creatures, game_map)
    n_turns += 1
if finished_during_turn:
    n_turns -= 1
outcome = n_turns * sum_hit_points(creatures)
assert n_turns == 46 and outcome == 39514

test_battle3 = """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""

creatures, game_map = parse_input(test_battle3.split())
n_turns = 0
while not battle_finished(creatures):
    creatures, finished_during_turn = move_and_attack(creatures, game_map)
    n_turns += 1
if finished_during_turn:
    n_turns -= 1
outcome = n_turns * sum_hit_points(creatures)
assert n_turns == 35 and outcome == 27755

test_battle4 = """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"""

creatures, game_map = parse_input(test_battle4.split())
n_turns = 0
while not battle_finished(creatures):
    creatures, finished_during_turn = move_and_attack(creatures, game_map)
    n_turns += 1
if finished_during_turn:
    n_turns -= 1
outcome = n_turns * sum_hit_points(creatures)
assert n_turns == 54 and outcome == 28944

test_battle5 = """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""

creatures, game_map = parse_input(test_battle5.split())
n_turns = 0
while not battle_finished(creatures):
    creatures, finished_during_turn = move_and_attack(creatures, game_map)
    n_turns += 1
if finished_during_turn:
    n_turns -= 1
outcome = n_turns * sum_hit_points(creatures)
assert n_turns == 20 and outcome == 18740

if __name__ == '__main__':
    # part 1
    creatures, game_map = parse_input(open('data/input15').read().strip().split())
    n_turns = 0
    while not battle_finished(creatures):
        creatures, finished_during_turn = move_and_attack(creatures, game_map)
        n_turns += 1
    if finished_during_turn:
        n_turns -= 1
    outcome = n_turns * sum_hit_points(creatures)
    print(f"solution for part1: {outcome}")




