import uuid



class TemporalExpression:
    def __init__(self, time_type, value, original_sentence, annotated_time):
        self.id = uuid.uuid4()
        self.time_type = time_type
        self.value = value
        self.original_sentence = original_sentence.lower()
        self.annotated_time = annotated_time.lower()
        self._freq = None
        self._quant = None
        self._process_description_name = None
        self._process_description_version = None

    def __repr__(self):
        to_print = "Sentence: " + self.original_sentence + "\n" \
                   + "Annotated Time: " + self.annotated_time + "\n" \
                   + "Value: " + self.value
        if self.process_description_name:
            to_print = "\n" + "Process Description: " + self.process_description_name + "\n" + to_print
        if self.process_description_version:
            to_print = "Process Description Version: " + self.process_description_version + "\n" + to_print
        if self.freq:
            to_print = "\n" + to_print + "Frequency: " + self.freq
        if self.quant:
            to_print = to_print + "\n" + "Quantity: " + self.quant
        if self.time_type:
            to_print = to_print + "\n" + "Time Type: " + str(self.time_type)

        return to_print

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, freq):
        self._freq = freq

    @property
    def quant(self):
        return self._quant

    @quant.setter
    def quant(self, new_quant):
        self._quant = new_quant

    @property
    def process_description_name(self):
        return self._process_description_name

    @process_description_name.setter
    def process_description_name(self, process_description_name):
        self._process_description_name = process_description_name

    @property
    def process_description_version(self):
        return self._process_description_version

    @process_description_version.setter
    def process_description_version(self, process_description_version):
        self._process_description_version = process_description_version


def make_temporal_expression(time_type, value, original_sentence, original_temporal_expression):
    temporal_expression = TemporalExpression(time_type, value, original_sentence, original_temporal_expression)
    return temporal_expression
