from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity


def _run_closest_exp(part1, part2):
    for idx, expression in enumerate(part1):
        similarities = cosine_similarity([expression], part2)
        most_similar_idx = similarities.argmax()
        most_similar_value = similarities[0, most_similar_idx]
        return idx, most_similar_idx, most_similar_value


def _run_metric_couple(part1, part2):
    distances = distance.cdist(part1, part2, 'euclidean')
    return distances.mean()


class AvgMinDist:
    @staticmethod
    def run_metric(coupling, participants_exp_rep):
        print("Running Average Minimal Distance Metric")
        results = {}

        for couple in coupling:
            results.update({couple: {(_run_metric_couple(participants_exp_rep[couple[0]], participants_exp_rep[couple[1]])),
                            _run_closest_exp(participants_exp_rep[couple[0]], participants_exp_rep[couple[1]])}})
