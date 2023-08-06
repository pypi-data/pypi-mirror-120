from os.path import join, expanduser, dirname
from ovos_plugin_manager.templates.hotwords import HotWordEngine
from precise_lite_runner import PreciseLiteListener, ReadWriteStream
from chatterbox_utils.log import LOG
from chatterbox_bus_client import Message


class DoubleTapsHotwordPlugin(HotWordEngine):
    def __init__(self, key_phrase="tap tap", config=None, lang="en-us"):
        super().__init__(key_phrase, config, lang)
        self.expected_duration = self.config.get("expected_duration") or 3
        self.has_found = False
        self.conf = 0.0

        self.stream = ReadWriteStream()
        self.chunk_size = 2048
        self.trigger_level = self.config.get('trigger_level', 2)
        self.sensitivity = self.config.get('sensitivity', 0.5)

        self.precise_model = join(dirname(__file__), "res", "double_tap.tflite")

        self.runner = PreciseLiteListener(model=self.precise_model,
                                          stream=self.stream,
                                          chunk_size=self.chunk_size,
                                          trigger_level=self.trigger_level,
                                          sensitivity=self.sensitivity,
                                          on_prediction=self.on_prediction,
                                          on_activation=self.on_activation,
                                          )
        self.runner.start()

    # bus events
    @property
    def bus(self):
        return self._bus

    def bind(self, bus):
        # TODO standardize usage of bind in ovos plugin manager
        self._bus = bus

    def on_prediction(self, conf):
        self.conf = float(conf)

    def on_activation(self):
        if not self.has_found:
            # LOG.debug(f"tap tap: {self.conf}")
            self.bus.emit(Message("chatterbox.double_tap",
                                  {"conf": self.conf}))
        self.has_found = True

    def update(self, chunk):
        self.stream.write(chunk)

    def found_wake_word(self, frame_data):
        if self.has_found:
            self.has_found = False
            return False
        return False

    def stop(self):
        if self.runner:
            self.runner.stop()
