import matplotlib.pyplot as plt


def viz(results):
    """Generate visualization

    Plot global best value achieved (y-axis) over the generations (x-axis)
    when finding the optimal solution to the objective function

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

