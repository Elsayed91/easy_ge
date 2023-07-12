import argparse

from easy_ge.main import easy_validation

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run data validation.')
    parser.add_argument('config', type=str, help='Path to the configuration file')

    args = parser.parse_args()

    easy_validation(args.config)
