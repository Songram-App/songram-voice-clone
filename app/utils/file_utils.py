def save_audio_file(audio_data, file_path):
    with open(file_path, 'wb') as f:
        f.write(audio_data)

def load_audio_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def generate_file_name(prefix, extension):
    import uuid
    return f"{prefix}_{uuid.uuid4().hex}{extension}"