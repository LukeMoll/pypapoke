from abc import ABCMeta, abstractmethod

from typing import List, NewType, Union, Tuple

SinkIndex = NewType('SinkIndex', int)
SinkInputIndex = NewType('SinkInputIndex', int)
SinkName = NewType('SinkName', str)

class AbstractBackend(metaclass=ABCMeta):

    @abstractmethod
    def get_sinks(self) -> List[Tuple[SinkIndex,SinkName]]:
        pass

    @abstractmethod
    def get_sink_inputs(self) -> List[Tuple[SinkInputIndex, SinkIndex]]:
        pass

    @abstractmethod
    def move_sink_inputs_to(self, sink : Union[SinkIndex,SinkName]):
        pass

    @abstractmethod
    def set_default_sink(self, sink : Union[SinkIndex,SinkName]):
        pass