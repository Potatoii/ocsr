# -*- coding: utf-8 -*-

"""
DECIMER Segmentation Python Package.

Segmentation of chemical structure depictions from scientific literature.


For comments, bug reports or feature requests,
please raise a issue on our Github repository.
"""

__version__ = "1.1.3"

__all__ = [
    "decimer_segmentation",
    "segment_chemical_structures"
]

from .complete_structure import *
from .decimer_segmentation import *
