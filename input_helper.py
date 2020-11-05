
class InputHelper():

    def __init__(self, help='', options=[], default=None):
        if isinstance(default, str):
            if default in options:
                default = options.index(default)
            else:
                try:
                    default = int(default)
                    if not default < len(options):
                        default = 0
                except:
                    default = 0

        elif isinstance(default, int):
            if not default < len(options):
                default = 0
        else:
            default = 0

        self.help = help
        self.options = options
        self.default = default

    def get_output(self):
        while True:
            print(self.help)
            for index, option in enumerate(self.options):
                print('[%d]: %s' % (index, option.capitalize()))
            
            if not self.default == None:
                selection = raw_input('Select option [%d]: ' % (self.default))
            else:
                selection = raw_input('Select option: ')
            
            if selection == '':
                selection = self.default

            try:
                selection = int(selection)

                if selection < len(self.options):
                    return self.options[selection]
                else:
                    print('\n[Error]: Selection has to be between %s.\n' % ('0-' + str(len(self.options) - 1)))
            except ValueError:
                print('\n[Error]: Enter selection as a number\n')


