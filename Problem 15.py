import networkx as nx

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


def parse_input(lines):
    game_map = set()
    creatures = []
    for r, row in enumerate(lines):
        row = row.strip()
        for c, tile in enumerate(row):
            if tile in 'GE.':
                game_map.add((r, c))
                if tile in 'GE':
                    creatures.append((tile, r, c))

    return creatures, game_map


# unit tests parse_input
creatures, game_map = parse_input(test_input1.split())
assert all([('E', 1, 1) in creatures, ('G', 1, 4) in creatures, ('G', 3, 2)])


def in_range(creature, creatures, game_map):
    creature_type, R, C = creature
    occupied_cells = [(r, c) for (t, r, c) in creatures]
    enemies = [c for c in creatures if c[0] != creature_type]
    cells = []
    for enemy in enemies:
        r, c = enemy[1], enemy[2]
        for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            rc = (r + dr, c + dc)
            if rc not in occupied_cells:
                if rc in game_map:
                    cells.append(rc)
    return cells


# unit tests in_range
creatures, game_map = parse_input(test_input1.split())
cells_in_range = in_range(('E', 1, 1), creatures, game_map)
assert all([rc in cells_in_range for rc in [(1, 3), (1, 5), (2, 2), (3, 1), (3, 3), (2, 5)]])
cells_in_range = in_range(('G', 1, 4), creatures, game_map)
assert all([rc in cells_in_range for rc in [(1, 2), (2, 1)]])


def choose_nearest_reachable(creature, cells_in_range, creatures, game_map):
    # build a graph that includes only empty cells
    G = nx.Graph()
    occupied_cells = [(r, c) for (t, r, c) in creatures]
    G.add_node(creature[1:])
    G.add_nodes_from([cell for cell in game_map if cell not in occupied_cells])
    for node in G:
        (r, c) = node
        for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            other = (r + dr, c + dc)
            if other in G:
                G.add_edge(node, other)
    # try to find a path
    reachable_cells = {}
    for cell in cells_in_range:
        try:
            path = nx.shortest_path(G, creature[1:], cell)
            path_length = len(path) - 1
            reachable_cells[cell] = (path_length, path)
        except nx.NetworkXNoPath:
            pass
    min_length = min((reachable_cells[rc][0] for rc in reachable_cells))
    nearest_reachable_cells = [rc for rc in reachable_cells if reachable_cells[rc][0] == min_length]
    assert len(nearest_reachable_cells) > 0
    chosen = sorted(nearest_reachable_cells, key=lambda item: item[0])[0]
    assert min_length > 0
    pos_after_step = reachable_cells[chosen][1][1]
    return list(reachable_cells.keys()), nearest_reachable_cells, chosen, pos_after_step


# unit tests are_reachable
creatures, game_map = parse_input(test_input1.split())
creature = ('E', 1, 1)
cells_in_range = in_range(creature, creatures, game_map)
reachable_cells, nearest_reachable_cells, chosen, pos_after_step = choose_nearest_reachable(creature, cells_in_range,
                                                                                            creatures,
                                                                                            game_map)
assert chosen == (1, 3)
assert all([rc in reachable_cells for rc in [(1, 3), (2, 2), (3, 1), (3, 3)]])
assert all([rc in nearest_reachable_cells for rc in [(1, 3), (2, 2), (3, 1)]])

creatures, game_map = parse_input(test_input2.split())
creature = ('E', 1, 2)
cells_in_range = in_range(creature, creatures, game_map)
reachable_cells, nearest_reachable_cells, chosen, pos_after_step = choose_nearest_reachable(creature, cells_in_range,
                                                                                            creatures,
                                                                                            game_map)
