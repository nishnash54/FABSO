import numpy as np
from scipy.spatial.distance import euclidean


class FABSO:
    def __init__(
        self,
        space,
        bounds,
        params,
        objective,
        generations,
        n_particles,
        n_dimensions,
        archive_size,
        restart_freq=np.inf
    ):
        """Initialize the algorithm

        Creates a FABSO class depending on the values initialized

        Attributes
        ----------
        space : fabso.topology.Space
            Search space containing particle swarm
        bounds : tuple(int, int)
            Tuple of size 2 where the first entry is the minimum bound
            and second entry is the maximum bound `(min, max)`
        params : Dict with keys `{'w', 'c1', 'c2', 'c3'}`
            A dictionary containing the parameters for the specific
            optimization technique
                * w : float
                    inertia parameter
                * c1 : float
                    cognitive parameter
                * c2 : float
                    social parameter
                * c2 : float
                    additional parameter
        objective : function
            Objective function (calculates fitness value) for a
            given particles. returns fitness : float
        generations : int
            Number of generations/iterations to run the optimizer
        n_particles : int
            Number of particles in the swarm
        n_dimensions : int
            Dimensionality of the search space
        archive_size : int
            Maximum number of particles the archive can hold
        restart_freq : int
            Number of iterations with no improvements after which
            the swarm is randomly re-initialized
        """
        self.space = space
        self._bounds = bounds
        self._objective = objective
        self._generations = generations
        self._n_particles = n_particles
        self._n_dimensions = n_dimensions
        self._archive_size = archive_size
        self._restart_freq = restart_freq
        self._vmax = -bounds[0] + bounds[1]

        assert generations >= 0
        assert n_particles >= 0
        assert n_dimensions >= 0
        assert restart_freq >= 1
        assert n_particles >= archive_size and archive_size >= 0

        try:
            self.w = params['w']
            self.c1 = params['c1']
            self.c2 = params['c2']
            self.c3 = params['c3']
            self._w = self.w
        except KeyError:
            print('Params: Missing parameters')
            raise KeyError

    def _archive(self):
        """Setup archive

        Helper function to initialize archive and populate archive elements
        Select the best N(archive size)  particles from the swarm based
        on their fitness values.
        """
        population_fitness = np.array(
                [self.space.particles[i].fitness
                    for i in range(self._n_particles)])
        n_best_idx = population_fitness.argsort()[
                -self._archive_size:][::-1].tolist()
        self.archive = [self.space.particles[idx].position.copy()
                        for idx in n_best_idx]
        self.archive_fitness = [population_fitness[idx] for idx in n_best_idx]

        self.gbest_value = np.max(population_fitness)
        self.gbest_position = self.space.particles[
                np.argmax(population_fitness)].position.copy()

    def _update_w(self, idx):
        """Update inertial weight parameter

        Implements linearly decreasing inertial weight.
        params.w -> 0.4 over generations

        Arguments
        ---------

        idx : int
            Index or current generation
        """
        self.w = ((self._w - 0.4) * (self._generations - idx)) /\
            (self._generations + 0.4)

    def _velocity_position(self, particle, dim, p_nd):
        """Velocity and Position update

        Update the velocity and calculate the new position of a single
        dimension of a particle based on the update parameters and bounds

        Arguments
        ---------

        particle : fabso.topology.Particle
            Contains particle features required to update
        dim : int
            Dimension value between `0` and `(n_dimensions - 1)`
        p_nd : float
            Position of selected archive element along dimension `dim`

        Return
        ------
        new_velocity : float
            Updated velocity along the dimension
        new_position : float
            Updated position along the dimension
        """

        new_velocity = (self.w * particle.velocity[dim]) \
            + (self.c1 *
                (particle.pbest_position[dim] - particle.position[dim])) \
            + (self.c2 * (self.gbest_position[dim] - particle.position[dim])) \
            + (self.c3 * (p_nd - particle.position[dim]))

        new_velocity = min(
                self._vmax,
                max(-self._vmax, new_velocity)
                )

        new_position = min(
                self._bounds[1],
                max(self._bounds[0], particle.position[dim] + new_velocity)
                )

        return new_velocity, new_position

    def optimize(self):
        """Optimization loop

        Runs the Fitness-Distance-Ratio Archive-Based Swarm Optimization
        based on the paper titled "Archive Based Swarms"

        Return
        ------
        results : List
            List of global best values achieved over the generations
        """
        self._archive()
        no_improve = 0
        results = []
        gbest_old = self.gbest_value
        # Generations
        for t in range(self._generations):
            self._update_w(t)
            # Particles
            for i in range(self._n_particles):
                particle = self.space.particles[i]
                new_velocity = np.zeros(self._n_dimensions)
                new_position = np.zeros(self._n_dimensions)
                # Dimensions
                for d in range(self._n_dimensions):
                    pn_value = float('-inf')
                    p_nd = 0
                    for j in range(self._archive_size):
                        if np.array_equal(particle.position, self.archive[j]):
                            continue

                        candidate = self.archive_fitness[j] - particle.fitness
                        den = max(
                                abs(self.archive[j][d] - particle.position[d]),
                                10e-100
                                )
                        candidate /= den
                        if candidate > pn_value:
                            pn_value = candidate
                            p_nd = self.archive[j][d]

                    new_velocity[d], new_position[d] = self._velocity_position(
                                                        particle, d, p_nd)

                particle.position = new_position.copy()
                particle.velocity = new_velocity.copy()

                candidate_fitness = self._objective(particle.position)
                particle.fitness = candidate_fitness
                if candidate_fitness > particle.pbest_value:
                    particle.pbest_value = candidate_fitness
                    particle.pbest_position = particle.position.copy()
                if candidate_fitness > self.gbest_value:
                    self.gbest_value = candidate_fitness
                    self.gbest_position = particle.position.copy()

                b_value = float('inf')
                b_idx = None
                # Archive
                for idx, element in enumerate(self.archive):
                    dist = euclidean(element, particle.position)
                    if dist < b_value:
                        b_value = dist
                        b_idx = idx

                if candidate_fitness > self.archive_fitness[b_idx]:
                    self.archive[b_idx] = particle.position.copy()
                    self.archive_fitness[b_idx] = candidate_fitness

                self.space.particles[i].update(particle)

            results.append(-self.gbest_value)

            if self.gbest_value == gbest_old:
                no_improve += 1
            else:
                no_improve = 0
            if no_improve == self._restart_freq:
                self.space.random_restart()
                no_improve = 0
            gbest_old = self.gbest_value

        return results

