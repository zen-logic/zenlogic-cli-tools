from ui.app import launch


if __name__ == "__main__":
    import multiprocessing as mp
    mp.freeze_support()
    mp.set_start_method('fork')
    launch(is_async=True)

