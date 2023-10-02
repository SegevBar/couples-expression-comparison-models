import matplotlib.pyplot as plt


def generate_clustering_plot(data, labels, title, file_path):
    plt.scatter(data[:, 0], data[:, 1], c=labels)
    plt.title(title)
    plt.savefig(file_path)
    plt.show()
