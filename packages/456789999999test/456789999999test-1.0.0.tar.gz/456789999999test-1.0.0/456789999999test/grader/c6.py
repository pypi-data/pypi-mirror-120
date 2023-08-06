from ..jupic import ImageClassification
import math

def evaluate_c6(jupic: ImageClassification) -> int:
    '''Evaluate competence 6: accuracy'''

    if jupic.dataset_total_images == 0:
        return 0

    tl_score = evaluate_accuracy_success_interpretation(
        jupic.model_categories, 
        jupic.tl_accuracy_categories, 
        jupic.tl_accuracy_interpretation,
    ) if jupic.tl_accuracy_analysis else evaluate_accuracy_fail_interpretation(
        jupic.tl_accuracy_interpretation, jupic.tl_accuracy_analysis_categories, 
        jupic.model_categories, jupic.tl_accuracy_categories,
    )

    ft_score = evaluate_accuracy_success_interpretation(
        jupic.model_categories, 
        jupic.ft_accuracy_categories, 
        jupic.ft_accuracy_interpretation
    ) if jupic.ft_accuracy_analysis else evaluate_accuracy_fail_interpretation(
        jupic.ft_accuracy_interpretation, jupic.ft_accuracy_analysis_categories, 
        jupic.model_categories, jupic.ft_accuracy_categories,
    )

    return math.floor(tl_score + ft_score) / 2
 
 
def evaluate_accuracy_success_interpretation(
    model_categories: list,
    accuracy_categories: list,
    accuracy_interpretation: str,
) -> int:
    '''Evalute success accuracy interpretation answer'''

    for c in model_categories:
        c_accuracy = 0.0
        
        for ac in accuracy_categories:
            for category in ac: 
                if c == category:
                    c_accuracy = ac[category]
        
        if c_accuracy < 0.9: 
            return 0

    return 2 if accuracy_interpretation else 1


def evaluate_accuracy_fail_interpretation(
    accuracy_interpretation: str,
    accuracy_analysis_categories: list,
    model_categories: list,
    accuracy_categories: list,
) -> int:
    '''Evalute fail accuracy interpretation answer'''

    if accuracy_interpretation: 
        return 0
        
    low_categories = get_low_accuracy_categories(model_categories, accuracy_categories)

    if set(accuracy_analysis_categories) == set(low_categories):
        return 1 if accuracy_interpretation else 2

    return 0


def get_low_accuracy_categories(
    model_categories: list,
    accuracy_categories: list,
) -> list:
    '''Returns categories below 90% threshold accuracy'''

    low_accuracy_categories = []

    for c in model_categories:
        c_accuracy = 0.0
        
        for ac in accuracy_categories:
            for category in ac: 
                if c == category:
                    c_accuracy = ac[category]

        if c_accuracy < 0.9: 
            low_accuracy_categories.append(c)

    return low_accuracy_categories  