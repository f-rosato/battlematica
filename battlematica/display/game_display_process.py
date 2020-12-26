import multiprocessing as mp
import os
import tempfile
import zipfile

import arcade as ad

from .asset_container import AssetContainer
from .gc_window import GCWindow

thisdir = os.path.dirname(os.path.realpath(__file__))
DEFAULT_ASSET_ZIP = os.path.join(thisdir, '..', '..', 'default_assets.zip')
DEFAULT_ASSET_FOLDER = tempfile.TemporaryDirectory()


class GameDisplayProcess(mp.Process):
    def __init__(self, engine, speed=1.0, asset_archive=None):

        """A Process that runs the game displayer.

        :param engine: the GameEngine instance to display
        :param speed: a multiplier representing the display speed. Normally the target speed is 60 ticks/s.
        :param asset_archive: optional path to an alternative asset archive

        """

        super().__init__()
        self.X = int(engine.X)
        self.Y = int(engine.Y)
        self.state_queue = engine.give_state_queue()
        self.speed_mult = speed

        if asset_archive is None:
            asset_archive = DEFAULT_ASSET_ZIP

        a = zipfile.ZipFile(asset_archive)
        a.extractall(DEFAULT_ASSET_FOLDER.name)
        self.asset_container = AssetContainer(DEFAULT_ASSET_FOLDER.name)

    def run(self) -> None:
        gamedisplayer = GCWindow(self.X, self.Y, self.state_queue,
                                 update_rate=1/60/self.speed_mult, asset_container=self.asset_container)
        gamedisplayer.setup()
        ad.run()
