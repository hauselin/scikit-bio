# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

import unittest

import numpy as np
import numpy.testing as npt

from skbio import Protein


class TestProtein(unittest.TestCase):
    def test_alphabet(self):
        expected = set("ACDEFGHIKLMNPQRSTVWYBZX-.*")
        self.assertIs(type(Protein.alphabet), set)
        self.assertEqual(Protein.alphabet, expected)

        Protein.alphabet.add("JO")
        self.assertEqual(Protein.alphabet, expected)
        self.assertEqual(Protein('').alphabet, expected)

        with self.assertRaises(AttributeError):
            Protein('').alphabet = set("ABCD")

    def test_nondegenerate_chars(self):
        exp = set("ACDEFGHIKLMNPQRSTVWY")
        self.assertEqual(Protein("").nondegenerate_chars, exp)
        self.assertEqual(Protein.nondegenerate_chars, exp)

    def test_degenerate_map(self):
        exp = {
            'B': set(['D', 'N']), 'Z': set(['E', 'Q']),
            'X': set(['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
                      'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'])
        }
        self.assertEqual(Protein("").degenerate_map, exp)
        self.assertEqual(Protein.degenerate_map, exp)

    def test_stop_chars(self):
        expected = set('*')
        self.assertIs(type(Protein.stop_chars), set)
        self.assertEqual(Protein.stop_chars, expected)

        Protein.stop_chars.add("JO")
        self.assertEqual(Protein.stop_chars, expected)
        self.assertEqual(Protein('').stop_chars, expected)

        with self.assertRaises(AttributeError):
            Protein('').stop_chars = set("^&")

    def test_stops(self):
        npt.assert_array_equal(Protein('').stops(), np.array([]))

        npt.assert_array_equal(Protein('P').stops(), np.array([False]))

        npt.assert_array_equal(Protein('PAW').stops(),
                               np.array([False, False, False]))

        npt.assert_array_equal(Protein('PAW*').stops(),
                               np.array([False, False, False, True]))

        npt.assert_array_equal(Protein('P*W*').stops(),
                               np.array([False, True, False, True]))

        npt.assert_array_equal(Protein('****').stops(),
                               np.array([True, True, True, True]))

        npt.assert_array_equal(Protein('XZB-.').stops(),
                               np.array([False, False, False, False, False]))

    def test_has_stops(self):
        self.assertFalse(Protein('').has_stops())
        self.assertFalse(Protein('P').has_stops())
        self.assertFalse(Protein('PAW').has_stops())
        self.assertTrue(Protein('PAW*').has_stops())
        self.assertTrue(Protein('P*W*').has_stops())
        self.assertTrue(Protein('****').has_stops())
        self.assertFalse(Protein('XZB-.').has_stops())

    def test_motif_n_glycosylation(self):
        seq = Protein("ACDFFACGNPSL")
        self.assertEqual(list(seq.find_motifs("N-glycosylation")), [])

        seq = Protein("ACDFNFTACGNPSL")
        self.assertEqual(list(seq.find_motifs("N-glycosylation")),
                         [slice(4, 8)])

        seq = Protein("AC-DFN-FTACGNPSL")
        self.assertEqual(list(seq.find_motifs("N-glycosylation",
                                              ignore=seq.gaps())),
                         [slice(5, 10)])


if __name__ == "__main__":
    unittest.main()
