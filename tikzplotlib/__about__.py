try:
    # Python 3.8
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

try:
    __version__ = metadata.version("tikzplotlib")
except Exception:
    __version__ = "unknown"
