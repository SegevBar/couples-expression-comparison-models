import numpy
import matplotlib.pyplot as plt


def generate_double_histogram(couples, strangers, name):
    #max_val = max([max(couples), max(strangers)])
    #min_val = min([min(couples), min(strangers)])

    #bins = numpy.linspace(min_val, max_val, 10)
    plt.hist([couples, strangers], bins=10, label=['couples', 'strangers'])
    plt.legend(loc='upper right')
    plt.savefig(name)
    plt.show()


