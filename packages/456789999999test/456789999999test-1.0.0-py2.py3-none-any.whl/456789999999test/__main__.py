from .jupic import ImageClassification
from .grader import evaluate
from .json import write_json
from .ninja_robot import get_ninja_robot
from .pdf import PDFWriter

jupic = ImageClassification()
###### Model
jupic.set_model_categories(['Aroeira','Jeriva','Pitangueira','Embauba', 'Mulungu', 'Capororoca'])
jupic.set_model_correctly_labeled_images(100)
###### Dataset
jupic.set_dataset_categories_images([
    { 'Aroeira': 20 }, 
    { 'Capororoca': 20 }, 
    { 'Embauba': 20 }, 
    { 'Jeriva': 20 }, 
    { 'Mulungu': 20 }, 
    { 'Pitangueira': 20 }
])
jupic.set_dataset_total_images(100)
###### Transfer Learning
jupic.set_tl_models(["resnet50", "resnet32"])
jupic.set_tl_epochs([1, 2])
jupic.set_tl_learning_rates([0.01, 0.02])
jupic.set_tl_trained(True)
##### Accuracy - Transfer Learning
jupic.set_tl_accuracy_categories([
    { 'Aroeira': 0.9 }, 
    { 'Capororoca': 0.9 }, 
    { 'Embauba': 0.9 }, 
    { 'Jeriva': 0.9 }, 
    { 'Mulungu': 0.9 }, 
    { 'Pitangueira': 0.9 }
])
jupic.set_tl_accuracy_analysis(True)
jupic.set_tl_accuracy_analysis_categories(["Aroeira", "Capororoca", "Embauba", "Jeriva", "Mulungu", "Pitangueira"])
jupic.set_tl_accuracy_interpretation(False)
##### Confusion matrix- Transfer Learning
jupic.set_tl_confusion_matrix_mislabeled_real([{'Pitangueira': ['Capororoca', 'Aroeira', 'Embauba', 'Mulungu']}, {'Jeriva': []}, {'Capororoca': ['Jeriva', 'Aroeira']}, {'Mulungu': []}, {'Embauba': []}, {'Aroeira': ['Pitangueira', 'Embauba', 'Jeriva', 'Mulungu']}])
jupic.set_tl_confusion_matrix_mislabeled([{'Pitangueira': ['Aroeira', 'Capororoca', 'Embauba', 'Mulungu']}, {'Jeriva': []}, {'Capororoca': ['Aroeira', 'Jeriva']}, {'Mulungu': []}, {'Embauba': []}, {'Aroeira': ['Embauba', 'Jeriva', 'Mulungu', 'Pitangueira']}])
jupic.set_tl_confusion_matrix_interpretation(False)
##### Fine-Tuning
jupic.set_ft_unfreezed(True)
jupic.set_ft_learning_rate(True)
jupic.set_ft_trained(True)
##### Accuracy - Fine-Tuning
jupic.set_ft_accuracy_categories([
    { 'Aroeira': 0.1 }, 
    { 'Capororoca': 0.2 }, 
    { 'Embauba': 0.3 }, 
    { 'Jeriva': 0.4 }, 
    { 'Mulungu': 0.5 }, 
    { 'Pitangueira': 0.6 }
])
jupic.set_ft_accuracy_analysis("Falso")
jupic.set_ft_accuracy_analysis_categories(["Aroeira", "Capororoca", "Embauba", "Jeriva", "Mulungu", "Pitangueira"])
jupic.set_ft_accuracy_interpretation("Falso")
##### Confusion matrix - Fine-Tuning
jupic.set_ft_confusion_matrix_mislabeled_real([{'Pitangueira': ['Capororoca', 'Aroeira', 'Embauba', 'Mulungu']}, {'Jeriva': []}, {'Capororoca': ['Jeriva', 'Aroeira']}, {'Mulungu': []}, {'Embauba': []}, {'Aroeira': ['Pitangueira', 'Embauba', 'Jeriva', 'Mulungu']}])
jupic.set_ft_confusion_matrix_mislabeled([{'Pitangueira': ['Aroeira', 'Capororoca', 'Embauba', 'Mulungu']}, {'Jeriva': []}, {'Capororoca': ['Aroeira', 'Jeriva']}, {'Mulungu': []}, {'Embauba': []}, {'Aroeira': ['Embauba', 'Jeriva', 'Mulungu', 'Pitangueira']}])
jupic.set_ft_confusion_matrix_interpretation("Falso")
##### Performance
jupic.set_performance_tuning(2)
jupic.set_performance_tuning_text("Acurácia")
##### New objects
jupic.set_real_objects(['Aroeira', 'Aroeira', 'Aroeira', 'Aroeira', 'Aroeira'])
jupic.set_predicted_objects(['Aroeira', 'Aroeira', 'Aroeira', 'Aroeira', 'Aroeira'])
jupic.set_predicted_success_times(5)
jupic.set_predicted_success_interpretation("Verdadeiro")
# Documentation PDF
jupic.set_model_name("Modelo Teste")
jupic.set_model_date("26/08/2021")
jupic.set_model_version("v1.0.0")
jupic.set_model_task("Classificar a espécie de árvore de uma imagem de árvore capturada de um aplicativo Android em relação a 6 categorias de árvores nativas/endêmicas de SC/Brasil. ")
jupic.set_model_use_context('O modelo é utilizado como exemplo no contexto de ensino de na Educação Básica. Este modelo não foi treinado para ser utilizado em pesquisa na área de botânica.')
jupic.set_model_target_audience('Cidadãos (8+ anos), Foco em alunos do Ensino Médio')
jupic.set_model_risks('Risco de classificar erroneamente as espécies de árvores, porém se refere a classificação de árvores sem riscos à saúde dos usuários.')
jupic.set_model_task_type('Single-label classificação de imagens')
jupic.set_dataset_augmentation_size("224x224 pixels")
jupic.set_dataset_augmentation_type("rotate")
jupic.set_dataset_description('Conjunto de imagens de árvores (tipicamente a vista da árvore toda ou partes dentro do habitat natural (rua, praça,  parque etc.) capturada de um aplicativo Android')
jupic.set_dataset_origin("Conjunto de dados de árvores disponibilizado pela CnE")
jupic.set_dataset_validation_percentage(0.2)
jupic.set_dataset_labeler_name('Por biólogos (conjunto de dados CnE)')
jupic.set_tl_batch_size('200')
jupic.set_ft_learning_rate('0.005')
jupic.set_ft_epoch('35')
jupic.set_ethics_limitations('Esse modelo é limitado a somente 6 espécies nativas de árvores com um desempenho aceitável. Os resultados da classificação devem ser utilizados com cuidado sempre revisado por humanos.')
jupic.set_ethics_considerations('N/A')
jupic.set_author('C. Gresse von Wangenheim, R. M. Martins, A. Franz, G. Salvador, INCoD/INE/UFSC')

score = evaluate(jupic)
write_json(jupic)
get_ninja_robot(score['total_score'])
writer = PDFWriter('logo.png', 'dataset_distribution.png', 'tl_confusion_matrix.png', 
    'tl_top_losses.png', 'ft_confusion_matrix.png', 'ft_top_losses.png') 
writer.write(jupic)

print(score)
