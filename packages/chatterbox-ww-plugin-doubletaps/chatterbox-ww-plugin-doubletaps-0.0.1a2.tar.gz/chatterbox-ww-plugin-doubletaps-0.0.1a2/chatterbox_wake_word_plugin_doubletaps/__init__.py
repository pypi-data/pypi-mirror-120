from os.path import join, expanduser, dirname
from ovos_plugin_manager.templates.hotwords import HotWordEngine
from precise_lite_runner import PreciseLiteListener, ReadWriteStream


class DoubleTapsHotwordPlugin(HotWordEngine):
    def __init__(self, key_phrase="tap tap", config=None, lang="en-us"):
        super().__init__(key_phrase, config, lang)
        self.expected_duration = self.config.get("expected_duration") or 3
        self.has_found = False
        self.stream = ReadWriteStream()
        self.chunk_size = 2048
        self.trigger_level = self.config.get('trigger_level', 3)
        self.sensitivity = self.config.get('sensitivity', 0.5)

        model = join(dirname(__file__), "res", "double_tap.tflite")
        self.precise_model = expanduser(model)

        self.runner = PreciseLiteListener(model=self.precise_model,
                                          stream=self.stream,
                                          chunk_size=self.chunk_size,
                                          trigger_level=self.trigger_level,
                                          sensitivity=self.sensitivity,
                                          on_activation=self.on_activation,
                                          )
        self.runner.start()

    def on_activation(self):
        if not self.has_found:
            print("tap tap") # TODO emit bus event
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
