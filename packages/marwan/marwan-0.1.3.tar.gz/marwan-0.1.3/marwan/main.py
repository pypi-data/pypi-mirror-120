import webbrowser
import argparse
import sys
from typing import Optional, Sequence

websites = {
    "github": "https://www.github.com/marwanhawari",
    "linkedin": "https://www.linkedin.com/in/marwanhawari/",
    "pypi": "https://pypi.org/user/marwanhawari/",
    "website": "https://www.marwanhawari.com/",
}


def open_websites(args: argparse.Namespace) -> int:
    for arg, input in vars(args).items():
        if input and arg != "repo":
            print(f"Opening {websites[arg]}")
            webbrowser.open(websites[arg])
        elif input is not None and arg == "repo":
            print(f"Opening {websites['github']}/{input}")
            webbrowser.open(f"{websites['github']}/{input}")

    return 0


def main(argv: Optional[Sequence] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g",
        "--github",
        dest="repo",
        nargs="?",
        const="",
        help="""Open my GitHub page.
        You can specify the repository or leave empty for my homepage.""",
    )
    parser.add_argument(
        "-l",
        "--linkedin",
        dest="linkedin",
        action="store_true",
        help="Open my LinkedIn page.",
    )
    parser.add_argument(
        "-p",
        "--pypi",
        dest="pypi",
        action="store_true",
        help="Open my PyPI page.",
    )
    parser.add_argument(
        "-w",
        "--website",
        dest="website",
        action="store_true",
        help="Open my personal website.",
    )
    args = parser.parse_args(argv)

    open_websites(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
