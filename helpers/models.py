# -*- coding: utf-8 -*-


def representation_helper(cls):
    """
    Class decorator to return obj.__repr__() as Obj.objects.get(pk=X) - obj.str()
    in order to facilitate debug
    """

    def __my_repr__(self):
        try:
            return "{}.objects.get(pk={}) - {}".format(
                self.__class__.__name__, self.pk, self.__str__()
            )
        except Exception:
            return self.__str__()

    cls.__repr__ = lambda obj: __my_repr__(obj)
    return cls
