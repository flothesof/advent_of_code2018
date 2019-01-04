def load_sample_input():
    scores = [3, 7]
    elves = [0, 1]
    return scores, elves


def new_scores(scores, elves):
    digits = [scores[elve] for elve in elves]
    return list(int(item) for item in str(sum(digits)))


def move_elves(scores, elves):
    moved = []
    for ind, elve in enumerate(elves):
        elve = (elve + scores[elve] + 1) % len(scores)
        moved.append(elve)
    return moved


def solve14_part2(inputstr):
    target = list(map(int, inputstr))
    scores, elves = load_sample_input()
    scores = list(scores)
    count = 2
    last_recipes_match = False
    while not last_recipes_match:
        new = new_scores(scores, elves)
        for recipe in new:
            scores.append(recipe)
            count += 1
            if len(scores) >= len(target):
                last = [scores[-1 - i] for i in range(len(target))][::-1]
                if last == target:
                    last_recipes_match = True
                    break
        elves = move_elves(scores, elves)
    return count - len(target)


if __name__ == '__main__':
    print(solve14_part2('51589'))
    print(solve14_part2('01245'))
    print(solve14_part2('92510'))
    print(solve14_part2('59414'))
    print(solve14_part2('598701'))