import getpass
import json
import numbers
import numpy as np
import pandas as pd
import tarfile
import tempfile
import socket

from ase import Atoms
from ase.io import Trajectory
from ase.io import write as ase_write, read as ase_read
from collections import OrderedDict
from datetime import datetime
from typing import BinaryIO, Dict, List, TextIO, Tuple, Union
from icet import __version__ as icet_version
from .data_analysis import analyze_data
from .observers.base_observer import BaseObserver


class Int64Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


class DataContainer:
    """
    Data container for storing information concerned with
    Monte Carlo simulations performed with mchammer.

    Parameters
    ----------
    atoms : ASE Atoms object
        reference atomic structure associated with the data container

    ensemble_parameters : dict
        parameters associated with the underlying ensemble

    metadata : dict
        metadata associated with the data container
    """

    def __init__(self, atoms: Atoms, ensemble_parameters: dict,
                 metadata: dict = OrderedDict()):
        """
        Initializes a DataContainer object.
        """
        if not isinstance(atoms, Atoms):
            raise TypeError('atoms is not an ASE Atoms object')

        self.atoms = atoms.copy()
        self._ensemble_parameters = ensemble_parameters
        self._metadata = metadata
        self._add_default_metadata()
        self._last_state = {}

        self._observables = set()
        self._data_list = []

    def append(self, mctrial: int,
               record: Dict[str, Union[int, float, list]]):
        """
        Appends data to data container.

        Parameters
        ----------
        mctrial
            current Monte Carlo trial step
        record
            dictionary of tag-value pairs representing observations

        Raises
        ------
        TypeError
            if input parameters have the wrong type

        """
        if not isinstance(mctrial, numbers.Integral):
            raise TypeError('mctrial has the wrong type: {}'
                            .format(type(mctrial)))

        if self._data_list:
            if self._data_list[-1]['mctrial'] > mctrial:
                raise ValueError('mctrial values should be given in ascending'
                                 ' order. This error can for example occur'
                                 ' when trying to append to an existing data'
                                 ' container after having reset the time step.'
                                 ' Note that the latter happens automatically'
                                 ' when initializing a new ensemble.')

        if not isinstance(record, dict):
            raise TypeError('record has the wrong type: {}'
                            .format(type(record)))

        for tag in record.keys():
            self._observables.add(tag)

        row_data = OrderedDict()
        row_data['mctrial'] = mctrial
        row_data.update(record)
        self._data_list.append(row_data)

    def _update_last_state(self, last_step: int, occupations: List[int],
                           accepted_trials: int, random_state: tuple):
        """Updates last state of the simulation: last step, occupation vector
        and number of accepted trial steps.

        Parameters
        ----------
        last_step
            last trial step
        occupations
            occupation vector observed during the last trial step
        accepted_trial
            number of current accepted trial steps
        random_state
            tuple representing the last state of the random generator
        """
        self._last_state['last_step'] = last_step
        self._last_state['occupations'] = occupations
        self._last_state['accepted_trials'] = accepted_trials
        self._last_state['random_state'] = random_state

    def update_from_observer(self, observer: BaseObserver):
        """ Adds observer data from observer to data container.

        The observer will only be run for the mctrials for which the
        trajectory have been saved.

        The interval of the observer is ignored.

        Parameters
        ----------
        observer
            observer to be used
        """
        for row_data in self._data_list:
            if 'occupations' in row_data:
                atoms = self.atoms.copy()
                atoms.numbers = row_data['occupations']
                record = {observer.tag: observer.get_observable(atoms)}
                row_data.update(record)
                self._observables.add(observer.tag)

    def get_data(self, *tags,
                 start: int = None,
                 stop: int = None,
                 interval: int = 1,
                 fill_method: str = 'skip_none',
                 apply_to: List[str] = None) \
            -> Union[np.ndarray, List[Atoms], Tuple[np.ndarray, List[Atoms]]]:
        """Returns the accumulated data for the requested observables.

        Parameters
        ----------
        tags
            tuples of the requested properties

        start
            minimum value of trial step to consider; by default the
            smallest value in the mctrial column will be used.

        stop
            maximum value of trial step to consider; by default the
            largest value in the mctrial column will be used.

        interval
            increment for mctrial; by default the smallest available
            interval will be used.

        fill_method : {'skip_none', 'fill_backward', 'fill_forward',
                       'linear_interpolate', None}
            method employed for dealing with missing values; by default
            uses 'skip_none'.

        apply_to
            tags of columns for which fill_method will be employed;
            by default parse all columns with fill_method.

        Raises
        ------
        ValueError
            if tags is empty
        ValueError
            if observables are requested that are not in data container
        ValueError
            if fill method is unknown
        ValueError
            if trajectory is requested and fill method is not skip_none
        """
        fill_methods = ['skip_none',
                        'fill_backward',
                        'fill_forward',
                        'linear_interpolate']

        if len(tags) == 0:
            raise TypeError('Missing tags argument')

        if 'trajectory' in tags:
            if fill_method != 'skip_none':
                raise ValueError('Only skip_none fill method is avaliable'
                                 ' when trajectory is requested')
            return self._get_trajectory(*tags, start=start, stop=stop,
                                        interval=interval)

        for tag in tags:
            if tag == 'mctrial':
                continue
            if tag not in self.observables:
                raise ValueError('No observable named {} in data'
                                 ' container'.format(tag))

        mctrials = [row_dict['mctrial'] for row_dict in self._data_list]
        data = pd.DataFrame.from_records(self._data_list,
                                         index=mctrials,
                                         columns=tags)
        if start is None and stop is None:
            data = data.loc[::interval, tags].copy()
        else:
            # slice and pass a copy to avoid slowing down dropna method below
            if start is None:
                data = data.loc[:stop:interval, tags].copy()
            elif stop is None:
                data = data.loc[start::interval, tags].copy()
            else:
                data = data.loc[start:stop:interval, tags].copy()

        if fill_method is not None:
            if fill_method not in fill_methods:
                raise ValueError('Unknown fill method: {}'
                                 .format(fill_method))

            if apply_to is None:
                apply_to = tags

            # retrieve only valid observations
            if fill_method == 'skip_none':
                data.dropna(inplace=True, subset=apply_to)

            else:
                # if requested, drop NaN values in columns
                subset = [tag for tag in tags if tag not in apply_to]
                data.dropna(inplace=True, subset=subset)

                # fill NaN with the next valid observation
                if fill_method == 'fill_backward':
                    data.fillna(method='bfill', inplace=True)

                # fill NaN with the last valid observation
                elif fill_method == 'fill_forward':
                    data.fillna(method='ffill', inplace=True)

                # fill NaN with the linear interpolation of the last and
                # next valid observations
                elif fill_method == 'linear_interpolate':
                    data.interpolate(limit_area='inside', inplace=True)

                # drop any left-over nan values
                data.dropna(inplace=True)

        data_list = []
        for tag in tags:
            # convert NaN to None
            data_list.append(np.array(
                [None if np.isnan(x).any() else x for x in data[tag]]))
        if len(tags) > 1:
            # return a tuple if more than one tag is given
            return tuple(data_list)
        else:
            # return a list if only one tag is given
            return data_list[0]

    @property
    def data(self) -> pd.DataFrame:
        """ pandas data frame (see :class:`pandas.DataFrame`) """
        if self._data_list:
            df = pd.DataFrame.from_records(self._data_list, index='mctrial',
                                           exclude=['occupations'])
            df.dropna(axis='index', how='all', inplace=True)
            df.reset_index(inplace=True)
            return df
        else:
            return pd.DataFrame()

    @property
    def ensemble_parameters(self) -> dict:
        """ parameters associated with Monte Carlo simulation """
        return self._ensemble_parameters.copy()

    @property
    def observables(self) -> List[str]:
        """ observable names """
        return list(self._observables)

    @property
    def metadata(self) -> dict:
        """ metadata associated with data container """
        return self._metadata

    @property
    def last_state(self) -> Dict[str, Union[int, List[int]]]:
        """ last state to be used to restart Monte Carlo simulation """
        return self._last_state

    def reset(self):
        """ Resets (clears) internal data list of data container. """
        self._data_list.clear()
        self._observables.clear()

    def get_number_of_entries(self, tag: str = None) -> int:
        """
        Returns the total number of entries with the given observable tag.

        Parameters
        ----------
        tag
            name of observable; by default the total number of rows in the
            data frame will be returned.

        Raises
        ------
        ValueError
            if observable is requested that is not in data container
        """
        data = pd.DataFrame.from_records(self._data_list)
        if tag is None:
            return len(data)
        else:
            if tag not in data:
                raise ValueError('No observable named {}'
                                 ' in data container'.format(tag))
            return data[tag].count()

    def analyze_data(self, tag: str, start: int = None,
                     stop: int = None, max_lag: int = None) -> dict:
        """
        Returns detailed analysis of a scalar observerable.

        Parameters
        ----------
        tag
            tag of field over which to average
        start
            minimum value of trial step to consider; by default the
            smallest value in the mctrial column will be used.
        stop
            maximum value of trial step to consider; by default the
            largest value in the mctrial column will be used.
        max_lag
            maximum lag between two points in data series, by default the
            largest length of the data series will be used.
            Used for computing autocorrelation
        Raises
        ------
        ValueError
            if observable is requested that is not in data container
        ValueError
            if observable is not scalar
        ValueError
            if observations is not evenly spaced

        Returns
        -------
        dict
            calculated properties of the data including mean,
            standard_deviation, correlation_length and error_estimate
            (95% confidence)
        """
        if tag in ['trajectory', 'occupations']:
            raise ValueError('{} is not scalar'.format(tag))
        steps, data = self.get_data('mctrial', tag, start=start, stop=stop)

        # check that steps are evenly spaced
        diff = np.diff(steps)
        step_length = diff[0]
        if not np.allclose(step_length, diff):
            raise ValueError('data records must be evenly spaced.')

        summary = analyze_data(data, max_lag=max_lag)
        summary['correlation_length'] *= step_length  # in mc-trials
        return summary

    def get_average(self, tag: str,
                    start: int = None, stop: int = None) -> float:
        """
        Returns average of a scalar observable.

        Parameters
        ----------
        tag
            tag of field over which to average
        start
            minimum value of trial step to consider; by default the
            smallest value in the mctrial column will be used.
        stop
            maximum value of trial step to consider; by default the
            largest value in the mctrial column will be used.

        Raises
        ------
        ValueError
            if observable is requested that is not in data container
        ValueError
            if observable is not scalar
        """
        if tag in ['trajectory', 'occupations']:
            raise ValueError('{} is not scalar'.format(tag))
        data = self.get_data(tag, start=start, stop=stop)
        return np.mean(data)

    def _get_trajectory(self, *tags, start: int = None, stop: int = None,
                        interval: int = 1) \
            -> Union[List[Atoms], Tuple[List[Atoms], np.ndarray]]:
        """
        Returns a trajectory in the form of a list of ASE Atoms
        along with the corresponding values of the mctrial and/or scalar
        properties upon request.
        Configurations with non properties will be
        skipped in the trajectory if the property is requested.

        Parameters
        ----------
        start
            minimum value of trial step to consider; by default the
            smallest value in the mctrial column will be used.
        stop
            maximum value of trial step to consider; by default the
            largest value in the mctrial column will be used.
        interval
            increment for mctrial; by default the smallest available
            interval will be used.
        """
        new_tags = tuple(['occupations' if tag == 'trajectory' else
                          tag for tag in tags])
        data = \
            self.get_data(*new_tags, start=start, stop=stop, interval=interval)

        if len(tags) > 1:
            data_list = list(data)
        else:
            data_list = [data]

        tag_list = list(new_tags)
        atoms_list = []
        for tag, data_row in zip(tag_list, data_list):
            if tag == 'occupations':
                ind = tag_list.index('occupations')
                for occupation_vector in data_row:
                    atoms = self.atoms.copy()
                    atoms.numbers = occupation_vector
                    atoms_list.append(atoms)
                data_list[ind] = atoms_list

        if len(data_list) > 1:
            return tuple(data_list)
        else:
            return data_list[0]

    def write_trajectory(self, outfile: Union[str, BinaryIO, TextIO]) -> None:
        """Writes the configurations along the trajectory to file in ASE
        trajectory format.  The file also includes the respectives
        values of the potential for each configuration. If the file
        exists the trajectory will be appended. The ASE `convert`
        command can be used to convert the trajectory file to other
        formats. The ASE `gui` can be used to visualize the
        trajectory.

        Parameters
        ----------
        outfile
            output file name or file object
        """
        atoms_list, energies = self._get_trajectory('occupations', 'potential')
        traj = Trajectory(outfile, mode='a')
        for atoms, energy in zip(atoms_list, energies):
            traj.write(atoms=atoms, energy=energy)
        traj.close()

    @staticmethod
    def read(infile: Union[str, BinaryIO, TextIO], old_format: bool = False):
        """
        Reads DataContainer object from file.

        Parameters
        ----------
        infile
            file from which to read
        old_format
            If true use old json format to read runtime data; default to false

        Raises
        ------
        FileNotFoundError
            if file is not found (str)
        ValueError
            if file is of incorrect type (not a tarball)
        """
        if isinstance(infile, str):
            filename = infile
        else:
            filename = infile.name

        if not tarfile.is_tarfile(filename):
            raise TypeError('{} is not a tar file'.format(filename))

        reference_atoms_file = tempfile.NamedTemporaryFile()
        reference_data_file = tempfile.NamedTemporaryFile()
        runtime_data_file = tempfile.NamedTemporaryFile()

        with tarfile.open(mode='r', name=filename) as tar_file:
            # file with atoms
            reference_atoms_file.write(tar_file.extractfile('atoms').read())

            reference_atoms_file.seek(0)
            atoms = ase_read(reference_atoms_file.name, format='json')

            # file with reference data
            reference_data_file.write(
                tar_file.extractfile('reference_data').read())
            reference_data_file.seek(0)
            with open(reference_data_file.name, encoding='utf-8') as fd:
                reference_data = json.load(fd)

            # init DataContainer
            dc = \
                DataContainer(atoms=atoms,
                              ensemble_parameters=reference_data['parameters'])

            # overwrite metadata
            dc._metadata = reference_data['metadata']

            for tag, value in reference_data['last_state'].items():
                if tag == 'random_state':
                    value = \
                        tuple(tuple(x) if isinstance(x, list)
                              else x for x in value)
                dc._last_state[tag] = value

            # add runtime data from file
            runtime_data_file.write(
                tar_file.extractfile('runtime_data').read())
            runtime_data_file.seek(0)
            if old_format:
                runtime_data = pd.read_json(runtime_data_file)
                data = runtime_data.sort_index(ascending=True)
                dc._data_list = \
                    data.T.apply(lambda x: x.dropna().to_dict()).tolist()
            else:
                dc._data_list = np.load(runtime_data_file, allow_pickle=True)['arr_0'].tolist()

        dc._observables = set([key for data in dc._data_list for key in data])
        dc._observables = dc._observables - {'mctrial'}

        return dc

    def _write(self, outfile: Union[str, BinaryIO, TextIO]):
        """
        Writes DataContainer object to file.

        Parameters
        ----------
        outfile
            file to which to write
        """
        self._metadata['date_last_backup'] = \
            datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        # Save reference atomic structure
        reference_atoms_file = tempfile.NamedTemporaryFile()
        ase_write(reference_atoms_file.name, self.atoms, format='json')

        # Save reference data
        reference_data = {'parameters': self._ensemble_parameters,
                          'metadata': self._metadata,
                          'last_state': self._last_state}

        reference_data_file = tempfile.NamedTemporaryFile()
        with open(reference_data_file.name, 'w') as handle:
            json.dump(reference_data, handle, cls=Int64Encoder)

        # Save runtime data
        runtime_data_file = tempfile.NamedTemporaryFile()
        np.savez_compressed(runtime_data_file, self._data_list)

        with tarfile.open(outfile, mode='w') as handle:
            handle.add(reference_atoms_file.name, arcname='atoms')
            handle.add(reference_data_file.name, arcname='reference_data')
            handle.add(runtime_data_file.name, arcname='runtime_data')
        runtime_data_file.close()

    def _add_default_metadata(self):
        """Adds default metadata to metadata dict."""

        self._metadata['date_created'] = \
            datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self._metadata['username'] = getpass.getuser()
        self._metadata['hostname'] = socket.gethostname()
        self._metadata['icet_version'] = icet_version
