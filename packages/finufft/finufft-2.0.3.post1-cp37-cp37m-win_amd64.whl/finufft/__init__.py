"""The Python interface to FINUFFT is divided into two parts: the simple
interface (through the ``nufft*`` functions) and the more advanced plan
interface (through the ``Plan`` class). The former allows the user to perform
an NUFFT in a single call while the latter allows for more efficient reuse of
resources when the same NUFFT is applied several times to different data by
saving FFTW plans, sorting the nonuniform points, and so on.
"""


""""""  # start delvewheel patch
def _delvewheel_init_patch_0_0_14():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'finufft.libs'))
    if sys.version_info[:2] >= (3, 8):
        if os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')):
            os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE']='1'
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-finufft-2.0.3.post1')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_14()
del _delvewheel_init_patch_0_0_14
# end delvewheel patch



# that was the docstring for the package finufft.

__all__ = ["nufft1d1","nufft1d2","nufft1d3","nufft2d1","nufft2d2","nufft2d3","nufft3d1","nufft3d2","nufft3d3","Plan"]
# etc..

# let's just get guru and nufft1d1 working first...
from finufft._interfaces import Plan
from finufft._interfaces import nufft1d1,nufft1d2,nufft1d3
from finufft._interfaces import nufft2d1,nufft2d2,nufft2d3
from finufft._interfaces import nufft3d1,nufft3d2,nufft3d3