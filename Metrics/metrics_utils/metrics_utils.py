from scipy.spatial.distance import cdist
import torch.nn.functional as F
import torch

# CUDA device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def find_min_dist(vector, vector_tensor):
    vector = vector.clone().detach()
    vector_tensor = vector_tensor.clone().detach()

    distances = cdist(vector.unsqueeze(0), vector_tensor, metric='euclidean')
    return distances.min().item()


def find_min_cosine(vector, vector_tensor):
    vector = vector.clone().detach()
    vector_tensor = vector_tensor.clone().detach()

    cosine_similarities = F.cosine_similarity(vector.unsqueeze(0), vector_tensor, dim=1)
    return cosine_similarities.min().item()

