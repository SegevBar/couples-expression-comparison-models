import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from itertools import cycle


def generate_tsne(matrix, title, file_path, labels=None):
    tsne = TSNE(n_components=2, random_state=42)
    tsne_result = tsne.fit_transform(matrix)

    colors = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

    plt.figure(figsize=(16, 12))
    for label in set(labels):
        mask = labels == label
        plt.scatter(tsne_result[mask, 0], tsne_result[mask, 1], label=f'Label {label}', alpha=0.5, s=10, color=next(colors))

    plt.title(title)
    plt.xlabel('t-SNE Dimension 1')
    plt.ylabel('t-SNE Dimension 2')
    plt.legend()
    print("saving t-SNE plot")
    plt.savefig(file_path, dpi=300)
    plt.show()
