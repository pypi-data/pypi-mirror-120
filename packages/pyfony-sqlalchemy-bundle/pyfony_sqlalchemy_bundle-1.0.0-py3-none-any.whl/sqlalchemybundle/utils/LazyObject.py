from werkzeug.utils import cached_property


class LazyObject:
    def __init__(self, factory_callback: callable):
        self._factory_callback = factory_callback

    @cached_property
    def get(self):
        return self._factory_callback()
