from slicesampling import univariate_sampler
import numpy as np


def map_1d_to_nd(u, v, x0):
    """

    :param u:
    :param v:
    :param x0:
    :return:
    """

    x = u * v + x0

    return x


class SliceSampler(univariate_sampler.UnivariateSliceSampler):
    """ Implementation of the multivariate slice_sampler sampler, based on [1, 2, 3].

    References
    ----------
    [1] Neal, Radford M. (2003). Slice sampling. The Annals of Statistics, 31(3), 705 - 767. URL: https://doi.org/10.1214/aos/1056562461
    [2] Thompson, Madeleine (2011). Slice Sampling with Multivariate Steps. PhD Thesis. URL: https://hdl.handle.net/1807/31955
    [3] Rudolf, Daniel; Ullrich, Mario (2018). Comparison of hit-and-run, slice_sampler sampler and random walk metropolis. Journal of Applied Probability, 55(4), 1186-1202. URL: https://doi.org/10.1017/jpr.2018.78

    Attributes
    ----------
    :param current_sample = the last known sample
    :param current_log_likelihood_value = log_likelihood of the last known sample
    :param dimension = dimension of the sampled space (number of variables/parameters)
    :param expansion_method = method to expand the sampling interval
    :param expansion_limit = maximum number of expansions for a single sample
    :param initial_interval_width = initial width for the sampling interval
    :param count = number of samples taken since initialization
    """

    def __init__(self, *, log_likelihood_function, initial_sample=np.array(0),
                 adaptation_interval=False,
                 direction_method='random',
                 expansion_method='double',
                 expansion_limit=8,
                 initial_interval_width=1):
        """ Create a multivariate slice_sampler sampler that samples in one direction at the time

        Parameters
        ----------
        :param log_likelihood_function: function that evaluates log-likelihood taking a sample (x) as an input
        :param initial_sample: initial sample (x)
        :param adaptation_interval: number of samples between adaptation of the covariance matrix (0 for no updates)
        :param direction_method: method to sample in multivariate space, either
            "univar_random" (sample one random direction according of the covariance matrix for one sample) or
            "univar_eigen" (univariate updates along every eigenvector of the covariance matrix for one sample)
        :param expansion_method: method to expand sampling interval (either 'fixed', 'double', or 'step_out')
        :param expansion_limit: maximum number of expansions of sampling interval for one new sample, only relevant if
        expansion_method equals 'double' or 'step_out'.
        :param initial_interval_width: initial width of sampling interval, only relevant if
        expansion_method equals 'double' or 'step_out'.
        """

        assert isinstance(initial_sample, np.ndarray), \
            "initial_sample must be a NumPy array (numpy.ndarray). "
        assert initial_sample.ndim == 1, \
            "initial_sample must be a 1-dimensional array."
        assert expansion_method in ['fixed', 'double', 'step_out'], \
            "method to choose direction must be either 'random' or 'gibbslike'. "
        assert direction_method in ['random_eigen', 'univar_eigen'], \
            "method to choose direction must be either 'random_eigen' or 'univar_eigen'. "

        super().__init__(log_likelihood_function=log_likelihood_function,
                         initial_sample=initial_sample,
                         expansion_method=expansion_method,
                         expansion_limit=expansion_limit,
                         initial_interval_width=initial_interval_width)

        dimension = initial_sample.shape[0]

        if dimension == 1:
            # override adaptation, only needed in multivariate case
            adaptation_interval = 0
            pass

        self.adaptation_interval = adaptation_interval
        self.count = 0
        self.sample_mean = initial_sample
        self.sample_covariance = np.zeros(dimension)
        self.sample_coordinate_basis = np.eye(dimension)

        self.dimension = dimension
        self.multivariate_log_likelihood_function = log_likelihood_function

        self.direction_method = direction_method

        self._assert_input()

        return

    def _assert_input(self):

        assert isinstance(self.current_sample, np.ndarray), "initial_sample must be a float. "

        return

    def _get_sample_univar(self, v, x0, y0):
        """ Apply univariate slice_sampler sampler to get a sample in the chose direction

        :param v: chosen direction and unit vector
        :param x0: current sample in the multivariate space
        :param y0: log-likelihood at the current sample
        :return: new sample as pair of sample (x1) and log-likelihood (y1)
        """

        self.log_likelihood_function = lambda u: self.multivariate_log_likelihood_function(map_1d_to_nd(u, v, x0))
        u0 = 0
        [u1, y1] = self._get_sample(u0, y0)
        x1 = map_1d_to_nd(u1, v, x0)

        return x1, y1

    def _sample_update(self):
        """ Get a new sample and update associated attributes in the sampler object and execute following actions as
        necessary:
        -   recursive estimation of mean vector and covariance matrix of the samples
        -   adjust coordinate basis for the multivariate space so origin reflects the sample mean and the coordinates
            align with the eigenvectors of the covariance matrix
        """

        x0 = self.current_sample
        y0 = self.current_log_likelihood_value

        if self.direction_method == 'random_eigen':
            v = np.matmul(self.sample_coordinate_basis, np.random.randn(self.dimension))
            [x0, y0] = self._get_sample_univar(v, x0, y0)
            pass
        elif self.direction_method == 'univar_eigen':
            for direction in np.random.permutation(range(self.dimension)):
                v = self.sample_coordinate_basis[:, direction]
                [x0, y0] = self._get_sample_univar(v, x0, y0)
                pass
            pass

        self.current_sample = x0
        self.current_log_likelihood_value = y0
        self.count += 1

        if self.adaptation_interval > 0:
            alpha = 1 / self.count
            dx = x0 - self.sample_mean
            self.sample_covariance = (1 - alpha) * (self.sample_covariance + alpha * np.dot(dx[:, None], dx[:, None].T))
            self.sample_mean = (1 - alpha) * self.sample_mean + alpha * x0
            if np.mod(self.count, self.adaptation_interval) == 0:
                eigenvectors, eigenvalues, eigenvectorsT = np.linalg.svd(self.sample_covariance)
                coordinate_basis = np.matmul(eigenvectors, np.diag(eigenvalues ** (1 / 2)))
                self.sample_coordinate_basis = coordinate_basis
                pass
            pass

        return

    pass


if __name__ == '__main__':
    help(SliceSampler)
    pass
