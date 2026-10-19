"""Inferencia Bayesiana simple para cuantificar riesgo de fallo."""

from scipy.special import expit

DEFAULT_PRIOR = 0.05


def likelihood_from_entropy(entropy_score: float, alpha: float = 8.0) -> float:
    return float(expit(alpha * (entropy_score - 0.5)))


def bayes_posterior(prior: float, likelihood: float, false_likelihood: float = None) -> float:
    if false_likelihood is None:
        false_likelihood = max(1e-6, 1.0 - likelihood) * 0.5
    numerator = likelihood * prior
    denominator = numerator + false_likelihood * (1 - prior)
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def estimate_failure_probability(entropy_score: float, prior: float = DEFAULT_PRIOR) -> float:
    likelihood = likelihood_from_entropy(entropy_score)
    false_likelihood = max(1e-6, 1.0 - likelihood) * 0.5
    return bayes_posterior(prior, likelihood, false_likelihood)
