class Configuration(object):
    def __init__(self):
        self._cycles_samples = 20
        self._cycles_max_bounces = 8
        self._p_scalar_mutation = 0.1
        self._scalar_range_sigma = 0.1
        self._p_color_mutation = 0.1
        self._color_sigma = 0.1

    @property
    def cycles_samples(self):
        """
        The number of samples per pixel to use when rendering.
        """
        return self._cycles_samples

    @property
    def cycles_max_bounces(self):
        """
        The maximum number of bounces light is allowed when rendering.
        """
        return self._cycles_max_bounces

    @property
    def p_scalar_mutation(self):
        """
        The probability (between 0 and 1) that a scalar value will be mutated.
        """
        return self._p_scalar_mutation

    @property
    def scalar_range_sigma(self):
        """
        When mutating a scalar value, the sigma of the normal distribution
        from which the change is taken is calculated as the range of the
        property, multiplied by this value.
        """
        return self._scalar_range_sigma

    @property
    def p_color_mutation(self):
        """
        The probability (between 0 and 1) that a color value will be mutated.
        """
        return self._p_color_mutation

    @property
    def color_sigma(self):
        """
        When mutating a color value, the sigma of the normal distribution
        from which the change is taken.
        """
        return self._color_sigma
