import platform
from src.batch_color import bcolors

class LEDController:

    @staticmethod
    def isRaspberryPi():
        return platform.platform() == "Linux" and (platform.machine().startswith("arm") or platform.machine() == "aarch64")  

    def __init__(self, led_count, led_pin, led_freq_hz, led_dma, led_brightness, led_invert, led_channel):
        if self.isRaspberryPi():
            from rpi_ws281x import Adafruit_NeoPixel, Color
            self.pixels = Adafruit_NeoPixel(led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel)
            self.pixels.begin()
            self.LED_ON_COLOR = Color(255,0,0)
            self.LED_OFF_COLOR = Color(0,0,0)
        else:
            self.pixels = None
            self.LED_ON_COLOR = None
            self.LED_OFF_COLOR = None
            self.print_info()

    def print_info(self):
        print(bcolors.WARNING + "-------------------------------------------------------------------------------------" + bcolors.ENDC)      
        print(bcolors.WARNING + "LEDController: Not running on a Raspberry Pi. LED controller will not be initialized!" + bcolors.ENDC)
        print(bcolors.WARNING + "-------------------------------------------------------------------------------------" + bcolors.ENDC)

    def get_pixel(self, pixel_id):
        if self.isRaspberryPi() and pixel_id is not None:
            return self.pixels.getPixelColor(pixel_id)
        else:
            return None
    
    def set_pixel(self, pixel_id, color):
        if self.isRaspberryPi() and pixel_id is not None:
            self.pixels.setPixelColor(pixel_id, color)
            self.pixels.show()

    def set_all_pixels(self, color):
        if self.isRaspberryPi():
            for i in range(self.pixels.numPixels()):
                self.pixels.setPixelColor(i, color)
            self.pixels.show()

    def clear_all_pixels(self):
        if self.isRaspberryPi():
            self.set_all_pixels(Color(0, 0, 0))

    def change_brightness(self, brightness):
        if self.isRaspberryPi():
            self.pixels.setBrightness(brightness)
            self.pixels.show()

    def get_brightness(self):
        if self.isRaspberryPi():
            return self.pixels.getBrightness()
        else:
            return None