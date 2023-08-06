from box import Box
from sqlalchemybundle.engine.EngineFactoryResolver import EngineFactoryResolver
from sqlalchemybundle.engine.EngineLazy import EngineLazy


class EngineFactory:
    def __init__(self, engine_factory_resolver: EngineFactoryResolver):
        self.__engine_factory_resolver = engine_factory_resolver

    def create(self, db_config: Box) -> EngineLazy:
        return self.__engine_factory_resolver.resolve(db_config).create(db_config)
