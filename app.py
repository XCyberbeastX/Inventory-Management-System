from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from src.models import db, Component
from src.forms import AddComponentForm
from src.file_handler import FileHandler
from src.barcode_scanner import BarcodeScanner
from src.led_controller import LEDController
from src.barcode_generator import BarcodeGenerator
from src.config import Config
from signal import signal, SIGINT
import atexit
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
led_controller = LEDController(Config.LED_COUNT, Config.LED_PIN, Config.LED_FREQ_HZ, Config.LED_DMA, Config.LED_BRIGHTNESS, Config.LED_INVERT, Config.LED_CHANNEL)
barcode_scanner = BarcodeScanner(Config.SERIAL_PORT, Config.SERIAL_BAUDRATE, Config.SERIAL_TIMEOUT)
barcode_generator = BarcodeGenerator('code128')

def handle_shutdown(*args):
    print("Shutdown: Closing serial port and clearing all LEDs")
    barcode_scanner.close_serial()
    led_controller.clear_all_pixels()
    db.session.remove()
    db.engine.dispose()
    exit(0)

atexit.register(handle_shutdown)
signal(SIGINT, handle_shutdown)

@app.route('/')
def home():
    all_components = Component.query.all()
    return render_template('/index.html', components=all_components)

@app.route('/add_component', methods=['GET', 'POST'])
def add_component():
    form = AddComponentForm()
    if form.validate_on_submit():
        new_component = Component(
            name=form.name.data,
            quantity=form.quantity.data,
            category=form.category.data,
            description=form.description.data,
            io_number=form.io_number.data
        )

        datasheet_path = FileHandler.save_file(form.datasheet.data, Config.PDF_FOLDER, Config.ALLOWED_PDF_EXTENSIONS) or Config.PDF_FOLDER + '/placeholder.pdf'
        image_path = FileHandler.save_file(form.image.data, Config.IMAGE_FOLDER, Config.ALLOWED_IMAGE_EXTENSIONS) or Config.IMAGE_FOLDER + '/placeholder.jpg'
        
        new_component.datasheet = datasheet_path
        new_component.image = image_path

        db.session.add(new_component)
        db.session.commit()

        new_component.barcode = barcode_generator.generate_barcode(new_component.id)
        
        db.session.commit()

        flash('Component added successfully', 'success')
        return redirect(url_for('home'))

    return render_template('add_component.html', form=form)

@app.route('/detail')
def detail():
    id = request.args.get('id')
    component = Component.query.get_or_404(id)
    return render_template('detail.html', component=component)


@app.route('/get_barcode')
def get_barcode():
    barcode = barcode_scanner.read_barcode()
    if barcode is not None:
        return jsonify(barcode=barcode)
    else:
        return jsonify(error="serial port is not available!\n"), 500

@app.route('/update_component/<int:id>', methods=['POST'])
def update_component(id):
    component = Component.query.get_or_404(id)

    if component.io_number is not None:
        old_io_number = component.io_number
    else:
        old_io_number = None

    if request.method == 'POST':
        component.name = request.form['name']
        component.quantity = request.form['quantity']
        component.category = request.form['category']
        component.description = request.form['description']
        component.io_number = request.form['io_number'] or None
        
        if component.io_number == "":
            component.io_number = None
        
        if LEDController.isRaspberryPi:
            if old_io_number is not None:
                led_controller.set_pixel(old_io_number, led_controller.LED_OFF_COLOR)
            if component.io_number is not None:
                if(component.io_state):
                    led_controller.set_pixel(component.io_number, led_controller.LED_ON_COLOR)
                else:
                    led_controller.set_pixel(component.io_number, led_controller.LED_OFF_COLOR)
           
        datasheet_file = request.files['datasheet']
        image_file = request.files['image']

        if datasheet_file and component.datasheet is not None:
            if component.datasheet != Config.PDF_FOLDER + '/placeholder.pdf':
                os.remove(component.datasheet)
        
        if image_file and component.image is not None:
            if component.image != Config.IMAGE_FOLDER + '/placeholder.jpg':
                os.remove(component.image)

        if datasheet_file and FileHandler.allowed_file(datasheet_file.filename, Config.ALLOWED_PDF_EXTENSIONS):
            datasheet_path = FileHandler.save_file(datasheet_file, Config.PDF_FOLDER, Config.ALLOWED_PDF_EXTENSIONS)
            component.datasheet = datasheet_path

        if image_file and FileHandler.allowed_file(image_file.filename, Config.ALLOWED_IMAGE_EXTENSIONS):
            image_path = FileHandler.save_file(image_file, Config.IMAGE_FOLDER, Config.ALLOWED_IMAGE_EXTENSIONS)
            component.image = image_path

        db.session.commit()
        
        flash('Component updated successfully', 'success')
        return redirect(url_for('detail', id=component.id))

    return render_template('detail.html', component=component)

@app.route('/delete_component/<int:id>', methods=['POST'])
def delete_component(id):
    component = Component.query.get_or_404(id)

    if component.datasheet is not None:
        if component.datasheet != Config.PDF_FOLDER + '/placeholder.pdf':
            os.remove(component.datasheet)
    
    if component.image is not None:
        if component.image != Config.IMAGE_FOLDER + '/placeholder.jpg':
            os.remove(component.image)
    
    if component.barcode is not None:
        # alternative: os.remove(component.barcode)
        barcode_generator.delete_barcode(component.barcode)
    
    if LEDController.isRaspberryPi:
        if component.io_number is not None:
            led_controller.set_pixel(component.io_number, led_controller.LED_OFF_COLOR)
    
    db.session.delete(component)
    db.session.commit()
    
    flash('Component deleted successfully', 'success')
    return redirect(url_for('home'))

@app.route('/update_io_state', methods=['POST'])
def update_io_state():
    data = request.json
    component_id = data['id']
    component = Component.query.get_or_404(component_id)
    component.io_state = not component.io_state
    db.session.commit()

    if LEDController.isRaspberryPi:
        if component.io_number is not None:
            if component.io_state:
                led_controller.set_pixel(component.io_number, led_controller.LED_ON_COLOR)
            else:
                led_controller.set_pixel(component.io_number, led_controller.LED_OFF_COLOR)
    else:
        print("LEDController: Not running on a Raspberry Pi. IO state cant be displayed!")

    return jsonify({'status': 'success'}), 200

@app.route('/options')
def options():
    return render_template('options.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80, debug=True)