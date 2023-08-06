from ..jupic import ImageClassification

def evaluate_c3(jupic: ImageClassification) -> int:
    '''Evaluate competence 3: model predictions'''

    if jupic.dataset_total_images == 0:
        return 0
    
    ratio = jupic.model_correctly_labeled_images / jupic.dataset_total_images

    if ratio < 0.2:
        return 0
    if ratio > 0.2 and ratio < 0.99:
        return 1
    if ratio == 1:
        return 2
        
    return 0
