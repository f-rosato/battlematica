import arcade as ad


class SpriteM90(ad.Sprite):
    def _set_angle(self, new_value: float):
        super()._set_angle(new_value - 90.0)

    def _get_angle(self) -> float:
        return super(SpriteM90, self)._get_angle()

    angle = property(_get_angle, _set_angle)