import llist

def simulate(last_marble, nplayers):
    players = list(range(1, nplayers+1))
    scores = {player: 0 for player in players}
    current_marble = 0
    current_pos = 0
    current_player_index = -1
    circle = [0]
    while current_marble < last_marble:
        current_marble += 1
        current_player_index = (current_player_index + 1) % nplayers
        if not current_marble % 23 == 0:
            if len(circle) > 1:
                n = (current_pos + 1) % len(circle)
                nn = (current_pos + 2) % len(circle)
                # append at the end
                if n > nn:
                    circle.append(current_marble)
                    current_pos = n + 1
                # insert
                else:
                    circle.insert(nn, current_marble)
                    current_pos = nn
            else:
                circle.append(current_marble)
                current_pos += 1
        else:
            pop = circle.pop(current_pos - 7)
            scores[players[current_player_index]] += current_marble + pop
            current_pos = current_pos - 7
            if current_pos < 0:
                current_pos += len(circle) + 1
    return scores

def simulate2(last_marble, nplayers):
    players = list(range(1, nplayers+1))
    scores = {player: 0 for player in players}
    current_marble = 0

    current_player_index = -1
    circle = llist.dllist([0])
    current_pos = circle.first
    while current_marble < last_marble:
        current_marble += 1
        current_player_index = (current_player_index + 1) % nplayers
        if not current_marble % 23 == 0:
            if len(circle) > 1:
                n = current_pos.next
                if n is None:
                    n = circle.first
                nn = n.next
                if nn is None:
                    # append at the end
                    current_pos = circle.append(current_marble)
                else:
                    # insert
                    current_pos = circle.insert(current_marble, nn)
            else:
                circle.append(current_marble)
                current_pos = current_pos.next
        else:
            for _ in range(6):
                current_pos = current_pos.prev
                if current_pos is None:
                    current_pos = circle.last
            if current_pos.prev is not None:
                pop = circle.remove(current_pos.prev)
            else:
                pop = circle.remove(circle.last)
            scores[players[current_player_index]] += current_marble + pop
    return scores

if __name__ == '__main__':
    score = simulate2(25, nplayers=9)
    print(max(score.values()))
    score = simulate2(1618, nplayers=10)
    print(max(score.values()))
    score = simulate2(7999, nplayers=13)
    print(max(score.values()))
    score = simulate2(1104, nplayers=17)
    print(max(score.values()))
    score = simulate2(6111, nplayers=21)
    print(max(score.values()))
    score = simulate2(5807, nplayers=30)
    print(max(score.values()))

    # my input
    score = simulate2(70950, nplayers=431)
    print(max(score.values()))

    # my input for part 2
    score = simulate2(7095000, nplayers=431)
    print(max(score.values()))