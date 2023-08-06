# -*- coding: utf-8 -*-
from pathlib import Path
from pytest import approx

import octopost


def test_get_eigenvalues():
    dir_path = Path(__file__).parent
    op = octopost.Octopost(dir_path / '../demo/data/graphene')

    eigenvalues = op.get_eigenvalues(n_max=None, k_point=1)

    assert(len(eigenvalues) == 5)

    eigenvalues = op.get_eigenvalues(n_max=1, k_point=3)
    assert(eigenvalues[0] == -0.867412)

    eigenvalues = op.get_eigenvalues(n_max=1, k_point=3, energy_units='eV')
    assert(eigenvalues[0] == approx(-23.60348296640494))

def test_get_fermi():
    dir_path = Path(__file__).parent
    op = octopost.Octopost(dir_path / '../demo/data/PTCDA')

    fermi = op.get_fermi()
    assert(fermi == approx(-0.240775))