
import argparse
import subprocess as sub
import sys


def yesno(msg: str, default: bool = None):
    positive = ["yes", "ye", "y"]
    negative = ["no", "n"]
    while True:
        answer = input(f"{msg} - yes/no:\n")
        if answer == "" and default is not None:
            return default
        elif answer in positive:
            return True
        elif answer in negative:
            return False
        print(f"Please respond with 'yes' or 'no'")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-tests", action="store_true", help="Skip coverage tests."
    )
    parser.add_argument(
        "--skip-checks", action="store_true", help="Skip build checks."
    )
    parser.add_argument(
        "-y", "--yes", action="store_true", help="Skip upload confirmation."
    )

    args = parser.parse_args()

    if not args.skip_tests:
        sub.run(["coverage", "run", "-m", "pytest"]).check_returncode()

    sub.run([sys.executable, "-m", "build"]).check_returncode()

    if not args.skip_checks:
        sub.run([sys.executable, "-m", "twine", "check", "dist/*"]).check_returncode()

    if not args.yes:
        if not yesno(f"All checks passed. Would you like to upload the package?"):
            print("Aborting...")
            return

    sub.run([sys.executable, "-m", "twine", "upload", "dist/*"]).check_returncode()


if __name__ == "__main__":
    main()
