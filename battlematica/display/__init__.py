import warnings

try:
    import arcade
except ModuleNotFoundError:
    warnings.warn('Optional requirement "arcade" not found. '
                  'You will not be able to use the built-in graphics.')
else:
    from .game_display_process import GameDisplayProcess
    from .asset_container import AssetContainer
