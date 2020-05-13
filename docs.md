# Documentation
## Table of Contents
 * [fabso.topology](#fabsotopology)
    * [fabso.topology.Particle](#fabsotopologyparticle)
       * [Update](#update)
    * [fabso.topology.Space](#fabsotopologyspace)
       * [Generate particles](#generate-particles)
       * [Random restart](#random-restart)
 * [fabso.optimizer](#fabsooptimizer)
    * [fabso.optimizer.FABSO](#fabsooptimizerfabso)
       * [Setup archive](#setup-archive)
       * [Update weight](#update-weight)
       * [Velocity and Position update](#velocity-and-position-update)
       * [Optimize](#optimize)
 * [fabso.utils](#fabsoutils)
    * [Generate visualization](#generate-visualization)
## fabso.topology
#### fabso.topology.Particle
```py
class fabso.topology.Particle(position, fitness)
'''Particle specific features and methods'''
```
###### Arguments:
```yaml
position : List
        list of lenght equal to `n_dimensions`. Denotes the initial
        position of the particle in the search space
fitness : float
    objective function value corresponding to the current
    position of the particle
```
#### Methods:
##### Update
```py
update(self*, particle)
'''
    Attributes updated based on copy constructor approach.
    Required attributes from a new particle used to over write.
'''
```
###### Arguments:
```yaml
particle : fabso.topology.Particle
        New particle. Extract data and update current particle
```
#### fabso.topology.Space
```py
class fabso.topology.Space(self, bounds, objective, n_particles, n_dimensions)
'''
    Defines the search space for Swarm optimization
    
    Initialize search space. Setup search space parameters to control particles, including
     * setup space from given particles list
     * setup space by generating random particles
     * randomly re-initialize the particles
'''
```
###### Arguments:
```yaml
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
```
#### Methods:
##### Generate particles
```py
generate_particles(self, particles=None)
'''
    Populate search space based on a list of user input particles or
    randomly populate search space based on the user-defined parameters
    (n_particles, n_dimensions)
'''
```
###### Arguments:
```yaml
particles : List (default = `None`)
    Search space populated based on an input list of particles. If
    `None` particles are generated randomly based on user-defined
    parameters and bounds
```
##### Random restart
```py
random_restart(self)
'''
    Randomly re-initialize the swarm of particles. New particles are 
    generated based on the user-defined parameters and bounds
'''
```
## fabso.optimizer
#### fabso.optimizer.FABSO
```py
class fabso.optimizer.FABSO(
    self, space, bounds, params, objective, generations,
    n_particles, n_dimensions, archive_size, restart_freq=np.inf
)
```
###### Arguments:
```yaml
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
```
#### Methods:
##### Setup archive
```py
_archive(self)
'''
    Helper function to initialize archive and populate archive elements
    Select the best N(archive size)  particles from the swarm based
    on their fitness values.
'''
```
##### Update weight
```py
_update_w(self, idx)
'''
    Implements linearly decreasing inertial weight.
    params.w -> 0.4 over generations
'''
```
###### Arguments:
```yaml
idx : int
    Index or current generation
```
##### Velocity and Position update
```py
_velocity_position(self, particle, dim, p_nd)
'''
    Update the velocity and calculate the new position of a single
    dimension of a particle based on the update parameters and bounds
'''
```
###### Arguments:
```yaml
particle : fabso.topology.Particle
    Contains particle features required to update
dim : int
    Dimension value between `0` and `(n_dimensions - 1)`
p_nd : float
    Position of selected archive element along dimension `dim`
```
###### Returns:
```yaml
new_velocity : float
    Updated velocity along the dimension
new_position : float
    Updated position along the dimension
```
##### Optimize
```py
optimize(self)
'''
    Runs the Fitness-Distance-Ratio Archive-Based Swarm Optimization
    based on the paper titled "Archive Based Swarms"
'''
```
###### Returns:
```yaml
results : List
    List of global best values achieved over the generations
```
## fabso.utils
#### Methods
##### Generate visualization
```py
viz(results)
'''
    Plot global best value achieved (y-axis) over the generations (x-axis)
    when finding the optimal solution to the objective function
'''
```
###### Arguments:
```yaml
results: List
    List of optimal values achieved at each generation by the particle swarm
```
###### Returns:
```yaml
plot : matplotlib.pyplot.Figure
    Generated plot
```
