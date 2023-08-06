class EngineLazy:
    def __init__(self, factory_callback: callable):
        self._factory_callback = factory_callback
        self._engine = None

    def __getattr__(self, attribute_name):
        if self._engine is None:
            self._engine = self._factory_callback()

        return getattr(self._engine, attribute_name)
