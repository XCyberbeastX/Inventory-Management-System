from barcode.writer import ImageWriter
from src.config import Config
import barcode
import os

class BarcodeGenerator:
    def __init__(self, barcode_type):
        self.barcode_type = barcode_type
    
    def generate_barcode(self, barcode_data):
        barcode_class = barcode.get_barcode_class(self.barcode_type)
        barcode_obj = barcode_class(str(barcode_data), writer=ImageWriter())
        barcode_filename = 'barcode_' + str(barcode_data)
        barcode_obj.save(os.path.join(Config.BARCODE_FOLDER + "/",barcode_filename))
        barcode_image = Config.BARCODE_FOLDER + "/" + barcode_filename + '.png'
        return barcode_image
    
    def delete_barcode(self, barcode_component):
        os.remove(barcode_component)