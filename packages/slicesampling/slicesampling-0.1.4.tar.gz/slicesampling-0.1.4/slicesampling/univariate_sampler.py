#!/usr/bin/env python


import numpy as np
import warnings


class UnivariateSliceSampler:
    """
    Implementation of the univariate slice_sampler sampler, as described in [1].

    References
    ----------
    [1] Neal, R. M. (2003). Slice sampling. Ann. Statist. 31 (3) 705 - 767. https://doi.org/10.1214/aos/1056562461

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

    def __init__(self, *, log_likelihood_function,
                 initial_sample=0,
                 expansion_method: str = 'double',
                 expansion_limit: int = 8,
                 initial_interval_width: float = 1):
        """
        Create a univariate slice_sampler sampler

        Parameters
        ----------
        :param log_likelihood_function: function that evaluates log-likelihood taking a sample (x) as an input
        :param initial_sample: initial sample (x)
        :param expansion_method: method to expand sampling interval (either 'fixed', 'double', or 'step_out')
        :param expansion_limit: maximum number of expansions of sampling interval for one new sample, only relevant if
        expansion_method equals 'double' or 'step_out'.
        :param initial_interval_width: initial width of sampling interval, only relevant if
        expansion_method equals 'double' or 'step_out'.
        """

        assert expansion_method in ['fixed', 'double', 'step_out'], \
            "method to choose direction must be either 'fixed', 'double', or 'step_out'. "

        self.log_likelihood_function = log_likelihood_function

        if np.isnan(log_likelihood_function(initial_sample)):
            warnings.warn("Initial sample results in NaN results for log_likelihood_function. Sampler may not succeed "
                          "in finding feasible samples.")
            pass

        if np.isinf(log_likelihood_function(initial_sample)):
            warnings.warn("Initial sample results in infinity value for log_likelihood_function. Sampler may not "
                          "succeed in finding feasible samples.")
            pass

        self.current_sample = initial_sample
        self.current_log_likelihood_value = self.log_likelihood_function(initial_sample)
        self.dimension = 1
        self.expansion_method = expansion_method
        self.expansion_limit = expansion_limit
        self.initial_interval_width = initial_interval_width
        self.count = 0

        self._assert_input()

        return

    def _assert_input(self):

        assert isinstance(self.current_sample, float), "initial_sample must be a float. "

        return

    def get_trace(self, number_of_samples: int = 1000):
        """
        Produces a sequence of Markov Chain Monte Carlo samples with the slice_sampler sampler

        :param number_of_samples: number of samples to get from the sampler
        :return: sequence of samples, corresponding log-likelihood values
        """

        sample_sequence = np.matrix(np.zeros([0, self.dimension]))
        log_likelihood_seq = []
        sample_index = 0
        while sample_index < number_of_samples:
            self._sample_update()
            sample = self.current_sample
            log_likelihood_value = self.current_log_likelihood_value
            if np.isinf(log_likelihood_value) or np.isnan(log_likelihood_value):
                # do not add sample to sequence if infeasible
                pass
            else:
                sample_sequence = np.append(sample_sequence, np.matrix(sample), axis=0)
                log_likelihood_seq = np.append(log_likelihood_seq, log_likelihood_value)
                sample_index += 1
                pass

        return sample_sequence, log_likelihood_seq

    def _sample_update(self):
        """ Get a new sample and update associated attributes in the sampler object """

        x0 = self.current_sample
        y0 = self.current_log_likelihood_value

        [x1, y1] = self._get_sample(x0, y0)

        self.current_sample = x1
        self.current_log_likelihood_value = y1
        self.count += 1
        return

    def _get_sample(self, x0, y0):
        """ Get a new Monte Carlo sample starting from a given sample (x0) and corresponding log-likelihood (y0)

        :param x0: sample to start with
        :param y0: auxiliary variable (log-likelihood) to start with
        :return: [x1, y1]; pair of new sample (x1) and corresponding log-likelihood (y1)
        """

        # define auxiliary variable range as [0, y]
        alpha = np.random.rand(1)
        y = np.log(alpha) + y0

        # apply procedure to define new sampling interval
        if self.expansion_method == 'step_out':
            [bound_left, bound_right] = self._step_out(x0, y)
            pass
        elif self.expansion_method == 'double':
            [bound_left, bound_right] = self._double(x0, y)
            pass
        elif self.expansion_method == 'fixed':
            u = np.random.rand(1)
            bound_left = x0 - self.initial_interval_width * u
            bound_right = bound_left + self.initial_interval_width
            pass

        # sample from sampling interval defined above
        accept_sample = False
        while not accept_sample:

            # get proposal
            u = np.random.rand(1)
            x1 = bound_left + u * (bound_right - bound_left)
            y1 = self.log_likelihood_function(x1)

            # evaluate proposal
            if y < y1 and self._accept(x0, x1, y, bound_left, bound_right):
                accept_sample = True
                pass

            # update sampling interval if proposal was rejected
            if not accept_sample:
                if x1 < x0:
                    bound_left = x1
                    pass
                else:
                    bound_right = x1
                    pass
                pass

            pass

        return x1, y1

    def _accept(self, x0, x1, y, bound_left, bound_right):
        """ Evaluate whether proposed sample satisfies detailed balance

        :param x0: sample of origin
        :param x1: newly proposed sample
        :param y: auxiliary variable (log-likelihood reference)
        :param bound_left: left bound of sampling interval
        :param bound_right: right bound of sampling interval
        :return: accept/reject decision
        :rtype: boolean
        """

        # accept sample by default
        accept_sample = True

        # detailed balance check when using the doubling interval expansion method. See original paper cited in class
        # docstring for detailed information
        if self.expansion_method == 'double':
            bound_left_star = bound_left
            bound_right_star = bound_right
            y_left_star = np.nan
            y_right_star = np.nan
            decision = False
            while bound_right_star - bound_left_star > 1.1 * self.initial_interval_width:
                center = (bound_left_star + bound_right_star) / 2
                if (x0 < center <= x1) or (x0 >= center > x1):
                    decision = True
                    pass
                if x1 < center:
                    bound_right_star = center
                    y_right_star = self.log_likelihood_function(bound_right_star)
                    pass
                else:
                    bound_left_star = center
                    y_left_star = self.log_likelihood_function(bound_left_star)
                    pass
                if decision:
                    if np.isnan(y_left_star):
                        y_left_star = self.log_likelihood_function(bound_left_star)
                        pass
                    if np.isnan(y_right_star):
                        y_right_star = self.log_likelihood_function(bound_right_star)
                        pass
                    if y >= y_left_star and y >= y_right_star:
                        accept_sample = False
                        pass
                    pass

                pass
            pass

        return accept_sample

    def _double(self, x0, y):
        """ Apply doubling procedure to obtain new sampling interval

        :param x0: current sample
        :param y: auxiliary variable (reference log-likelihood)
        :return: sampling interval as a pair of scalars: bound_left, bound_right
        """

        # define initial interval by picking a random number from the unit interval and defining this point as the
        # center of the initial sampling interval
        u = np.random.rand(1)
        bound_left = x0 - self.initial_interval_width * u
        bound_right = bound_left + self.initial_interval_width

        # evaluate log-likelihood at the interval bounds
        y_left = self.log_likelihood_function(bound_left)
        y_right = self.log_likelihood_function(bound_right)

        # continue to expand the sampling interval until (a) the interval bound log-likelihood remain above the
        # reference log-likelihood or (b) the maximum number of expansions has been met
        expansion_budget = self.expansion_limit
        while expansion_budget > 0 and (y < y_left or y < y_right):
            # determine to expand to the left (0) or to the right (1)
            v = np.random.rand(1) * 2
            direction = v > 1

            # double the size of the interval
            if direction:
                bound_right = bound_right + (bound_right - bound_left)
                y_right = self.log_likelihood_function(bound_right)
                pass
            else:
                bound_left = bound_left - (bound_right - bound_left)
                y_left = self.log_likelihood_function(bound_left)
                pass

            # update number of expansions available
            expansion_budget -= 1
            pass

        return bound_left, bound_right

    def _step_out(self, x0, y):
        """ Apply step-out procedure to obtain new sampling interval

        :param x0: current sample
        :param y: auxiliary variable (reference log-likelihood)
        :return: sampling interval as a pair of scalars: bound_left, bound_right
        """

        # define initial interval by picking a random number from the unit interval and defining this point as the
        # center of the initial sampling interval
        u = np.random.rand(1)
        bound_left = x0 - self.initial_interval_width * u
        bound_right = bound_left + self.initial_interval_width

        # determine number of times one can step out to the left and to the right
        v = np.random.rand(1)
        expansion_budget_left = np.floor(self.expansion_limit * v)
        expansion_budget_right = (self.expansion_limit - 1) - expansion_budget_left
        while expansion_budget_left > 0 and y < self.log_likelihood_function(bound_left):
            bound_left = bound_left - self.initial_interval_width
            expansion_budget_left = expansion_budget_left - 1
            pass

        while expansion_budget_right > 0 and y < self.log_likelihood_function(bound_right):
            bound_right = bound_right + self.initial_interval_width
            expansion_budget_right = expansion_budget_right - 1
            pass

        return bound_left, bound_right

    pass


if __name__ == '__main__':
    help(UnivariateSliceSampler)
    pass
