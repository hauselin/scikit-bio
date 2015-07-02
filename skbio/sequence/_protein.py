# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

import numpy as np

from skbio.util import classproperty, overrides
from ._iupac_sequence import IUPACSequence, _motifs as parent_motifs


class Protein(IUPACSequence):
    """Store protein sequence data and optional associated metadata.

    Only characters in the IUPAC protein character set [1]_ are supported.

    Parameters
    ----------
    sequence : str, Sequence, or 1D np.ndarray (np.uint8 or '\|S1')
        Characters representing the protein sequence itself.
    metadata : dict, optional
        Arbitrary metadata which applies to the entire sequence.
    positional_metadata : Pandas DataFrame consumable, optional
        Arbitrary per-character metadata. For example, quality data from
        sequencing reads. Must be able to be passed directly to the Pandas
        DataFrame constructor.
    validate : bool, optional
        If ``True``, validation will be performed to ensure that all sequence
        characters are in the IUPAC protein character set. If ``False``,
        validation will not be performed. Turning off validation will improve
        runtime performance. If invalid characters are present, however, there
        is **no guarantee that operations performed on the resulting object
        will work or behave as expected.** Only turn off validation if you are
        certain that the sequence characters are valid. To store sequence data
        that is not IUPAC-compliant, use ``Sequence``.
    case_insenstive : bool, optional
        If ``True``, lowercase sequence characters will be converted to
        uppercase characters in order to be valid IUPAC protein characters.

    Attributes
    ----------
    values
    metadata
    positional_metadata
    alphabet
    gap_chars
    nondegenerate_chars
    degenerate_chars
    degenerate_map

    References
    ----------
    .. [1] Nomenclature for incompletely specified bases in nucleic acid
       sequences: recommendations 1984.
       Nucleic Acids Res. May 10, 1985; 13(9): 3021-3030.
       A Cornish-Bowden

    Examples
    --------
    >>> from skbio import Protein
    >>> Protein('PAW')
    Protein
    -----------------------------
    Stats:
        length: 3
        has gaps: False
        has degenerates: False
        has non-degenerates: True
    -----------------------------
    0 PAW

    Convert lowercase characters to uppercase:

    >>> Protein('paW', lowercase=True)
    Protein
    -----------------------------
    Stats:
        length: 3
        has gaps: False
        has degenerates: False
        has non-degenerates: True
    -----------------------------
    0 PAW

    """
    __stop_codes = None

    @classproperty
    def _stop_codes(cls):
        if cls.__stop_codes is None:
            stops = cls.stop_chars
            cls.__stop_codes = np.asarray([ord(s) for s in stops])
        return cls.__stop_codes

    @classproperty
    # TODO figure out why this doesn't work
    #@overrides(IUPACSequence)
    def alphabet(cls):
        return (cls.degenerate_chars | cls.nondegenerate_chars |
                cls.gap_chars | cls.stop_chars)

    @classproperty
    @overrides(IUPACSequence)
    def nondegenerate_chars(cls):
        return set("ACDEFGHIKLMNPQRSTVWY")

    @classproperty
    @overrides(IUPACSequence)
    def degenerate_map(cls):
        return {
            "B": set("DN"), "Z": set("EQ"),
            "X": set("ACDEFGHIKLMNPQRSTVWY")
        }

    @classproperty
    def stop_chars(cls):
        return set('*')

    @property
    def _motifs(self):
        return _motifs

    def stops(self):
        return np.in1d(self._bytes, self._stop_codes)

    def has_stops(self):
        return bool(self.stops().any())


_motifs = parent_motifs.copy()


@_motifs("N-glycosylation")
def _motif_nitro_glycosylation(sequence, min_length, ignore):
    """Identifies N-glycosylation runs"""
    return sequence.find_with_regex("(N[^PX][ST][^PX])", ignore=ignore)

# Leave this at the bottom
_motifs.interpolate(Protein, "find_motifs")
