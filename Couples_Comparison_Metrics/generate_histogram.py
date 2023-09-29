import numpy
from matplotlib import pyplot


def generate_double_histogram(x, y):
    bins = numpy.linspace(0, max([max(x), max(y)]), 10)

    pyplot.hist(x, bins, alpha=0.5, label='x')
    pyplot.hist(y, bins, alpha=0.5, label='y')
    pyplot.legend(loc='upper right')
    pyplot.show()

