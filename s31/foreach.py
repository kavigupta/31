import itertools
import csv

MAX_FOREACHES = 9


def parse_foreach_args(args):
    foreach = []
    if args.foreach is not None:
        foreach += args.foreach
    for k in range(2, 1 + MAX_FOREACHES):
        foreach_k = getattr(args, "foreach_{}".format(k))
        if foreach_k is not None:
            foreach += foreach_k
    return parse_foreach_statements(foreach)


def parse_foreach_statements(foreach):
    all_assigns = [
        list(itertools.chain(*x))
        for x in itertools.product(
            *[parse_foreach_statement(statement) for statement in foreach]
        )
    ]
    return all_assigns


def parse_foreach_statement(statement):
    assert statement, "must provide at least one element"
    assert len(statement) % 2 == 0, "must provide an even number of elements"
    k = len(statement) // 2
    variables = statement[:k]
    values = statement[k:]
    values = [parse_values(v) for v in values]
    for v in values:
        if len(v) != len(values[0]):
            raise RuntimeError(
                "Values must be the same length but have lengths of {} ({!r}) vs {} ({!r})".format(
                    len(values[0]), values[0], len(v), v
                )
            )
    return [
        [(variable, v) for variable, v in zip(variables, vals)]
        for vals in list(zip(*values))
    ]


def parse_values(values):
    return list(csv.reader([values]))[0]
