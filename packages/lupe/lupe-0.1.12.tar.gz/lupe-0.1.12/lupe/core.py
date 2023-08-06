class Lupe():
    def __init__(self, help_message, options={}):
        self.version = ''

        self.flags = {}
        self.inputs = []
        self.aliases = {}

        self.help = help_message

        self._set_options(options)

    def _set_options(self, options):
        for key, value in options.items():
            if key == 'version':
                self.version = value
            elif key == 'help':
                self.help = value
            elif key == 'flags':
                self.flags = self._set_flags(value)
            elif key == 'inputs':
                self.inputs = self._set_inputs(value)

    def _set_flags(self, flags):
        return flags

    def _set_inputs(self, inputs):
        return inputs

    def show_help(self):
        print(self.help)
        exit(2)

    def show_version(self):
        print(self.version)
        exit()
