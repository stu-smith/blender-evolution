class AABB(object):
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._z1 = z1
        self._z2 = z2

    @property
    def x1(self):
        return self._x1

    @property
    def x2(self):
        return self._x2

    @property
    def y1(self):
        return self._y1

    @property
    def y2(self):
        return self._y2

    @property
    def z1(self):
        return self._z1

    @property
    def z2(self):
        return self._z2

    @property
    def mid_x(self):
        return self._x1 + (self._x2 - self._x1) / 2

    @property
    def mid_y(self):
        return self._y1 + (self._y2 - self._y1) / 2

    @property
    def mid_z(self):
        return self._z1 + (self._z2 - self._z1) / 2

    @staticmethod
    def union(aabb1, aabb2):
        if not aabb1 and not aabb2:
            return None
        if not aabb1:
            return aabb2
        if not aabb2:
            return aabb1

        return AABB(
            min(aabb1.x1, aabb2.x1),
            max(aabb1.x2, aabb2.x2),
            min(aabb1.y1, aabb2.y1),
            max(aabb1.y2, aabb2.y2),
            min(aabb1.z1, aabb2.z1),
            max(aabb1.z2, aabb2.z2)
        )
