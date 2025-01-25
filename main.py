import argparse
from console.main import main as console_main
from web.main import run as web_main


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
        console_main()
    elif args.mode == "web":
        print(f"Running the app in web mode port {args.port}.")
        web_main(args.port)


if __name__ == "__main__":
    main()