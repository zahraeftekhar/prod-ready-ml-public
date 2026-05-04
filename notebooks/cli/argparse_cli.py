"""CLI using argparse."""

import argparse


def say_hi(name):
    print(f"Hello {name}")


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description="CLI using argparse",
    )

    # Required positional argument
    parser.add_argument("name", type=str, help="Name")

    # Parse arguments
    args = parser.parse_args()

    # Call the main function
    say_hi(
        name=args.name,
    )


if __name__ == "__main__":
    main()
