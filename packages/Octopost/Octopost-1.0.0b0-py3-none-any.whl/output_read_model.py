# -*- coding: utf-8 -*-
"""Convienence class to extract various data from Octopus output.
"""

# Python Imports
import re

# Third Party Imports
import numpy as np
import matplotlib.pyplot as plt

# Octopost Imports
import units


class OutputReadModel:
    """OutputRead model handles all things related to basic information output.

    Should not be used directly by the user but called by the abstraction layer
    octopost class.

    Args:
        octopost (object): An instance of the octopost class.
    """

    def __init__(self, ocotpost):
        self.op = ocotpost

    def get_fermi(self, energy_units='hartree'):
        """Returns fermi energy found in the 'total-dos-efermi.dat' file.

        Args:
            energy_units (str): Specify the units in which the energy is
                returned. Options: 'hartree', 'eV'

        Returns:
            float:
                Fermi energy in the specified units.
        """

        file = 'total-dos-efermi.dat'
        dir_ = 'static'
        path = self.op._check_for_file(dir_, file)

        with open(path, 'r') as f:
            # Fermi energy is the first value in the file
            fermi = np.loadtxt(f)[0, 0]

        if energy_units == 'eV':
            fermi = units.energy(fermi, from_='hartree', to='eV')

        return fermi

    def get_eigenvalues(self, n_max=None, n_min=1, k_point=None,
                        energy_units='hartree'):
        """Returns the eigenvalues found in the 'info' file.

        Args:
            n_max (int): How many eigenvalues to be returned. If 'None' all of
                them are returned. If n_max > available eigenvalues all
                available ones are returned.
            k_points (int): At which k_point the eigenvalues are to be read.
            energy_units (str): Specify the units in which the energy is
                returned. Options: 'hartree', 'eV'

        Returns:
            list:
                List of eigenvalues (float).
        """

        dir_ = 'static'
        file = 'info'
        path = self.op._check_for_file(dir_, file)

        with open(path, 'r') as f:
            line = f.readline()

            if k_point is not None:
                # Periodic system
                while line and ('#k =' + f'{k_point}'.rjust(4)) not in line:
                    line = f.readline()

            else:
                # Non-periodic system
                while (line and
                       line != ' #st  Spin   Eigenvalue      Occupation\n'):
                    line = f.readline()

            if not line:
                print(f'{path} is not a valid \'info\' file.')
                raise

            eigenvalues = []
            if n_max is not None:
                line = f.readline()
                n = 1
                while (line and line != '\n' and '#k' not in line and
                       n <= n_max):

                    if n >= n_min:
                        eigenvalues.append(float(
                            re.search('-- *(.*?) ', line).groups()[0]))

                    line = f.readline()
                    n += 1

                if '#k' in line:
                    print('INFO: Not enough eigenvalues.')

            else:
                line = f.readline()
                n = 1
                while (line and line != '\n' and
                       '#k' not in line):

                    if n >= n_min:
                        eigenvalues.append(float(
                            re.search('-- *(.*?) ', line).groups()[0]))

                    line = f.readline()
                    n += 1

        eigenvalues = np.array(eigenvalues)
        if energy_units == 'eV':
            eigenvalues = units.energy(eigenvalues, from_='hartree', to='eV')

        return eigenvalues

    def get_cell(self):
        """Returns lattice vectors.

        Returns:
            nd.array:
                3x3 array where first index runs through the vectors
                and second through their coordinate.
        """

        dir_ = 'static'
        file = 'info'
        path = self.op._check_for_file(dir_, file)

        found = False
        with open(path) as f:
            for line in f:
                if line.startswith('  Lattice Vectors'):
                    lattice = np.zeros((3, 3))
                    for i in range(3):
                        lattice[i, :] = self._parse_vector(f.readline())
                        found = True
        if found:
            return lattice

        else:
            print('No reciprocal lattice found. Is this system periodic?')
            raise TypeError

    def get_reciprocal_cell(self):
        """Returns reciprocal lattice vectors.

        Returns:
            nd.array:
                3x3 array where first index runs through the vectors and second
                through their coordinate.
        """

        dir_ = 'static'
        file = 'info'
        path = self.op._check_for_file(dir_, file)

        found = False
        with open(path) as f:
            for line in f:
                if line.startswith('  Reciprocal-Lattice Vectors'):
                    lattice = np.zeros((3, 3))
                    for i in range(3):
                        lattice[i, :] = self._parse_vector(f.readline())
                        found = True
        if found:
            return lattice

        else:
            print('No reciprocal lattice found. Is this system periodic?')
            raise TypeError

    def get_convergence(self, plot=False):
        """Returns the convergence parameter energy and density.

        Args:
            plot (bool): If True a basic convergence plot for energy and
                density will be returned.

        Returns:
            nd.array:
                First column is the SCF cycle. Then energy, energy
                difference, density and relative density in this order.
            fig, ax, ax:
                Matplotlib handles for the figure, the left axis
                and the right axis in this order.
        """

        dir_ = 'static'
        file = 'convergence'
        path = self.op._check_for_file(dir_, file)
        data = np.loadtxt(path)[:, :5]

        if plot:
            fig, ax_left = plt.subplots()

            line_1 = ax_left.plot(data[:, 0], data[:, 1], marker='o',
                                  linestyle='', color='tab:red',
                                  label='Total Energy')
            line_2 = ax_left.plot(data[:, 0], data[:, 2], color='tab:red',
                                  label='Energy Difference', marker='x',
                                  linestyle='')

            ax_left.set_xlabel('SCF Cycle')
            ax_left.set_ylabel('Energy (Hartree)', color='tab:red')
            ax_left.tick_params(axis='y', labelcolor='tab:red')

            ax_right = ax_left.twinx()
            line_3 = ax_right.plot(data[:, 0], data[:, 3], marker='o',
                                   linestyle='', color='tab:blue',
                                   label='Total Density')
            line_4 = ax_right.plot(data[:, 0], data[:, 4], color='tab:blue',
                                   marker='x', linestyle='',
                                   label='Relative Density')

            ax_right.set_ylabel('Density', color='tab:blue')
            ax_right.tick_params(axis='y', labelcolor='tab:blue')

            lines = line_1 + line_2 + line_3 + line_4
            labels = [line.get_label() for line in lines]
            ax_left.legend(lines, labels, loc='center left')

            return data, (fig, ax_left, ax_right)

        else:
            return data

    def _parse_vector(self, line):
        vector = re.search(
            r' {3,4}([0-9\.\-]*) {3,4}([0-9\.\-]*) {3,4}([0-9\.\-]*)',
            line).groups((1, 2, 3))
        vector = [float(number) for number in vector]

        return vector
