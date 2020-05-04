import sys
import numpy as np

from fabso.topology import Particle, Space

sys.path.append('./')
np.random.seed(42)

# Parameters
bounds = (-10, 10)
n_particles = np.random.randint(2, 10)
n_dimensions = np.random.randint(2, 10)


def objective(data):
    """
    Objective function
    Returns sum of array

    Parameters:
    data : np.array
    """
    return sum(data)

# Sample data
positions = np.random.randn(n_particles, n_dimensions)
fitness = [objective(pos) for pos in positions]


# Test Particle
def test_particle_init():
    """Test init particle"""
    particle = Particle(positions[0], fitness[0])
    assert str(particle) == np.array_str(positions[0])


def test_particle_update():
    """Test updating particle"""
    particle = Particle(positions[0], fitness[0])
    _new_particle = Particle(positions[1], fitness[1])
    particle.update(_new_particle)
    assert np.array_equal(particle.position, positions[1])
    assert particle.fitness == fitness[1]

# Test Space
space = Space(bounds, objective, n_particles, n_dimensions)


def test_space_generate_random():
    """Test randomly populating search space"""
    space.generate_particles()
    particle_positions = [part.position for part in space.particles]
    particle_fitness = [part.fitness for part in space.particles]
    assert np.array(particle_positions).shape == (n_particles, n_dimensions)
    assert np.array(particle_fitness).shape == (n_particles,)


def test_space_generate_particles():
    """Test populating space based on given positions"""
    space.generate_particles(positions)
    particle_positions = [part.position for part in space.particles]
    particle_fitness = [part.fitness for part in space.particles]
    assert np.array_equal(particle_positions, positions)
    assert np.array_equal(particle_fitness, fitness)


def test_space_random_restart():
    """Test applying random restarts"""
    space.random_restart()
    particle_positions = [part.position for part in space.particles]
    particle_fitness = [part.fitness for part in space.particles]
    assert np.array(particle_positions).shape == (n_particles, n_dimensions)
    assert np.array(particle_fitness).shape == (n_particles,)
    assert not np.array_equal(particle_positions, positions)
    assert not np.array_equal(particle_fitness, fitness)

