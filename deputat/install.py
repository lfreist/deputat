try:
    from deputat import settings
except ImportError:
    import settings

def install():
    platform = settings.get_os()
