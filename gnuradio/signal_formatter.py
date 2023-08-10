import numpy as np
from gnuradio import gr


class blk(gr.basic_block):
    def __init__(self, signal_length=0, preamble=None, postamble=None, delay_length=0):
        gr.basic_block.__init__(self, name="Signal Formatter", in_sig=[np.byte], out_sig=[np.byte])

        self.idx = 0
        self.signal_length = signal_length
        self.preamble = preamble or []
        self.postamble = postamble or []
        self.delay_length = delay_length

    def general_work(self, input_items, output_items):
        number_of_inputs_processed = 0
        for i in range(len(output_items[0])):
            if self.idx < len(self.preamble):
                output_items[0][i] = self.preamble[self.idx]
            elif self.idx < len(self.preamble) + self.signal_length:
                output_items[0][i] = input_items[0][number_of_inputs_processed]
                number_of_inputs_processed += 1
            elif self.idx < len(self.preamble) + self.signal_length + len(self.postamble):
                output_items[0][i] = self.postamble[self.idx - len(self.preamble) - self.signal_length]
            else:
                output_items[0][i] = 0

            self.idx += 1
            if self.idx == len(self.preamble) + self.signal_length + len(self.postamble) + self.delay_length:
                self.idx = 0

        self.consume(0, number_of_inputs_processed)
        return len(output_items[0])
