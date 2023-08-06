from typing import List

# Document constants
frame_x1 = 15.0
frame_x2 = 195.0
offset = 3.0
left_text_x1 = frame_x1 + offset
vertical_divider_x = 80.0
right_text_x1 = vertical_divider_x + offset
highlight_color = 0x2A97DF
text_size = 11.0

def get_first_page_elements(
    logo_path: str,
) -> List[str]: 
    '''Return PDF first page fpdf elements'''

    return [
        # Header
        { 
            'name': 'logo', 'type': 'I', 
            'x1': 137.0, 'y1': 19.0, 
            'x2': 195.0, 'y2': 37.0, 
            'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'R', 'text': logo_path, 'priority': 2, 
        },
        { 
            'name': 'card_name', 'type': 'T', 
            'x1': left_text_x1, 'y1': 20.0, 
            'x2': 115.0, 'y2': 37.5, 
            'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': highlight_color, 'background': 0, 
            'align': 'L', 'text': 'Cartão de Modelo', 'priority': 2, 
        },

        # Document frame
        { 
            'name': 'frame', 'type': 'B', 
            'x1': frame_x1, 'y1': 15.0, 
            'x2': 195.0, 'y2': 282.0, 
            'font': 'Arial', 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 1, 
        },
        { 
            'name': 'line_1', 'type': 'L', 
            'x1': frame_x1, 'y1': 40.0, 
            'x2': frame_x2, 'y2': 40.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },
        { 
            'name': 'vertical_divider_1', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 40.0, 
            'x2': vertical_divider_x, 'y2': 70.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Nome do modelo
        { 
            'name': 'text_1', 'type': 'T', 
            'x1': left_text_x1, 'y1': 40.0, 
            'x2': frame_x2, 'y2': 50.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Nome do modelo', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'model_name', 'type': 'T', 
            'x1': right_text_x1, 'y1': 40.0, 
            'x2': frame_x2, 'y2': 50.0, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 
        },
        { 
            'name': 'line_2', 'type': 'L', 
            'x1': frame_x1, 'y1': 50.0, 
            'x2': frame_x2, 'y2': 50.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Data
        { 
            'name': 'text_3', 'type': 'T', 
            'x1': left_text_x1, 'y1': 50.0, 
            'x2': frame_x2, 'y2': 60.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Data', 'priority': 0, 
        },
        { 
            'name': 'model_date', 'type': 'T', 
            'x1': right_text_x1, 'y1': 50.0, 
            'x2': frame_x2, 'y2': 60.0, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'line_3', 'type': 'L', 
            'x1': frame_x1, 'y1': 60.0, 
            'x2': frame_x2, 'y2': 60.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Versão
        { 
            'name': 'text_5', 'type': 'T', 
            'x1': left_text_x1, 'y1': 60.0, 
            'x2': frame_x2, 'y2': 70.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Versão', 'priority': 0, 
        },
        { 
            'name': 'model_version', 'type': 'T', 
            'x1': right_text_x1, 'y1': 60.0, 
            'x2': frame_x2, 'y2': 70.0, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'line_4', 'type': 'L', 
            'x1': frame_x1, 'y1': 70.0, 
            'x2': frame_x2, 'y2': 70.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Objetivo do modelo de ML
        { 
            'name': 'text_7', 'type': 'T', 
            'x1': left_text_x1, 'y1': 70.0, 
            'x2': frame_x2, 'y2': 80.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': highlight_color, 'background': 0, 
            'align': 'L', 'text': 'Objetivo do modelo de ML', 'priority': 0, 
        },
        { 
            'name': 'line_5', 'type': 'L', 
            'x1': frame_x1, 'y1': 80.0, 
            'x2': frame_x2, 'y2': 80.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },
        { 
            'name': 'vertical_divider_2', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 80.0, 
            'x2': vertical_divider_x, 'y2': 190.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Tarefa
        { 
            'name': 'text_9', 'type': 'T', 
            'x1': left_text_x1, 'y1': 80.0, 
            'x2': frame_x2, 'y2': 90.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Tarefa', 'priority': 0, 
        },
        { 
            'name': 'model_task', 'type': 'T', 
            'x1': right_text_x1, 'y1': 82.5, 
            'x2': frame_x2, 'y2': 87.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True, 
        },
        { 
            'name': 'line_6', 'type': 'L', 
            'x1': frame_x1, 'y1': 105.0, 
            'x2': frame_x2, 'y2': 105.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Contexto de uso
        { 
            'name': 'text_10', 'type': 'T', 
            'x1': left_text_x1, 'y1': 105.0, 
            'x2': frame_x2, 'y2': 115.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Contexto de uso', 'priority': 0, 
        },
        { 
            'name': 'model_use_context', 'type': 'T', 
            'x1': right_text_x1, 'y1': 107.5, 
            'x2': frame_x2, 'y2': 112.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True, 
        },
        { 
            'name': 'line_7', 'type': 'L', 
            'x1': frame_x1, 'y1': 125.0, 
            'x2': frame_x2, 'y2': 125.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Público alvo
        { 
            'name': 'text_12', 'type': 'T', 
            'x1': left_text_x1, 'y1': 125.0, 
            'x2': frame_x2, 'y2': 135.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Público alvo', 'priority': 0, 
        },
        { 
            'name': 'model_target_audience', 'type': 'T', 
            'x1': right_text_x1, 'y1': 127.5, 
            'x2': frame_x2, 'y2': 132.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True, 
        },
        { 
            'name': 'line_8', 'type': 'L', 
            'x1': frame_x1, 'y1': 140.0, 
            'x2': frame_x2, 'y2': 140.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Riscos
        { 
            'name': 'text_14', 'type': 'T', 
            'x1': left_text_x1, 'y1': 140.0, 
            'x2': frame_x2, 'y2': 150.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Riscos', 'priority': 0, 
        },
        { 
            'name': 'model_risks', 'type': 'T', 
            'x1': right_text_x1, 'y1': 142.5, 
            'x2': frame_x2, 'y2': 147.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True, 
        },
        { 
            'name': 'line_9', 'type': 'L', 
            'x1': frame_x1, 'y1': 160.0, 
            'x2': frame_x2, 'y2': 160.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Tipo da tarefa
        { 
            'name': 'text_15', 'type': 'T', 
            'x1': left_text_x1, 'y1': 160.0, 
            'x2': frame_x2, 'y2': 170.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Tipo da tarefa', 'priority': 0, 
        },
        { 
            'name': 'model_task_type', 'type': 'T', 
            'x1': right_text_x1, 'y1': 160.0, 
            'x2': frame_x2, 'y2': 170.0, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True, 
        },
        { 
            'name': 'line_10', 'type': 'L', 
            'x1': frame_x1, 'y1': 170.0, 
            'x2': frame_x2, 'y2': 170.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Categorias
        { 
            'name': 'text_17', 'type': 'T', 
            'x1': left_text_x1, 'y1': 170.0, 
            'x2': frame_x2, 'y2': 180.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Categorias', 'priority': 0, 
        },
        { 
            'name': 'model_categories', 'type': 'T', 
            'x1': right_text_x1, 'y1': 172.5, 
            'x2': frame_x2, 'y2': 177.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': None, 'priority': 0, 'multiline': True, 
        },
        { 
            'name': 'line_11', 'type': 'L', 
            'x1': frame_x1, 'y1': 190.0, 
            'x2': frame_x2, 'y2': 190.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Conjunto de dados
        { 
            'name': 'text_19', 'type': 'T', 
            'x1': left_text_x1, 'y1': 190.0, 
            'x2': frame_x2, 'y2': 200.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': highlight_color, 'background': 0, 
            'align': 'L', 'text': 'Conjunto de dados', 'priority': 0, 
        },
        { 
            'name': 'line_12', 'type': 'L', 
            'x1': frame_x1, 'y1': 200.0, 
            'x2': frame_x2, 'y2': 200.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },
        { 
            'name': 'vertical_divider_3', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 200.0, 
            'x2': vertical_divider_x, 'y2': 282.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Descrição dos dados
        { 
            'name': 'text_20', 'type': 'T', 
            'x1': left_text_x1, 'y1': 200.0, 
            'x2': frame_x2, 'y2': 210.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Descrição dos dados', 'priority': 0, 
        },
        { 
            'name': 'dataset_description', 'type': 'T', 
            'x1': right_text_x1, 'y1': 202.5, 
            'x2': frame_x2, 'y2': 207.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True, 
        },
        { 
            'name': 'line_13', 'type': 'L', 
            'x1': frame_x1, 'y1': 220.0, 
            'x2': frame_x2, 'y2': 220.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Origem dos dados
        { 
            'name': 'text_22', 'type': 'T', 
            'x1': left_text_x1, 'y1': 220.0, 
            'x2': frame_x2, 'y2': 230.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Origem dos dados', 'priority': 0, 
        },
        { 
            'name': 'dataset_origin', 'type': 'T', 
            'x1': right_text_x1, 'y1': 220.0, 
            'x2': frame_x2, 'y2': 230.0, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True
        },
        { 
            'name': 'line_14', 'type': 'L', 
            'x1': frame_x1, 'y1': 230.0, 
            'x2': frame_x2, 'y2': 230.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Quantidade de dados
        { 
            'name': 'text_24', 'type': 'T', 
            'x1': left_text_x1, 'y1': 230.0, 
            'x2': frame_x2, 'y2': 240.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Quantidade total de dados', 'priority': 0, 
        },
        { 
            'name': 'dataset_total_images', 'type': 'T', 
            'x1': right_text_x1, 'y1': 230.0, 
            'x2': frame_x2, 'y2': 240.0, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'line_15', 'type': 'L', 
            'x1': frame_x1, 'y1': 240.0, 
            'x2': frame_x2, 'y2': 240.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Tipos de aumento de dados aplicados
        { 
            'name': 'text_26', 'type': 'T', 
            'x1': left_text_x1, 'y1': 242.5, 
            'x2': right_text_x1, 'y2': 247.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Tipos de aumento de dados aplicados', 'priority': 0, 'multiline': True,
        },
        { 
            'name': 'dataset_augmentation_type', 'type': 'T', 
            'x1': right_text_x1, 'y1': 240.0, 
            'x2': frame_x2, 'y2': 250.0, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'line_16', 'type': 'L', 
            'x1': frame_x1, 'y1': 255.0, 
            'x2': frame_x2, 'y2': 255.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Tamanho de imagens
        { 
            'name': 'text_28', 'type': 'T', 
            'x1': left_text_x1, 'y1': 255.0, 
            'x2': frame_x2, 'y2': 265.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Tamanho de imagens', 'priority': 0, 
        },
        { 
            'name': 'dataset_augmentation_size', 'type': 'T', 
            'x1': right_text_x1, 'y1': 255.0, 
            'x2': frame_x2, 'y2': 265.0, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'line_16', 'type': 'L', 
            'x1': frame_x1, 'y1': 265.0, 
            'x2': frame_x2, 'y2': 265.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  
        
        # Divisão do conjunto de dados
        { 
            'name': 'text_30', 'type': 'T', 
            'x1': left_text_x1, 'y1': 267.5, 
            'x2': right_text_x1, 'y2': 272.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Divisão do conjunto de dados', 'priority': 0, 'multiline': True,
        },
        { 
            'name': 'dataset_validation_percentage', 'type': 'T', 
            'x1': right_text_x1, 'y1': 267.5, 
            'x2': frame_x2, 'y2': 272.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True,
        },
    ]


def get_second_page_elements(
    dataset_distribution_path: str,
    tl_confusion_matrix_path: str,
    tl_top_losses_path: str,
) -> List[str]: 
    '''Return PDF second page fpdf elements'''

    return [
        # Document frame
        { 
            'name': 'frame', 'type': 'B', 
            'x1': frame_x1, 'y1': 15.0, 
            'x2': 195.0, 'y2': 282.0, 
            'font': 'Arial', 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 1, 
        },
        { 
            'name': 'vertical_divider_1', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 15.0, 
            'x2': vertical_divider_x, 'y2': 100.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Distribuição dos dados por categoria
        { 
            'name': 'text_1', 'type': 'T', 
            'x1': left_text_x1, 'y1': 17.5, 
            'x2': right_text_x1, 'y2': 22.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Distribuição dos dados por categoria', 'priority': 0, 'multiline': True,
        },
        { 
            'name': 'dataset_distribution', 'type': 'I', 
            'x1': right_text_x1, 'y1': 17.5, 
            'x2': 192.5, 'y2': 82.5, 
            'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'R', 'text': dataset_distribution_path, 'priority': 2, 
            # 'align': 'R', 'text': '', 'priority': 2, 
        },
        { 
            'name': 'line_1', 'type': 'L', 
            'x1': frame_x1, 'y1': 85.0, 
            'x2': frame_x2, 'y2': 85.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Labeling
        { 
            'name': 'text_2', 'type': 'T', 
            'x1': left_text_x1, 'y1': 85.0, 
            'x2': frame_x2, 'y2': 95.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Labeling', 'priority': 0, 
        },
        { 
            'name': 'dataset_labeler_name', 'type': 'T', 
            'x1': right_text_x1, 'y1': 87.5, 
            'x2': frame_x2, 'y2': 92.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True, 
        },
        { 
            'name': 'line_2', 'type': 'L', 
            'x1': frame_x1, 'y1': 100.0, 
            'x2': frame_x2, 'y2': 100.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Treinamento - Transfer Learning
        { 
            'name': 'text_3', 'type': 'T', 
            'x1': left_text_x1, 'y1': 100.0, 
            'x2': frame_x2, 'y2': 110.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': highlight_color, 'background': 0, 
            'align': 'L', 'text': 'Treinamento - Transfer Learning', 'priority': 0, 
        },
        { 
            'name': 'line_3', 'type': 'L', 
            'x1': frame_x1, 'y1': 110.0, 
            'x2': frame_x2, 'y2': 110.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },
        { 
            'name': 'vertical_divider_2', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 110.0, 
            'x2': vertical_divider_x, 'y2': 150.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Tipo de modelo
        {
            'name': 'text_4', 'type': 'T', 
            'x1': left_text_x1, 'y1': 110.0, 
            'x2': frame_x2, 'y2': 120.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Tipo de modelo', 'priority': 0, 
        },
        { 
            'name': 'tl_model', 'type': 'T', 
            'x1': right_text_x1, 'y1': 112.5, 
            'x2': frame_x2, 'y2': 117.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'line_4', 'type': 'L', 
            'x1': frame_x1, 'y1': 120.0, 
            'x2': frame_x2, 'y2': 120.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Tamanho do batch
        {
            'name': 'text_4', 'type': 'T', 
            'x1': left_text_x1, 'y1': 120.0, 
            'x2': frame_x2, 'y2': 130.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Tamanho do batch', 'priority': 0, 
        },
        { 
            'name': 'tl_batch_size', 'type': 'T', 
            'x1': right_text_x1, 'y1': 125.5, 
            'x2': frame_x2, 'y2': 127.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'line_4', 'type': 'L', 
            'x1': frame_x1, 'y1': 130.0, 
            'x2': frame_x2, 'y2': 130.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Quantidade de épocas
        {
            'name': 'text_5', 'type': 'T', 
            'x1': left_text_x1, 'y1': 130.0, 
            'x2': frame_x2, 'y2': 140.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Quantidade de épocas', 'priority': 0, 
        },
        { 
            'name': 'tl_epoch', 'type': 'T', 
            'x1': right_text_x1, 'y1': 135.5, 
            'x2': frame_x2, 'y2': 137.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'line_5', 'type': 'L', 
            'x1': frame_x1, 'y1': 140.0, 
            'x2': frame_x2, 'y2': 140.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Taxa de aprendizagem
        {
            'name': 'text_5', 'type': 'T', 
            'x1': left_text_x1, 'y1': 140.0, 
            'x2': frame_x2, 'y2': 150.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Taxa de aprendizagem', 'priority': 0, 
        },
        { 
            'name': 'tl_learning_rate', 'type': 'T', 
            'x1': right_text_x1, 'y1': 145.5, 
            'x2': frame_x2, 'y2': 147.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 
        },
        { 
            'name': 'line_5', 'type': 'L', 
            'x1': frame_x1, 'y1': 150.0, 
            'x2': frame_x2, 'y2': 150.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Avaliação - Transfer Learning
        { 
            'name': 'text_6', 'type': 'T', 
            'x1': left_text_x1, 'y1': 150.0, 
            'x2': frame_x2, 'y2': 160.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': highlight_color, 'background': 0, 
            'align': 'L', 'text': 'Avaliação - Transfer Learning', 'priority': 0, 
        },
        { 
            'name': 'line_6', 'type': 'L', 
            'x1': frame_x1, 'y1': 160.0, 
            'x2': frame_x2, 'y2': 160.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },
        { 
            'name': 'vertical_divider_3', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 160.0, 
            'x2': vertical_divider_x, 'y2': 282.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Acurácia por categoria
        {
            'name': 'text_7', 'type': 'T', 
            'x1': left_text_x1, 'y1': 160.0, 
            'x2': frame_x2, 'y2': 170.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Acurácia por categoria', 'priority': 0, 
        },
        { 
            'name': 'tl_accuracy_categories', 'type': 'T', 
            'x1': right_text_x1, 'y1': 161.5, 
            'x2': frame_x2, 'y2': 166.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True,
        },
        { 
            'name': 'line_7', 'type': 'L', 
            'x1': frame_x1, 'y1': 200.0, 
            'x2': frame_x2, 'y2': 200.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Matriz de confusão
        {
            'name': 'text_8', 'type': 'T', 
            'x1': left_text_x1, 'y1': 203.5, 
            'x2': frame_x2, 'y2': 205.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Matriz de confusão', 'priority': 0, 
        },
        { 
            'name': 'confusion_matrix', 'type': 'I', 
            'x1': frame_x1 + 5, 'y1': 212.5, 
            'x2': vertical_divider_x - 5, 'y2': 275.0, 
            'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'R', 'text': tl_confusion_matrix_path, 'priority': 2, 
        },

        # Top 4 losses
        {
            'name': 'text_9', 'type': 'T', 
            'x1': right_text_x1, 'y1': 203.5, 
            'x2': frame_x2, 'y2': 205.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Top 4 losses', 'priority': 0, 
        },
        {
            'name': 'top_losses', 'type': 'I', 
            'x1': vertical_divider_x + 15, 'y1': 207.5, 
            'x2': frame_x2 - 15, 'y2': 280.0, 
            'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'R', 'text': tl_top_losses_path, 'priority': 2, 
        },
    ]


def get_third_page_elements(
    ft_confusion_matrix_path: str,
    ft_top_losses_path: str,
) -> List[str]: 
    '''Return PDF third page fpdf elements'''

    return [
        # Document frame
        { 
            'name': 'frame', 'type': 'B', 
            'x1': frame_x1, 'y1': 15.0, 
            'x2': 195.0, 'y2': 282.0, 
            'font': 'Arial', 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 1, 
        },
        { 
            'name': 'vertical_divider_1', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 25.0, 
            'x2': vertical_divider_x, 'y2': 45.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Treinamento - Fine Tuning
        { 
            'name': 'text_1', 'type': 'T', 
            'x1': left_text_x1, 'y1': 17.5, 
            'x2': right_text_x1, 'y2': 22.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': highlight_color, 'background': 0, 
            'align': 'L', 'text': 'Treinamento - Fine Tuning', 'priority': 0,
        },
        { 
            'name': 'line_1', 'type': 'L', 
            'x1': frame_x1, 'y1': 25.0, 
            'x2': frame_x2, 'y2': 25.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Taxa de aprendizagem
        {
            'name': 'text_2', 'type': 'T', 
            'x1': left_text_x1, 'y1': 25.0, 
            'x2': frame_x2, 'y2': 35.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Taxa de aprendizagem', 'priority': 0, 
        },
        { 
            'name': 'ft_learning_rate', 'type': 'T', 
            'x1': right_text_x1, 'y1': 27.5, 
            'x2': frame_x2, 'y2': 32.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'line_2', 'type': 'L', 
            'x1': frame_x1, 'y1': 35.0, 
            'x2': frame_x2, 'y2': 35.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Quantidade de épocas
        {
            'name': 'text_3', 'type': 'T', 
            'x1': left_text_x1, 'y1': 35.0, 
            'x2': frame_x2, 'y2': 45.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Quantidade de épocas', 'priority': 0, 
        },
        { 
            'name': 'ft_epoch', 'type': 'T', 
            'x1': right_text_x1, 'y1': 37.5, 
            'x2': frame_x2, 'y2': 42.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': False,
        },
        { 
            'name': 'line_3', 'type': 'L', 
            'x1': frame_x1, 'y1': 45.0, 
            'x2': frame_x2, 'y2': 45.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Avaliação - Fine Tuning
        { 
            'name': 'text_4', 'type': 'T', 
            'x1': left_text_x1, 'y1': 47.5, 
            'x2': right_text_x1, 'y2': 52.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': highlight_color, 'background': 0, 
            'align': 'L', 'text': 'Avaliação - Fine Tuning', 'priority': 0,
        },
        { 
            'name': 'line_4', 'type': 'L', 
            'x1': frame_x1, 'y1': 55.0, 
            'x2': frame_x2, 'y2': 55.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },
        { 
            'name': 'vertical_divider_2', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 55.0, 
            'x2': vertical_divider_x, 'y2': 172.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Acurácia por categoria
        {
            'name': 'text_5', 'type': 'T', 
            'x1': left_text_x1, 'y1': 55.0, 
            'x2': frame_x2, 'y2': 65.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Acurácia por categoria', 'priority': 0, 
        },
        { 
            'name': 'ft_accuracy_categories', 'type': 'T', 
            'x1': right_text_x1, 'y1': 56.5, 
            'x2': frame_x2, 'y2': 61.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True,
        },
        { 
            'name': 'line_5', 'type': 'L', 
            'x1': frame_x1, 'y1': 90.0, 
            'x2': frame_x2, 'y2': 90.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Matriz de confusão
        {
            'name': 'text_6', 'type': 'T', 
            'x1': left_text_x1, 'y1': 93.5, 
            'x2': frame_x2, 'y2': 95.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Matriz de confusão', 'priority': 0, 
        },
        { 
            'name': 'confusion_matrix', 'type': 'I', 
            'x1': frame_x1 + 5, 'y1': 102.5, 
            'x2': vertical_divider_x - 5, 'y2': 165.0, 
            'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'R', 'text': ft_confusion_matrix_path, 'priority': 2, 
        },

        # Top 4 losses
        {
            'name': 'text_7', 'type': 'T', 
            'x1': right_text_x1, 'y1': 93.5, 
            'x2': frame_x2, 'y2': 95.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Top 4 losses', 'priority': 0, 
        },
        {
            'name': 'top_losses', 'type': 'I', 
            'x1': vertical_divider_x + 15, 'y1': 97.5, 
            'x2': frame_x2 - 15, 'y2': 170.0, 
            'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'R', 'text': ft_top_losses_path, 'priority': 2, 
        },
        { 
            'name': 'line_6', 'type': 'L', 
            'x1': frame_x1, 'y1': 172.0, 
            'x2': frame_x2, 'y2': 172.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },  

        # Predição
        { 
            'name': 'text_8', 'type': 'T', 
            'x1': left_text_x1, 'y1': 174.5, 
            'x2': right_text_x1, 'y2': 179.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': highlight_color, 'background': 0, 
            'align': 'L', 'text': 'Predição', 'priority': 0,
        },
        { 
            'name': 'line_7', 'type': 'L', 
            'x1': frame_x1, 'y1': 182.0, 
            'x2': frame_x2, 'y2': 182.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },
        { 
            'name': 'vertical_divider_3', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 182.0, 
            'x2': vertical_divider_x, 'y2': 192.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Quantidade de testes realizados
        {
            'name': 'text_9', 'type': 'T', 
            'x1': left_text_x1, 'y1': 187.0, 
            'x2': frame_x2, 'y2': 187.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Quantidade de testes realizados', 'priority': 0, 
        },
        { 
            'name': 'performance_tuning', 'type': 'T', 
            'x1': right_text_x1, 'y1': 183.0, 
            'x2': frame_x2, 'y2': 190.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 
        },
        { 
            'name': 'line_8', 'type': 'L', 
            'x1': frame_x1, 'y1': 192.5, 
            'x2': frame_x2, 'y2': 192.5, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Limitações e considerações éticas
        { 
            'name': 'text_10', 'type': 'T', 
            'x1': left_text_x1, 'y1': 194.5, 
            'x2': right_text_x1, 'y2': 199.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': highlight_color, 'background': 0, 
            'align': 'L', 'text': 'Limitações e considerações éticas', 'priority': 0,
        },
        { 
            'name': 'line_9', 'type': 'L', 
            'x1': frame_x1, 'y1': 201.0, 
            'x2': frame_x2, 'y2': 201.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },
        { 
            'name': 'vertical_divider_3', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 201.0, 
            'x2': vertical_divider_x, 'y2': 247.5, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Limitações
        {
            'name': 'text_11', 'type': 'T', 
            'x1': left_text_x1, 'y1': 203.5, 
            'x2': frame_x2, 'y2': 208.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Limitações', 'priority': 0, 
        },
        { 
            'name': 'ethics_limitations', 'type': 'T', 
            'x1': right_text_x1, 'y1': 203.5, 
            'x2': frame_x2, 'y2': 209.00, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True,
        },
        { 
            'name': 'line_10', 'type': 'L', 
            'x1': frame_x1, 'y1': 229.0, 
            'x2': frame_x2, 'y2': 229.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        }, 

        # Considerações éticas
        {
            'name': 'text_12', 'type': 'T', 
            'x1': left_text_x1, 'y1': 231.5, 
            'x2': frame_x2, 'y2': 237.0, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Considerações éticas', 'priority': 0, 
        },
        { 
            'name': 'ethics_considerations', 'type': 'T', 
            'x1': right_text_x1, 'y1': 231.5, 
            'x2': frame_x2, 'y2': 237.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True,
        },
        { 
            'name': 'line_11', 'type': 'L', 
            'x1': frame_x1, 'y1': 247.5, 
            'x2': frame_x2, 'y2': 247.5, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        }, 

        # Referências
        { 
            'name': 'text_13', 'type': 'T', 
            'x1': left_text_x1, 'y1': 249.5, 
            'x2': right_text_x1, 'y2': 254.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': highlight_color, 'background': 0, 
            'align': 'L', 'text': 'Referências', 'priority': 0,
        },
        { 
            'name': 'line_12', 'type': 'L', 
            'x1': frame_x1, 'y1': 256.0, 
            'x2': frame_x2, 'y2': 256.0, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },
        { 
            'name': 'vertical_divider_4', 'type': 'L', 
            'x1': vertical_divider_x, 'y1': 256.0, 
            'x2': vertical_divider_x, 'y2': 282.5, 
            'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'I', 'text': None, 'priority': 3, 
        },

        # Autores e afiliação
        {
            'name': 'text_14', 'type': 'T', 
            'x1': left_text_x1, 'y1': 258.5, 
            'x2': frame_x2, 'y2': 263.5, 
            'font': 'Arial', 'size': text_size, 'bold': 1, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': 'Autores e afiliação', 'priority': 0, 
        },
        { 
            'name': 'author', 'type': 'T', 
            'x1': right_text_x1, 'y1': 258.5, 
            'x2': frame_x2, 'y2': 263.5, 
            'font': 'Arial', 'size': text_size, 'bold': 0, 'italic': 0, 'underline': 0, 
            'foreground': 0, 'background': 0, 
            'align': 'L', 'text': '', 'priority': 0, 'multiline': True,
        },
    ]