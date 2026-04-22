"""
Tidy JCM materials
=====

Export materials from the tidy3D aterial library for use in other EM solvers
"""

__version__ = "0.1.1"

from .generate import gen_material

__all__ = ['gen_material']
