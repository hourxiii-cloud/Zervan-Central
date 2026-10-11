"""Scoped interval transport arithmetic; does not certify physical mechanisms."""
import math


def finite(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('expected a finite measured/model number; unknown is not zero')
    return value


def conductance_rate(k, source_p, target_p):
    if finite(k) < 0:
        raise ValueError('negative conductance outside this model')
    return k * (finite(source_p) - finite(target_p))


def pressure_rate(net_rate, capacitance):
    if finite(capacitance) <= 0:
        raise ValueError('positive constant capacitance required')
    return finite(net_rate) / capacitance


def interval_direction(low, high):
    low, high = finite(low), finite(high)
    if low > high:
        raise ValueError('reversed uncertainty bounds')
    if high < 0:
        return 'BACKFLOW'
    if low > 0:
        return 'FORWARD'
    if low == high == 0:
        return 'ZERO_NET_TRANSFER'
    return 'UNRESOLVED_SIGN'


def balance(nodes, edges, start, end, additions, removals, transformations):
    """Compute residuals using interval totals in one declared common unit."""
    if not nodes or len(set(nodes)) != len(nodes):
        raise ValueError('distinct nonempty nodes required')
    inventories = (start, end, additions, removals, transformations)
    if any(set(x) != set(nodes) for x in inventories):
        raise ValueError('every node needs explicit observations, including zeros')
    for x in inventories:
        for v in x.values():
            finite(v)
    if any(v < 0 for x in (start, end, additions, removals) for v in x.values()):
        raise ValueError('negative inventory/addition/removal outside this model')
    net = {n: additions[n] - removals[n] + transformations[n] for n in nodes}
    ids = set()
    for e in edges:
        if e['id'] in ids or e['source'] not in net or e['target'] not in net:
            raise ValueError('duplicate edge or unknown endpoint')
        ids.add(e['id'])
        amount = finite(e['amount'])
        if not e.get('provenance'):
            raise ValueError('transfer lineage required')
        net[e['source']] -= amount
        net[e['target']] += amount
    return {n: end[n] - start[n] - net[n] for n in nodes}


def cycle_component(edges, traversal):
    """Check a declared simple oriented cycle; aggregate totals only."""
    by_id = {e['id']: e for e in edges}
    if len(by_id) != len(edges) or len(traversal) < 2:
        raise ValueError('unique edges and a nontrivial cycle required')
    ids = [edge_id for edge_id, _ in traversal]
    if len(set(ids)) != len(ids):
        raise ValueError('cycle must not reuse an edge')
    legs = []
    for edge_id, sign in traversal:
        if isinstance(sign, bool) or sign not in (-1, 1) or edge_id not in by_id:
            raise ValueError('known edge and orientation +/-1 required')
        e = by_id[edge_id]
        if not e.get('provenance'):
            raise ValueError('transfer lineage required')
        amount = finite(e['amount']) * sign
        if amount <= 0:
            raise ValueError('cycle direction not supported by positive transfer')
        source, target = (e['source'], e['target']) if sign == 1 else (e['target'], e['source'])
        if source == target:
            raise ValueError('self-loop requires a separate item/transform model')
        legs.append((source, target, amount))
    if len({x[0] for x in legs}) != len(legs) or any(
            leg[1] != legs[(i+1) % len(legs)][0] for i, leg in enumerate(legs)):
        raise ValueError('traversal is not a simple closed oriented cycle')
    amount = min(x[2] for x in legs)
    return {'common_interval_amount': amount,
            'residuals': {eid: by_id[eid]['amount'] - sign * amount for eid, sign in traversal},
            'standing': 'AGGREGATE_CYCLE_COMPONENT_ONLY',
            'physical_vortex': 'NOT_ESTABLISHED',
            'same_item_return': 'NOT_ESTABLISHED'}
