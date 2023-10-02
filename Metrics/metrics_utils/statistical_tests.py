import numpy as np

from scipy.stats import mannwhitneyu
from scipy import stats


def perform_mannwhitneyu_test(group1_name, group1_data, group2_name, group2_data):
    print(f"{group1_name} (mean, std): ", np.mean(group1_data), " , ", np.std(group1_data))
    print(f"{group2_name} (mean, std): ", np.mean(group2_data), " , ", np.std(group2_data))

    # Perform the Mann-Whitney U test
    statistic, p_value = mannwhitneyu(group1_data, group2_data)
    alpha = 0.05
    print("mann-whitneyu statistic: ", statistic)
    print(f"P-Value = {p_value},  alpha = {alpha}")
    if p_value < alpha:
        print("Reject the null hypothesis: The distributions are different.")
    else:
        print("Fail to reject the null hypothesis: The distributions are similar.")


def perform_t_test(group1_name, group1_data, group2_name, group2_data):
    print(f"{group1_name} (mean, std): ", np.mean(group1_data), " , ", np.std(group1_data))
    print(f"{group2_name} (mean, std): ", np.mean(group2_data), " , ", np.std(group2_data))

    t_statistic, p_value = stats.ttest_ind(group1_data, group2_data)
    alpha = 0.05
    print("t-statistic: ", t_statistic)
    print(f"P-Value = {p_value},  alpha = {alpha}")
    if p_value < alpha:
        print("Reject the null hypothesis: The means are significantly different.")
    else:
        print("Fail to reject the null hypothesis: The means are not significantly different.")
