
from .serve import Serve


def main(model_path, outside_function={}):
    Serve(model_path, outside_function)


if __name__ == '__main__':
    main()
