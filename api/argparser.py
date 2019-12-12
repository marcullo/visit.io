import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', type=str, required=False,
                        help='api key for authorization')
    parser.add_argument('--params', type=str, required=True,
                        help='params file path (see example.json)')
    args = parser.parse_args()

    params_path = Path(args.params)

    if not params_path.is_file():
        raise IOError('Params path not found!')

    return args
