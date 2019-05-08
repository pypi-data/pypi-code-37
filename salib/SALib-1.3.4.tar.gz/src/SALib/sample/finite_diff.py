from __future__ import division

import numpy as np

from . import common_args
from . import sobol_sequence
from ..util import scale_samples, read_param_file


# Generate matrix of samples for derivative-based global sensitivity measure (dgsm)
# start from a QMC (sobol) sequence and finite difference with delta % steps
def sample(problem, N, delta=0.01, seed=None):
    if seed:
        np.random.seed(seed)

    D = problem['num_vars']

    # How many values of the Sobol sequence to skip
    skip_values = 1000

    # Create base sequence - could be any type of sampling
    base_sequence = sobol_sequence.sample(N + skip_values, D)
    # scale before finite differencing
    scale_samples(base_sequence, problem['bounds'])
    dgsm_sequence = np.zeros([N * (D + 1), D])

    index = 0

    for i in range(skip_values, N + skip_values):

        # Copy the initial point
        dgsm_sequence[index, :] = base_sequence[i, :]
        index += 1

        for j in range(D):
            temp = np.zeros(D)
            temp[j] = base_sequence[i, j] * delta
            dgsm_sequence[index, :] = base_sequence[i, :] + temp
            dgsm_sequence[index, j] = min(
                dgsm_sequence[index, j], problem['bounds'][j][1])
            dgsm_sequence[index, j] = max(
                dgsm_sequence[index, j], problem['bounds'][j][0])
            index += 1

    return dgsm_sequence


def cli_parse(parser):
    """Add method specific options to CLI parser.

    Parameters
    ----------
    parser : argparse object

    Returns
    ----------
    Updated argparse object
    """
    parser.add_argument('-d', '--delta', type=float,
                        required=False, default=0.01,
                        help='Finite difference step size (percent)')
    parser.add_argument('-n', '--samples', type=int,
                        required=True, help='Number of Samples')
    return parser


def cli_action(args):
    """Run sampling method

    Parameters
    ----------
    args : argparse namespace
    """
    problem = read_param_file(args.paramfile)
    param_values = sample(problem, args.samples, args.delta, seed=args.seed)
    np.savetxt(args.output, param_values, delimiter=args.delimiter,
               fmt='%.' + str(args.precision) + 'e')


if __name__ == "__main__":
    common_args.run_cli(cli_parse, cli_action)
