from collections import OrderedDict
from copy import deepcopy

class Creature:
    def __init__(self, creature_type, r, c, hitpoints=200, attack_power=3):
        self.creature_type = creature_type
        self.r = r
        self.c = c
        self.hitpoints = hitpoints
        self.attack_power = attack_power

    def __repr__(self):
        return f"{self.creature_type} at ({self.r}, {self.c}), hitpoints: {self.hitpoints}"

def load_input(fname):
    creatures = []
    terrain = []
    lines = open(fname).readlines()
    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            if val == 'G':
                creatures.append(Creature('Goblin', r, c))
            elif val == 'E':
                creatures.append(Creature('Elf', r, c))
            elif val == '#':
                terrain.append((r, c))
    return creatures, terrain

def identify_targets(unit, creatures):
    unit_type = unit.creature_type
    return [c for c in creatures if c.creature_type != unit_type]

def is_valid(r, c, rmax, cmax):
    return r >= 0 and r <= rmax and c >= 0 and c <= cmax

def compute_target_range(targets, rmax, cmax, other_creatures, terrain):
    """Returns a list of empty cells ajacent to target units."""
    adjacent_to_enemy = {}
    creature_positions = [(c.r, c.c) for c in other_creatures]
    for enemy in targets:
        r, c = enemy.r, enemy.c
        for rr, cc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + rr, c + cc
            if not is_valid(nr, nc, rmax, cmax):
                continue
            if (nr, nc) in terrain:
                continue
            if (nr, nc) in creature_positions:
                continue
            adjacent_to_enemy[(nr, nc)] = (r, c)
    return adjacent_to_enemy

def unit_in_range_of_targets(unit, targets, rmax, cmax, creatures, terrain):
    """Returns True if unit is in range of one its targets."""
    return (unit.r, unit.c) in compute_target_range(targets, rmax, cmax, [c for c in creatures if c != unit], terrain)

def compute_reachable_cells(unit , terrain, creatures, rmax, cmax):
    """Returns a list of cells that are reachable by the unit."""
    blocked_cells = terrain + [(c.r, c.c) for c in creatures if c is not unit]
    wavefront = [(unit.r, unit.c, 0)]
    dist_dict = {}
    while len(wavefront) > 0:
        r, c, dist = wavefront.pop(0)
        for rr, cc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + rr, c + cc
            if (nr, nc) not in blocked_cells and is_valid(nr, nc, rmax, cmax) and (nr, nc) not in dist_dict:
                wavefront.append((nr, nc, dist + 1))
        dist_dict[(r, c)] = dist
    return dist_dict


def move(unit, targets, terrain, creatures, rmax, cmax):
    """Moves the unit if the unit can move towards a target.
    Does nothing if unit is blocked."""
    cells_in_range = compute_target_range(targets, rmax, cmax, [c for c in creatures if c != unit], terrain)
    dist_dict = compute_reachable_cells(unit, terrain, creatures, rmax, cmax)
    reachable_cells = [c for c in cells_in_range if c in dist_dict]
    if len(reachable_cells) == 0:
        # we cannot move
        return
    min_dist = min(dist_dict[c] for c in reachable_cells)
    nearest_cells = [c for c in reachable_cells if dist_dict[c] == min_dist]
    chosen_cell = sorted(nearest_cells)[0]
    # do shortest path backwards and choose the cell with min_dist but in reading order
    backwards = compute_reachable_cells(Creature('none', chosen_cell[0], chosen_cell[1]), terrain, creatures, rmax, cmax)
    possible_steps = [b for b in backwards if b in compute_target_range([unit], rmax, cmax, [c for c in creatures if c != unit], terrain)]
    min_step_dist = min(backwards[c] for c in possible_steps)
    nearest_step_cells = [c for c in possible_steps if backwards[c] == min_step_dist]
    chosen_step = sorted(nearest_step_cells)[0]
    unit.r, unit.c = chosen_step

def render(creatures, terrain, rmax, cmax):
    """Renders the map cells as a string."""
    elves = [(c.r, c.c) for c in creatures if c.creature_type == 'Elf']
    goblins = [(c.r, c.c) for c in creatures if c.creature_type == 'Goblin']

    rows = []
    for r in range(rmax + 1):
        row = ''
        for c in range(cmax + 1):
            cell = (r, c)
            if cell in terrain:
                row += '#'
            elif cell in elves:
                row += 'E'
            elif cell in goblins:
                row += 'G'
            else:
                row += '.'
        rows.append(row)
    return "\n".join(rows)


def adjacent(unit, targets):
    in_range = []
    r, c = unit.r, unit.c
    adj_cells =  [(r + rr, c + cc) for rr, cc in [(1, 0), (-1, 0), (0, 1), (0, -1)]]
    for target in targets:
        if (target.r, target.c) in adj_cells:
            in_range.append(target)
    return in_range


def is_combat_finished(creatures):
    survivor = creatures[0].creature_type
    return all([c.creature_type==survivor for c in creatures])


def run_game(input_fname, debug=False):
    creatures, terrain = load_input(input_fname)
    rmax, cmax = max(terrain, key=lambda item: item[0])[0], max(terrain, key=lambda item: item[1])[1]
    combat_finished = False
    rounds = 0
    snapshots = []
    if debug:
        print(render(creatures, terrain, rmax, cmax))
        snapshots.append((deepcopy(creatures), render(creatures, terrain, rmax, cmax)))

    while not combat_finished:
        creatures = [c for c in creatures if c.hitpoints > 0]
        creatures.sort(key=lambda c: (c.r, c.c))
        for unit in creatures:
            if unit.hitpoints <= 0:
                pass

            # identify targets
            targets = identify_targets(unit, creatures)
            if len(targets) == 0:
                combat_finished = True
                break

            #  move
            if not unit_in_range_of_targets(unit, targets, rmax, cmax, creatures, terrain):
                # the unit will move only if it can
                move(unit, targets, terrain, creatures, rmax, cmax)

            # attack
            in_range = adjacent(unit, targets)
            if len(in_range) > 0:
                target = sorted(in_range, key=lambda u: (u.hitpoints, u.r, u.c))[0]
                target.hitpoints -= unit.attack_power
                if target.hitpoints <= 0:
                    # unit just died
                    creatures.remove(target)


        if not is_combat_finished(creatures):
            rounds += 1
        if debug:
            print(f'game after {rounds} full rounds')
            print(f"{sorted(creatures, key=lambda unit: (unit.r, unit.c))}")
            print(render(creatures, terrain, rmax, cmax))
            snapshots.append((deepcopy(creatures), render(creatures, terrain, rmax, cmax)))
    print(
        f"{rounds} rounds, {sum(c.hitpoints for c in creatures)} hitpoints remaining")
    if debug:
        return snapshots


if __name__ == '__main__':
    """run_game('input15_sample4')
    print('47 rounds, 590 hitpoints remaining expected')
    run_game('input15_combat1')
    print('37 rounds, 982 hitpoints remaining expected')
    run_game('input15_combat2')
    print('46 rounds, 859 hitpoints remaining expected')
    run_game('input15_combat3')
    print('35 rounds, 793 hitpoints remaining expected')
    run_game('input15_combat4')
    print('54 rounds, 536 hitpoints remaining expected')
    run_game('input15_combat5')
    print('20 rounds, 937 hitpoints remaining expected')"""
    run_game('input15')