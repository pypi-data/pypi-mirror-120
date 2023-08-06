"""
"""

def main():
	# todo/fred: replace python __main__ cli with a shell wrapper instead
 import bumpkin

 args = bumpkin.cli_arguments()
 bumpkin.release(args)


if __name__ == "__main__":
 main()
