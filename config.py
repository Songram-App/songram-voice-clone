import os

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CHECKPOINTS_DIR = os.path.join(BASE_DIR, 'checkpoints')
    AUDIO_OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
    
    # Model configuration
    MODEL_NAME = 'openvoice_model'
    MODEL_CHECKPOINT = os.path.join(CHECKPOINTS_DIR, f'{MODEL_NAME}.pth')
    
    # Flask configuration
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000

    # Other configurations can be added here as needed
