
import glob
import os

# Bu qovluqdakı bütün .py faylları tapılır (init.py istisna olmaqla)
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))

__all__ = [
    os.path.basename(f)[:-3]
    for f in modules
    if os.path.isfile(f) and not f.endswith("__init__.py")
]

# Hər faylı import et
for module in __all__:
    __import__(f"{__name__}.{module}")
