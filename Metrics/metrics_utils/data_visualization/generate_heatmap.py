import matplotlib.pyplot as plt


def generate_heatmap(matrix, title, file_path):
    plt.imshow(matrix, cmap='viridis', origin='upper')
    plt.colorbar()
    plt.title(title)
    plt.savefig(file_path)
    plt.show()
