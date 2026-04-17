import collections
import collections.abc
try:
    collections.Sequence = collections.abc.Sequence
except AttributeError: pass
try:
    from pptx import Presentation
    print("python-pptx installed")
except ImportError:
    print("missing python-pptx")
