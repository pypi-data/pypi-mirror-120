"""
"""


def main():
 import argparse
 
 import bumpkin

 parser = argparse.ArgumentParser(description="Standard Bumpkin")

 parser.add_argument("--debug", "-d", default=False, action="store_true")
 parser.add_argument("--dry-run", default=False, action="store_true")

 parser.add_argument("--preview", "-p", default=False, action="store_true")
 parser.add_argument("--no-preview", dest="preview", action="store_false")

 parser.add_argument("--push", default=False, action="store_true")
 parser.add_argument("--no-push", dest="push", action="store_false")

 parser.add_argument("--tag", default=False, action="store_true", help="tag the repo with the version")
 parser.add_argument("--no-tag", dest="tag", action="store_false")

 parser.add_argument("--changelog-filename", "-f", default="CHANGELOG.md")
 parser.add_argument("--changelog", default=False, action="store_true", help="emit a changelog")
 parser.add_argument("--no-changelog", dest="changelog", action="store_false")

 parser.add_argument("--version-filename", default="VERSION")
 parser.add_argument("--version-file", default=False, action="store_true")
 parser.add_argument("--no-version-file", dest="version-file", action="store_false")

 args = parser.parse_args()

 bumpkin.release(args)


if __name__ == "__main__":
 main()
