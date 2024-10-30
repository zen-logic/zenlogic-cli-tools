
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog='fh',
        # description='What the program does',
        usage='%(prog)s [options]'
    )

    parser.add_argument('command')
    args = parser.parse_args()
    print (args.command)


