from ..jupic import ImageClassification
import math

def evaluate_c1(jupic: ImageClassification) -> int:
    '''Evaluate competence 1: category images'''
    
    score = 0

    if len(jupic.model_categories) == 0: 
        return 0

    for c in jupic.model_categories:
        c_images = 0
        
        for ci in jupic.dataset_categories_images:
            for category in ci: 
                if c == category:
                    c_images = ci[category]

        if c_images < 6: 
            score += 0
        if c_images > 5 and c_images < 11: 
            score += 1
        if c_images > 10: 
            score += 2

    if score == 0:
        return 0

    return math.floor(score / len(jupic.model_categories))
    