# slicesampler

Set of Markov chain Monte Carlo (MCMC) sampling methods based on slice sampling

## Available methods

The package includes the following methods:
1. Univariate slice sampler, as described in [1]
2. Multivariate slice sampler based on univariate updates along eigenvectors, as described in [2]
3. Multivariate slice sampler based on combination of hit-and-run and univariate slice sampler, named hybrid slice sampler in [3]

## Examples

1. example1_univariate.py illustrates how to use the package for univariate slice sampling
2. example2_bivariate.py illustrates how to use the package for multivariate slice sampling
