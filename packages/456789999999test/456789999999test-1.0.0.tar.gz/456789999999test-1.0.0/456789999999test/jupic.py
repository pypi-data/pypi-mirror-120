class ImageClassification:  
    '''Jupyter Notebook Image Classification training data'''

    # Model
    model_categories = []
    model_correctly_labeled_images = 0
    # Dataset
    dataset_categories_images = []
    dataset_total_images = 0
    # Transfer Learning
    tl_models = []
    tl_epochs = []
    tl_learning_rates = []
    tl_trained = False
    # Accuracy - Transfer Learning
    tl_accuracy_categories = []
    tl_accuracy_analysis = False
    tl_accuracy_analysis_categories = []
    tl_accuracy_interpretation = ''
    # Confusion matrix - Transfer Learning
    tl_confusion_matrix_mislabeled_real = []
    tl_confusion_matrix_mislabeled = []
    tl_confusion_matrix_interpretation = False
    # Fine-Tuning
    ft_unfreezed = False
    ft_learning_rate_found = False
    ft_trained = False
    # Accuracy - Fine-Tuning
    ft_accuracy_categories = []
    ft_accuracy_analysis = False
    ft_accuracy_analysis_categories = []
    ft_accuracy_interpretation = ''
    # Confusion matrix - Fine-Tuning
    ft_confusion_matrix_mislabeled_real = []
    ft_confusion_matrix_mislabeled = []
    ft_confusion_matrix_interpretation = False
    # Performance
    performance_tuning = 0
    performance_tuning_text = ''
    # New objects
    real_objects = []
    predicted_objects = []
    predicted_success_times = 0
    predicted_success_interpretation = False
    # Documentation PDF
    model_name = ''
    model_date = ''
    model_version = ''
    model_task = ''
    model_use_context = ''
    model_target_audience = ''
    model_risks = ''
    model_task_type = ''
    dataset_augmentation_size = ''
    dataset_augmentation_type = ''
    dataset_description = ''
    dataset_origin = ''
    dataset_validation_percentage = 0.0
    dataset_labeler_name = ''
    tl_batch_size = ''
    ft_learning_rate = ''
    ft_epoch = ''
    ethics_limitations = ''
    ethics_considerations = ''
    author = ''


    def set_model_categories(self, value: list) -> None:
        self.model_categories = value

    def set_model_correctly_labeled_images(self, value: int) -> None:
        self.model_correctly_labeled_images = value

    def set_dataset_categories_images(self, value: list) -> None:
        self.dataset_categories_images = value

    def set_dataset_total_images(self, value: int) -> None:
        self.dataset_total_images = value

    def set_dataset_total_images(self, value: int) -> None:
        self.dataset_total_images = value

    def set_tl_models(self, value: list) -> None:
        self.tl_models = value

    def set_tl_epochs(self, value: list) -> None:
        self.tl_epochs = value

    def set_tl_learning_rates(self, value: list) -> None:
        self.tl_learning_rates = value

    def set_tl_trained(self, value: bool) -> None:
        self.tl_trained = value

    def set_tl_accuracy_categories(self, value: list) -> None:
        self.tl_accuracy_categories = value

    def set_tl_accuracy_analysis(self, value: bool) -> None:
        self.tl_accuracy_analysis = value

    def set_tl_accuracy_analysis_categories(self, value: list) -> None:
        self.tl_accuracy_analysis_categories = value

    def set_tl_accuracy_interpretation(self, value: str) -> None:
        self.tl_accuracy_interpretation = value

    def set_tl_confusion_matrix_mislabeled_real(self, value: list) -> None:
        self.tl_confusion_matrix_mislabeled_real = value

    def set_tl_confusion_matrix_mislabeled(self, value: list) -> None:
        self.tl_confusion_matrix_mislabeled = value

    def set_tl_confusion_matrix_interpretation(self, value: bool) -> None:
        self.tl_confusion_matrix_interpretation = value

    def set_ft_unfreezed(self, value: bool) -> None:
        self.ft_unfreezed = value

    def set_ft_learning_rate_found(self, value: bool) -> None:
        self.ft_learning_rate_found = value

    def set_ft_trained(self, value: bool) -> None:
        self.ft_trained = value

    def set_ft_accuracy_categories(self, value: list) -> None:
        self.ft_accuracy_categories = value

    def set_ft_accuracy_analysis(self, value: bool) -> None:
        self.ft_accuracy_analysis = value

    def set_ft_accuracy_analysis_categories(self, value: list) -> None:
        self.ft_accuracy_analysis_categories = value

    def set_ft_accuracy_interpretation(self, value: str) -> None:
        self.ft_accuracy_interpretation = value

    def set_ft_confusion_matrix_mislabeled_real(self, value: list) -> None:
        self.ft_confusion_matrix_mislabeled_real = value

    def set_ft_confusion_matrix_mislabeled(self, value: list) -> None:
        self.ft_confusion_matrix_mislabeled = value

    def set_ft_confusion_matrix_interpretation(self, value: bool) -> None:
        self.ft_confusion_matrix_interpretation = value

    def set_performance_tuning(self, value: int) -> None:
        self.performance_tuning = value

    def set_performance_tuning_text(self, value: str) -> None:
        self.performance_tuning_text = value

    def set_real_objects(self, value: list) -> None:
        self.real_objects = value

    def set_predicted_objects(self, value: list) -> None:
        self.predicted_objects = value

    def set_predicted_success_times(self, value: int) -> None:
        self.predicted_success_times = value

    def set_predicted_success_interpretation(self, value: bool) -> None:
        self.predicted_success_interpretation = value

    def set_model_name(self, value: str) -> None:
        self.model_name = value

    def set_model_date(self, value: str) -> None:
        self.model_date = value

    def set_model_version(self, value: str) -> None:
        self.model_version = value

    def set_model_task(self, value: str) -> None:
        self.model_task = value

    def set_model_use_context(self, value: str) -> None:
        self.model_use_context = value

    def set_model_target_audience(self, value: str) -> None:
        self.model_target_audience = value

    def set_model_risks(self, value: str) -> None:
        self.model_risks = value

    def set_model_task_type(self, value: str) -> None:
        self.model_task_type = value

    def set_dataset_augmentation_size(self, value: str) -> None:
        self.dataset_augmentation_size = value

    def set_dataset_augmentation_type(self, value: str) -> None:
        self.dataset_augmentation_type = value

    def set_dataset_description(self, value: str) -> None:
        self.dataset_description = value

    def set_dataset_origin(self, value: str) -> None:
        self.dataset_origin = value

    def set_dataset_validation_percentage(self, value: str) -> None:
        self.dataset_validation_percentage = value

    def set_dataset_labeler_name(self, value: str) -> None:
        self.dataset_labeler_name = value

    def set_tl_batch_size(self, value: str) -> None:
        self.tl_batch_size = value

    def set_ft_learning_rate(self, value: str) -> None:
        self.ft_learning_rate = value

    def set_ft_epoch(self, value: str) -> None:
        self.ft_epoch = value

    def set_ethics_limitations(self, value: str) -> None:
        self.ethics_limitations = value

    def set_ethics_considerations(self, value: str) -> None:
        self.ethics_considerations = value

    def set_author(self, value: str) -> None:
        self.author = value