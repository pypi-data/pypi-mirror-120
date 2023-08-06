from ..jupic import ImageClassification

def evaluate_c8(jupic: ImageClassification) -> int:
    '''Evalute competence 8: performance tuning'''

    if jupic.performance_tuning == 0:
        return 0

    if jupic.performance_tuning == 1 \
        or jupic.performance_tuning == 2:
            
            if jupic.performance_tuning_text and jupic.performance_tuning_text.strip():
                return 2
            if not jupic.performance_tuning_text and jupic.performance_tuning_text.strip():
                return 1

    return 0