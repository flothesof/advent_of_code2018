from collections import namedtuple

Node = namedtuple('Node', 'children metadata')

def parse(subtree):
    nchildren = subtree[0]
    nmeta = subtree[1]
    if nchildren == 0:
        metadata = subtree[2:2+nmeta]
        remainder = subtree[2+nmeta:]
        return Node([], metadata), remainder
    else:
        parent = Node([], [])
        remainder = subtree[2:]
        while True:
            node, remainder = parse(remainder)
            parent.children.append(node)
            if len(parent.children) == nchildren:
                parent.metadata.extend(remainder[:nmeta])
                remainder = remainder[nmeta:]
                break
        return parent, remainder

def sum_metadata(node, partial_sum=0):
    """Part 1 of the puzzle."""
    partial_sum += sum(node.metadata)
    for child in node.children:
        partial_sum += sum_metadata(child)
    return partial_sum

def compute_value(node):
    """Part 2 of the puzzle."""
    if len(node.children) == 0:
        return sum(node.metadata)
    else:
        value = 0
        valid_metadata = [child_index for child_index in node.metadata \
                          if child_index > 0 if child_index <= len(node.children)]
        for child_index in valid_metadata:
            value += compute_value(node.children[child_index - 1])
        return value

if __name__ == '__main__':
    sample = [int(item) for item in '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split()]
    full_input = [int(item) for item in open('input08').readlines()[0].split()]
    # sample part 1
    root, _ = parse(sample)
    total = sum_metadata(root)
    print(total)

    # full part 1
    root, _ = parse(full_input)
    total = sum_metadata(root)
    print(total)

    # sample part 2
    root, _ = parse(sample)
    value = compute_value(root)
    print(value)

    # full part 2
    root, _ = parse(full_input)
    value = compute_value(root)
    print(value)
