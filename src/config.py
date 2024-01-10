import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')

    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_PDF_EXTENSIONS = {'pdf'}
    
    IMAGE_FOLDER = 'static/images'
    PDF_FOLDER = 'static/pdfs'
    BARCODE_FOLDER = 'static/barcodes'

    SERIAL_PORT = os.getenv('SERIAL_PORT', '/dev/ttyACM0')
    SERIAL_BAUDRATE = os.getenv('SERIAL_BAUDRATE', 9600)
    SERIAL_TIMEOUT = os.getenv('SERIAL_TIMEOUT', 1)

    LED_COUNT = os.getenv('LED_COUNT', 68)
    LED_PIN = os.getenv('LED_PIN', 18)
    LED_FREQ_HZ = os.getenv('LED_FREQ_HZ', 800000)
    LED_DMA = os.getenv('LED_DMA', 10)
    LED_BRIGHTNESS = os.getenv('LED_BRIGHTNESS', 255)
    LED_INVERT = os.getenv('LED_INVERT', False)
    LED_CHANNEL = os.getenv('LED_CHANNEL', 0)