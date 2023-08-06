from ..jupic import ImageClassification

def evaluate_c10(jupic: ImageClassification) -> int:
    '''Evalute competence 10: new tests interpretation'''

    success_predictions = 0
    objects_qty = 5

    if len(jupic.real_objects) == 0 or len(jupic.predicted_objects) == 0:
        return 0

    for i in range(objects_qty):
        if jupic.real_objects[i] == jupic.predicted_objects[i] \
            and jupic.real_objects[i] and jupic.real_objects[i].strip(): 
                success_predictions += 1

    if jupic.predicted_success_times == success_predictions:
        if success_predictions == objects_qty and jupic.predicted_success_interpretation:
                return 2
        else:
            if not jupic.predicted_success_interpretation:
                return 2
    
    return 0
