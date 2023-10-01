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


def find_min_dist_cuda(part1, part2, batch_size=1000):
    min_distances = []

    for i in range(0, len(part1), batch_size):
        batch_part1 = part1[i:i + batch_size]
        distances = torch.cdist(batch_part1.unsqueeze(1), part2.unsqueeze(0)).min(dim=2).values
        min_distances.append(distances)
    return torch.cat(min_distances, dim=0)


def find_min_cosine(vector, vector_tensor):
    vector = vector.clone().detach()
    vector_tensor = vector_tensor.clone().detach()

    cosine_similarities = F.cosine_similarity(vector.unsqueeze(0), vector_tensor, dim=1)
    return cosine_similarities.min().item()


def find_min_cos_cuda(part1, part2, batch_size=1000):
    matrix1_normalized = part1 / part1.norm(dim=1)[:, None]
    matrix2_normalized = part2 / part2.norm(dim=1)[:, None]
    max_cosine_similarities = torch.zeros(part1.shape[0], device='cuda')

    for i in range(0, part1.shape[0], batch_size):
        batch_matrix1 = matrix1_normalized[i:i + batch_size]
        batch_similarity = torch.mm(batch_matrix1, matrix2_normalized.T)
        batch_max_similarity, _ = batch_similarity.max(dim=1)
        max_cosine_similarities[i:i + batch_size] = batch_max_similarity
    return max_cosine_similarities
