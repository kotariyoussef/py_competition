import argparse


def main():
    parser = argparse.ArgumentParser(description="Run the app in console or web mode.")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["console", "web"],
        default="web",
        help="Choose the app mode (console or web)."
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8000,
        help="Port number (default: 8000) only on web mode."
    )

    args = parser.parse_args()

    if args.mode == "console":
        print("Running the app in console mode.")
    elif args.mode == "web":
        print(f"Running the app in web mode port {args.port}.")


if __name__ == "__main__":
    main()
