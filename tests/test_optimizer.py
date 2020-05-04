import sys
import pytest
import numpy as np

from fabso.topology import Particle, Space
from fabso.optimizer import FABSO

sys.path.append('./')
np.random.seed(42)

# Parameters
bounds = (-10, 10)
generations = 50
archive_size = 5
restart_freq = 20
n_particles = np.random.randint(2, 10)
n_dimensions = np.random.randint(2, 10)


def objective(data):
    """
    Objective function
    Returns sum of array

    Parameters:
    data : np.array
    """
    return -sum(data)

space = Space(bounds, objective, n_particles, n_dimensions)
space.generate_particles()


def test_missing_params():
    """Test missing keys in parameters"""
    with pytest.raises(KeyError):
        params = {'w': 0.9, 'c1': 1, 'c2': 0}
        fabso = FABSO(
                space, bounds, params, objective, generations,
                n_particles, n_dimensions, archive_size, restart_freq
            )


def test_assertion():
    """Test assertion (generations)"""
    with pytest.raises(AssertionError):
        params = {'w': 0.9, 'c1': 1, 'c2': 0, 'c3': 2}
        fabso = FABSO(
                space, bounds, params, objective, -1,
                n_particles, n_dimensions, archive_size, restart_freq
            )

# Sample optimizer
params = {'w': 0.9, 'c1': 1, 'c2': 0, 'c3': 2}
fabso = FABSO(
        space, bounds, params, objective, generations,
        n_particles, n_dimensions, archive_size, restart_freq
    )


def test_update_weight():
    """Test decreasing inertia weight"""
    assert fabso.w == 0.9
    fabso._update_w(1)
    assert round(fabso.w, 5) == 0.48611
    fabso._update_w(10)
    assert round(fabso.w, 5) == 0.39683
    fabso._update_w(30)
    assert round(fabso.w, 5) == 0.19841


def test_archive():
    """Test archive generation"""
    fabso._archive()
    assert len(fabso.archive) == fabso._archive_size
    assert len(fabso.archive_fitness) == fabso._archive_size


def test_optimize():
    """Test results from optimizer"""
    results = fabso.optimize()
    assert len(results) == fabso._generations

