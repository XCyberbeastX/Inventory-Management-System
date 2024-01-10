from werkzeug.utils import secure_filename
import os
import random

class FileHandler:
    @staticmethod
    def allowed_file(filename, allowed_extensions):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def save_file(file, folder, allowed_extensions):
        if file and FileHandler.allowed_file(file.filename, allowed_extensions):
            random_number = random.randint(10000000, 99999999)
            filename = secure_filename(str(random_number) + file.filename)
            file.save(os.path.join(folder, filename))
            return os.path.join(folder, filename)
        return None