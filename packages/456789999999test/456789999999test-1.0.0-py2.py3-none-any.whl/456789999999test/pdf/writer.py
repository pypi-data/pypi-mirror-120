from .elements import get_first_page_elements, get_second_page_elements, get_third_page_elements
from ..jupic import ImageClassification
from fpdf import Template
import json
from os import remove
from PyPDF2 import PdfFileMerger
from typing import List

# Document constants
page_title = 'Cartão de Modelo'
first_page_filename = 'pag_1.pdf'
second_page_filename = 'pag_2.pdf'
third_page_filename = 'pag_3.pdf'
final_filename='model_card.pdf'

class PDFWriter:
    '''Writes Model Card PDF'''

    logo_path = ''
    dataset_distribution_path = ''
    tl_confusion_matrix_path = ''
    tl_top_losses_path = ''
    ft_confusion_matrix_path = ''
    ft_top_losses_path = ''

    def __init__(
        self,
        logo_path: str,
        dataset_distribution_path: str,
        tl_confusion_matrix_path: str,
        tl_top_losses_path: str,
        ft_confusion_matrix_path: str,
        ft_top_losses_path: str,
    ):

        self.logo_path = logo_path
        self.dataset_distribution_path = dataset_distribution_path
        self.tl_confusion_matrix_path = tl_confusion_matrix_path
        self.tl_top_losses_path = tl_top_losses_path
        self.ft_confusion_matrix_path = ft_confusion_matrix_path
        self.ft_top_losses_path = ft_top_losses_path


    def write_first_page(
        self,
        jupic: ImageClassification, 
        filename: str,
    ):
        '''Writes first PDF page'''

        t = Template(format='A4', elements=get_first_page_elements(
            self.logo_path), title=page_title)
        t.add_page()

        t['logo'] = self.logo_path
        t['model_name'] = jupic.model_name
        t['model_date'] = jupic.model_date
        t['model_version'] = jupic.model_version
        t['model_task'] = jupic.model_task
        t['model_use_context'] = jupic.model_use_context
        t['model_target_audience'] = jupic.model_target_audience
        t['model_risks'] = jupic.model_risks
        t['model_task_type'] = jupic.model_task_type
        t['model_categories'] = ', '.join(jupic.model_categories)
        t['dataset_total_images'] = 'Total de {} imagens'.format(jupic.dataset_total_images)
        t['dataset_augmentation_type'] = jupic.dataset_augmentation_type
        t['dataset_augmentation_size'] = jupic.dataset_augmentation_size
        t['dataset_description'] = jupic.dataset_description
        t['dataset_origin'] = jupic.dataset_origin
        dataset_training_percentage = 1 - jupic.dataset_validation_percentage
        t['dataset_validation_percentage'] = \
            '{}% para treinamento ({} imagens), {}% para validação ({} imagens)'.format(
                int(dataset_training_percentage * 100), 
                int(jupic.dataset_total_images * dataset_training_percentage),
                int(jupic.dataset_validation_percentage * 100),
                int(jupic.dataset_total_images * jupic.dataset_validation_percentage)
            )

        t.render(filename)


    def write_second_page(
        self,
        jupic: ImageClassification, 
        filename: str,
    ):
        '''Writes second PDF page'''

        t = Template(format='A4', elements=get_second_page_elements(
            self.dataset_distribution_path, self.tl_confusion_matrix_path, self.tl_top_losses_path), title=page_title)
        t.add_page()

        t['dataset_distribution'] = self.dataset_distribution_path
        t['confusion_matrix'] = self.tl_confusion_matrix_path
        t['top_losses'] = self.tl_top_losses_path
        t['dataset_labeler_name'] = jupic.dataset_labeler_name
        t['model_date'] = jupic.model_date
        t['tl_model'] = jupic.tl_models[len(jupic.tl_models) - 1]
        t['tl_batch_size'] = jupic.tl_batch_size
        t['tl_epoch'] = jupic.tl_epochs[len(jupic.tl_epochs) - 1]
        t['tl_learning_rate'] = jupic.tl_learning_rates[len(jupic.tl_learning_rates) - 1]
        accuracy_categories_text = json.dumps(jupic.tl_accuracy_categories)
        t['tl_accuracy_categories'] = accuracy_categories_text.replace(
            '{', '').replace('}', '').replace('[', '').replace(']', '').replace("\"", '')

        t.render(filename)


    def write_third_page(
        self,
        jupic: ImageClassification, 
        filename: str,
    ):
        '''Writes third PDF page'''

        t = Template(format='A4', elements=get_third_page_elements(
            self.ft_confusion_matrix_path, self.ft_top_losses_path), title=page_title)
        t.add_page()

        t['confusion_matrix'] = self.ft_confusion_matrix_path
        t['top_losses'] = self.ft_top_losses_path
        t['ft_learning_rate'] = jupic.ft_learning_rate
        t['ft_epoch'] = jupic.ft_epoch
        accuracy_categories_text = json.dumps(jupic.ft_accuracy_categories)
        t['ft_accuracy_categories'] = accuracy_categories_text.replace(
            '{', '').replace('}', '').replace('[', '').replace(']', '').replace("\"", '')
        t['performance_tuning'] = self.handle_performance_tuning(jupic.performance_tuning)
        t['ethics_limitations'] = jupic.ethics_limitations
        t['ethics_considerations'] = jupic.ethics_considerations
        t['author'] = jupic.author

        t.render(filename)


    def handle_performance_tuning(
        self,
        value: int,
    ) -> str:
        '''Gets PDF text for a given performance_tuning value'''

        if value == 0:
            return 'Nenhum'
        if value == 1:
            return 'Um'
        if value == 2:
            return 'Vários'


    def merge_pdfs(
        self,
        final_filename: str, 
        *filenames: List[str],
    ): 
        '''Merges all PDFs into one'''

        pdf_merger = PdfFileMerger()

        for f in filenames:
            pdf_merger.append(f)

        pdf_merger.write(final_filename)

        for f in filenames:
            remove(f)


    def write(
        self,
        jupic: ImageClassification,
    ): 
        '''Writes PDF'''

        self.write_first_page(jupic, first_page_filename)
        self.write_second_page(jupic, second_page_filename)
        self.write_third_page(jupic, third_page_filename)
        self.merge_pdfs(final_filename, first_page_filename, second_page_filename, third_page_filename)