import arcade as ad


class SpriteM90(ad.Sprite):

    @ad.Sprite.angle.setter
    def angle(self, new_value: float):
        """Set the angle of the sprite's rotation."""
        new_value = new_value - 90.0
        ad.Sprite.angle.fset(self, new_value)
