import glob


class AssetContainer:

    def __init__(self, folder):

        """A wrapper class for a folder in which an asset archive was extracted.
        An instance of this class is passed to a GameDisplayProcess to customize it with the
        assets contained in the folder."""

        self.folder = folder

    def bot(self, team, kind):
        f = glob.glob(f'{self.folder}\\bots\\*{team}\\*{kind}.png')
        assert len(f) == 1
        return f[0]

    def blast(self, kind):
        f = glob.glob(f'{self.folder}\\blasts\\*{kind}.png')
        assert len(f) == 1
        return f[0]

    def artifact(self, team):
        if team is None:
            team = 0
        f = glob.glob(f'{self.folder}\\artifacts\\*{team}.png')
        assert len(f) == 1
        return f[0]

    def bullet(self, kind):
        f = glob.glob(f'{self.folder}\\bullets\\*{kind:02}.png')
        assert len(f) == 1
        return f[0]

    def drop_port(self, team):
        if team is None:
            team = 0
        f = glob.glob(f'{self.folder}\\drop_ports\\*{team}.png')
        assert len(f) == 1
        return f[0]

    def background(self):
        f = glob.glob(f'{self.folder}\\background\\*.png')
        assert len(f) == 1
        return f[0]

    def background_L(self):
        f = glob.glob(f'{self.folder}\\background\\*.txt')

        with open(f[0], 'r') as tf:
            ct = tf.read()

        return int(ct)