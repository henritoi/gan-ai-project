import sys

class Progress:

    def __init__(self, total, bar_len=60):
        self.total = total
        self.bar_len = bar_len

    def update(self, count, status=''):
        filled_len = int(round(self.bar_len * count / float(self.total)))

        percent = round(100.0 * count / float(self.total) - 1)
        bar = '=' * filled_len + '-' * (self.bar_len - filled_len)

        sys.stdout.write('[%s] %s%s [%s/%s] ...%s\r' % (bar, percent, '%', count, self.total, status))
        sys.stdout.flush()
    
    def stop(self):
        print()
