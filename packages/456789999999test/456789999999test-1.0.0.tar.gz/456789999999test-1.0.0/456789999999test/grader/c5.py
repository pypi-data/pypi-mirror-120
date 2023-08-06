from ..jupic import ImageClassification

def evaluate_c5(jupic: ImageClassification) -> int:
    '''Evaluate competence 5: Fine-Tuning'''

    if not jupic.ft_unfreezed: 
        return 0

    if jupic.ft_unfreezed:
            return 2 if jupic.ft_trained and jupic.ft_learning_rate_found else 1

    return 0