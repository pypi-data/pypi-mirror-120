from ..jupic import ImageClassification
import math

def evaluate_c7(jupic: ImageClassification) -> int:
    '''Evalute competence 7: confusion matrix'''

    if jupic.dataset_total_images == 0:
        return 0

    tl_score = evaluate_confusion_matrix(
        jupic.model_categories, jupic.tl_confusion_matrix_mislabeled, 
        jupic.tl_confusion_matrix_mislabeled_real, jupic.tl_accuracy_interpretation,
    )

    ft_score = evaluate_confusion_matrix(
        jupic.model_categories, jupic.ft_confusion_matrix_mislabeled, 
        jupic.ft_confusion_matrix_mislabeled_real, jupic.ft_accuracy_interpretation,
    )

    return math.floor(tl_score + ft_score) / 2


def evaluate_confusion_matrix(
    model_categories: list,
    confusion_matrix_mislabeled: list,
    confusion_matrix_mislabeled_real: list,
    confusion_matrix_interpretation: str,
) -> int:
    '''Evaluate confusion matrix answers'''
    mislabeled_identified = 0

    for index, mislabeled in enumerate(confusion_matrix_mislabeled):
        for c in model_categories:
            for category in mislabeled: 
                if category == c \
                    and set(confusion_matrix_mislabeled[index][c]) == \
                        set(confusion_matrix_mislabeled_real[index][c]):
                            mislabeled_identified += 1

    if mislabeled_identified == len(model_categories):
        has_mislabel = False

        for c in confusion_matrix_mislabeled_real:
           for mislabeled in c:
               if len(mislabeled) > 0:
                   has_mislabel = True

        if confusion_matrix_interpretation:
            return 1 if has_mislabel else 2
        else:
            return 2 if has_mislabel else 1
    
    return 0