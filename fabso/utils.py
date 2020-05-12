import matplotlib.pyplot as plt


def viz(results):
    """Generate visualization

    Plot global best value achieved (y-axis) over the generations (x-axis)
    when finding the optimal solution to the objective function

    Arguments
    ---------
    results: List
        List of optimal values achieved at each generation by the particle swarm

    Returns
    -------
    plot : matplotlib.pyplot.Figure
        Generated plot
    """
    plt.plot(range(len(results)), results, color='orange')
    plt.title('FABSO results')
    plt.xlabel('Generations')
    plt.ylabel('Ojvective value')
    return plt

