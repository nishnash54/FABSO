# FABSO
[![ACM DOI](https://img.shields.io/badge/ACM-doi%2F10.1145%2F3377929.3398112-success?style=for-the-badge)](https://dl.acm.org/doi/abs/10.1145/3377929.3398112) [![Download paper](https://img.shields.io/badge/PDF-Download-red?style=for-the-badge)](https://dl.acm.org/doi/pdf/10.1145/3377929.3398112)

###### Keywords
`swarm intelligence`, `archive`, `artificial neural networks`, `fitness-distance ratio`, `evolutionaly machine learning`, `permature convergence`, `particle swarm optimization`

### Abstract
The Particle Swarm Optimization (PSO) algorithm updates each individual's velocity and position using its own prior best position and the best position found so far by any particle. Effective search for global optima can benefit if each particle may utilize additional historical information regarding the quality of previously visited positions in its proximity. We present an approach for doing so, using an archive containing some prior particle positions, analogous to the archive used in some multi-objective optimization algorithms. A specific instance of this approach is the proposed *Fitness-Distance-Ratio Archive-Based Swarm Optimization* algorithm, shown to outperform PSO and three other variants, when applied to high-dimensional neural network training problems.

### Introduction
This repository contains the code for the core implementation of the *Fitness-Distance-Ratio Archive-Based Swarm Optimization (FABSO)* algorithm for maximizing the given objective function.

### Quickstart
For a quicksatrt into the implementation and the various available methods, refer to the [example notebook](./example.ipynb) where we find an optimal value of the *De Jong's function 1* using the FABSO algorithm.

### Documentation
For an in-depth documentation into the various classes and methods, please have a look at the [docs](./docs.md)!
### Citation
This work is licensed under MIT License. See [LICENSE](./LICENSE) for details.

If you find our code/paper useful, please consider citing our paper:
```bibtex
@inproceedings{10.1145/3377929.3398112,
    author = {Rodrigues, Nishant and Mohan, Chilukuri},
    title = {Archive-Based Swarms},
    year = {2020},
    isbn = {9781450371278},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3377929.3398112},
    doi = {10.1145/3377929.3398112},
    booktitle = {Proceedings of the 2020 Genetic and Evolutionary Computation Conference Companion},
    pages = {1460–1467},
    numpages = {8},
    keywords = {swarm intelligence, archive, artificial neural networks, fitness-distance ratio, 
        evolutionary machine learning, premature convergence, particle swarm optimization},
    location = {Canc\'{u}n, Mexico},
    series = {GECCO ’20}
}
```

