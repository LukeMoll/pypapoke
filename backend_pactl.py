from .backend import *

import subprocess
from operator import itemgetter

def pactl(*args : str) -> subprocess.CompletedProcess:
    return subprocess.run(["/usr/bin/pactl", *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True, text=True)

class PACtlBackend(AbstractBackend):

        def get_sinks(self) -> List[Tuple[SinkIndex,SinkName]]:
            proc = pactl("list", "short", "sinks")
            sinks = []
            for line in proc.stdout.strip().split("\n"):
                parts = line.split()
                index = SinkIndex(parts[0])
                name = SinkName(parts[1])
                sinks.append((index,name))
            return sinks

        def get_sink_inputs(self) -> List[Tuple[SinkInputIndex, SinkIndex]]:
            proc = pactl("list", "short", "sink-inputs")
            inputs = []
            for line in proc.stdout.strip().split("\n"):
                if len(line) < 3:
                    continue
                parts = line.split()
                sink_input = SinkInputIndex(parts[0])
                sink = SinkIndex(parts[1])
                inputs.append((sink_input,sink))
            return inputs

        def move_sink_input(self, sinkinput : SinkInputIndex, sink : Union[SinkIndex,SinkName]):
            pactl("move-sink-input", str(sinkinput), str(sink))

        def move_sink_inputs_to(self, sink : Union[SinkIndex,SinkName]):
            for sinkinput in map(itemgetter(0), self.get_sink_inputs()):
                self.move_sink_input(sinkinput, sink)

        def set_default_sink(self, sink : Union[SinkIndex,SinkName]):
            pactl("set-default-sink", str(sink))