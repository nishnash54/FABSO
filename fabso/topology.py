import numpy as np


class Particle:
    """Particle specific features and methods"""
    def __init__(self, position, fitness):
        """Initialize particle

        Arguments
        ---------

        position : List
            list of lenght equal to `n_dimensions`. Denotes the initial
            position of the particle in the search space
        fitness : float
            objective function value corresponding to the current
            position of the particle
        """
        self.fitness = fitness
        self.position = position.copy()
        self.pbest_value = fitness
        self.pbest_position = position.copy()
        self.velocity = np.zeros(len(position))

    def update(self, particle):
        """Update particle attribures

        Attributes updated based on copy constructor approach.
        Required attributes from a new particle used to over write.

        Arguments
        ---------

        particle : fabso.topology.Particle
            New particle. Extract data and update current particle
        """
        self.fitness = particle.fitness
        self.position = particle.position.copy()
        self.pbest_value = particle.pbest_value
        self.pbest_position = particle.pbest_position.copy()
        self.velocity = particle.velocity.copy()

    def __str__(self):
        return np.array_str(self.position)


class Space:
    """Defines the search space for Swarm optimization"""
    def __init__(
        self,
        bounds,
        objective,
        n_particles,
        n_dimensions,
    ):
        """Initialize search space

        Setup search space parameters to control particles, including
            * setup space from given particles list
            * setup space by generating random particles
            * randomly re-initialize the particles

        Arguments
        ---------

        bounds : tuple(int, int)
            Tuple of size 2 where the first entry is the minimum bound
            and second entry is the maximum bound `(min, max)`
         objective : function
            Objective function (calculates fitness value) for a
            given particles. returns fitness : float
        generations : int
            Number of generations/iterations to run the optimizer
        n_particles : int
            Number of particles in the swarm
        n_dimensions : int
            Dimensionality of the search space
        """
        self._bounds = bounds
        self._objective = objective
        self._n_particles = n_particles
        self._n_dimensions = n_dimensions

    def generate_particles(self, particles=None):
        """Generate particles and populate search space

        Populate search space based on a list of user input particles or
        randomly populate search space based on the user-defined parameters
        (n_particles, n_dimensions)

        Arguments
        ---------

        particles : List (default = `None`)
            Search space populated based on an input list of particles. If
            `None` particles are generated randomly based on user-defined
            parameters and bounds
        """
        if particles is None:
            self.particles = []
            for _ in range(self._n_particles):
                position = np.random.uniform(
                        self._bounds[0], self._bounds[1],
                        self._n_dimensions)
                fitness = self._objective(position)
                self.particles.append(Particle(position, fitness))
        else:
            assert len(particles) == self._n_particles
            assert len(particles[0]) == self._n_dimensions
            self.particles = []
            for idx in range(self._n_particles):
                self.particles.append(Particle(
                    particles[idx],
                    self._objective(particles[idx])))

    def random_restart(self):
        """Reandom restart

        Randomly re-initialize the swarm of particles. New particles are
        generated based on the user-defined parameters and bounds
        """
        self.particles = []
        for idx in range(self._n_particles):
            position = np.random.uniform(
                    self._bounds[0], self._bounds[1],
                    self._n_dimensions
                )
            fitness = self._objective(position)
            self.particles.append(Particle(position, fitness))

