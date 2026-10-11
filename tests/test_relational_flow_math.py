import unittest
from tools.relational_flow_math import balance, conductance_rate, pressure_rate, interval_direction, cycle_component


class FlowMathTests(unittest.TestCase):
    def test_path_change_with_same_potential(self):
        self.assertEqual(conductance_rate(2, 4, 1), 6)
        self.assertEqual(conductance_rate(1, 4, 1), 3)

    def test_pressure_accumulates_without_new_forcing(self):
        self.assertEqual(pressure_rate(2 - 1, 2), .5)

    def test_blocked_pipe_is_not_backflow(self):
        self.assertEqual(conductance_rate(0, 1, 8), 0)
        self.assertEqual(interval_direction(0, 0), 'ZERO_NET_TRANSFER')

    def test_reversed_gradient(self):
        self.assertEqual(conductance_rate(2, 1, 4), -6)

    def test_uncertain_sign_is_not_negative(self):
        self.assertEqual(interval_direction(-3, 1), 'UNRESOLVED_SIGN')
        self.assertEqual(interval_direction(-3, -1), 'BACKFLOW')
        self.assertEqual(interval_direction(1, 3), 'FORWARD')

    def test_invalid_measurements(self):
        for bad in (None, float('nan'), float('inf'), True):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                interval_direction(bad, 1)
        with self.assertRaises(ValueError):
            interval_direction(3, 1)
        with self.assertRaises(ValueError):
            pressure_rate(1, 0)
        with self.assertRaises(ValueError):
            conductance_rate(-1, 2, 1)

    def test_interval_conservation_and_drain(self):
        e = [{'id':'ab', 'source':'a', 'target':'b', 'amount':3, 'provenance':'obs1'}]
        self.assertEqual(balance(['a','b'], e, {'a':5,'b':0}, {'a':2,'b':2},
            {'a':0,'b':0}, {'a':0,'b':1}, {'a':0,'b':0}), {'a':0,'b':0})

    def test_missing_stock_rejected(self):
        with self.assertRaises(ValueError):
            balance(['a'], [], {}, {'a':0}, {'a':0}, {'a':0}, {'a':0})

    def test_copy_requires_transformation(self):
        self.assertEqual(balance(['a'], [], {'a':1}, {'a':2}, {'a':0}, {'a':0}, {'a':1}), {'a':0})
        self.assertEqual(balance(['a'], [], {'a':1}, {'a':2}, {'a':0}, {'a':0}, {'a':0}), {'a':1})

    def cycle(self):
        return [{'id':'ab','source':'a','target':'b','amount':2,'provenance':'obs1'},
                {'id':'bc','source':'b','target':'c','amount':1,'provenance':'obs2'},
                {'id':'ca','source':'c','target':'a','amount':3,'provenance':'obs3'}]

    def test_cycle_is_not_vortex_or_item_identity(self):
        r = cycle_component(self.cycle(), [('ab',1),('bc',1),('ca',1)])
        self.assertEqual(r['common_interval_amount'], 1)
        self.assertEqual(r['residuals'], {'ab':1,'bc':0,'ca':2})
        self.assertEqual(r['physical_vortex'], 'NOT_ESTABLISHED')
        self.assertEqual(r['same_item_return'], 'NOT_ESTABLISHED')

    def test_circulation_without_accumulation(self):
        e = self.cycle()
        for x in e: x['amount'] = 1
        z = dict.fromkeys(['a','b','c'], 0)
        self.assertEqual(balance(list(z), e, z, z, z, z, z), z)

    def test_open_path_is_not_cycle(self):
        with self.assertRaises(ValueError):
            cycle_component(self.cycle(), [('ab',1),('bc',1)])

    def test_lineage_cannot_be_omitted(self):
        e = self.cycle(); e[0]['provenance'] = ''
        with self.assertRaises(ValueError):
            cycle_component(e, [('ab',1),('bc',1),('ca',1)])

    def test_negative_orientation_cycle(self):
        e = self.cycle()
        for x in e: x['amount'] = -1
        r = cycle_component(e, [('ca',-1),('bc',-1),('ab',-1)])
        self.assertEqual(r['common_interval_amount'], 1)

    def test_no_inevitable_pressure_rise(self):
        self.assertEqual(pressure_rate(2-2, 2), 0)


if __name__ == '__main__':
    unittest.main()
