try:
    from deputat import run
except ImportError:
    import run

if __name__ == '__main__':
    run.run_gui()
