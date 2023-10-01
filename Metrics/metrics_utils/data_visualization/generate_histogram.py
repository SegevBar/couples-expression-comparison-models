import matplotlib.pyplot as plt


def generate_double_histogram(couples, strangers, title, file_path):
    plt.hist([couples, strangers], bins=10, label=['couples', 'strangers'])
    plt.title(title)
    plt.legend(loc='upper right')
    plt.savefig(file_path)
    plt.show()


