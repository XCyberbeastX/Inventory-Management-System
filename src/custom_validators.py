from wtforms import IntegerField
from wtforms.validators import ValidationError

class OptionalInteger(IntegerField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0])
            except ValueError:
                if valuelist[0] == "":
                    self.data = None
                else:
                    raise ValidationError('Not a valid integer value')