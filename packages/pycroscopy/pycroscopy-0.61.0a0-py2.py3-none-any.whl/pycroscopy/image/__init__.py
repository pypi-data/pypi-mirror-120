"""
Image Module

Should contain
- general feature extraction
- geometry feature extraction
- atom finding
- denoising
- windowing
- transforms (e.g., radon, hough)

Submodules
----------
.. autosummary::
    :toctree: _autosummary

"""

from .image_window import ImageWindowing
__all__ = ['ImageWindowing']

