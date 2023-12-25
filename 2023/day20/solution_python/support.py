import enum
from collections import deque

class NotImplemented(Exception):
    pass

class NotUnderstood(Exception):
    pass

class Pulse(enum.Enum):
    LOW = 0
    HIGH = 1
    NONE = 2

class Status(enum.Enum):
    OFF = 0
    ON = 1

class CircuitManager:
    def __init__(self):
        self.modules = {}
        self.hookups = []
        self.message_queue = deque()
        self.low_count = 0
        self.high_count = 0

    def parse_input_line(self, line):
        line = line.strip()
        module_name, destinations = line.split(' -> ')
        module = self.create_module(module_name)

        for destination in destinations.split(','):
            destination = destination.strip()
            module.add_destination_module(destination)
            self.hookups.append((destination, module.name))

        self.modules[module.name] = module

    def create_backlinks(self):
        for dest, source in self.hookups:
            if dest not in self.modules:
                print(dest)
                module = Module(dest)
                self.modules[module.name] = module
            self.modules[dest].add_input_module(source)

    def initialise_queue(self):
        if not 'button' in self.modules:
            self.modules['button'] = Button()
        for message in self.modules['button'].emit():
            self.message_queue.append(message)

    def run(self):
        while self.message_queue:
            message = self.message_queue.popleft()
            # if message.pulse != Pulse.NONE: print(message)
            if message.pulse == Pulse.LOW:
                self.low_count += 1
            if message.pulse == Pulse.HIGH:
                self.high_count += 1
            source = message.from_
            dest = message.to_
            pulse = message.pulse
            if pulse != pulse.NONE:
                self.modules[dest].receive(source, pulse)
                for emitted in self.modules[dest].emit():
                    self.message_queue.append(emitted)

    def push_button(self):
        self.initialise_queue()
        self.run()

    def read_file(self, filename):
        with open(filename) as fl:
            for line in fl:
                self.parse_input_line(line)
        self.create_backlinks()

    def create_module(self, name):
        if name == 'button':
            return Button()
        if name == 'broadcaster':
            return Broadcast()
        if name.startswith('%'):
            return FlipFlop(name[1:])
        if name.startswith('&'):
            return Conjunction(name[1:])
        raise NotUnderstood(f"Didn't understand how to create this module - {name}")

class Module:
    def __init__(self, name):
        self.name = name
        self.inputs = {}
        self.destinations = []
        self.pulse = Pulse.LOW

    def add_input_module(self, module: str):
        self.inputs[module] = Pulse.NONE

    def add_destination_module(self, module):
        self.destinations.append(module)

    def receive(self, from_: str, pulse: Pulse):
        self.inputs[from_] = pulse

    def emit(self):
        return [Message(self.name, destination, self.pulse)
                for destination in self.destinations]

class Rx(Module):
    pass

class Button(Module):
    def __init__(self):
        super().__init__("button")
        self.destinations = ['broadcaster']
        self.pulse = Pulse.LOW

    def add_input_module(self, module: str):
        raise NotImplemented("Buttons don't allow new input modules")

    def add_destination_module(self, module):
        raise NotImplemented("Buttons don't allow new destinations")

    def receive(self):
        raise NotImplemented("Buttons don't receive pulses")

class Conjunction(Module):
    """
    Conjunction:
    Remembers the last pulse sent by each input module.
    Defaults to a memory of a LOW pulse.
    If it remembers a HIGH pulse for all inputs, emits a LOW pulse
    Otherwise emits a HIGH pulse
    """
    def add_input_module(self, module: str):
        self.inputs[module] = Pulse.LOW
    
    def receive(self, from_: str, pulse: Pulse):
        self.inputs[from_] = pulse
        if all(val == Pulse.HIGH for val in self.inputs.values()):
            self.pulse = Pulse.LOW
        else:
            self.pulse = Pulse.HIGH

class Broadcast(Module):
    def __init__(self):
        super().__init__("broadcaster")
        self.inputs["button"] = Pulse.LOW

    def add_input_module(self, module: str):
        raise NotImplemented("Broadcasters don't allow new input modules")

    def receive(self, from_: str, pulse: Pulse):
        self.pulse = pulse

class FlipFlop(Module):
    """
    FlipFlops:
    Are initially set to OFF
    Ignore HIGH pulses
    On receiving a LOW pulse, either:
    flips from OFF to ON and sends a HIGH pulse
    flips from ON to OFF and sends a LOW pulse
    """
    prefix = '%'
    def __init__(self, name):
        super().__init__(name)
        self.status = Status.OFF

    def receive(self, from_: str, pulse: Pulse):
        if pulse == Pulse.LOW:
            if self.status == Status.OFF:
                self.status = Status.ON
                self.pulse = Pulse.HIGH
            else:
                self.status = Status.OFF
                self.pulse = Pulse.LOW
        else:
            self.pulse = Pulse.NONE

class Message:
    def __init__(self, from_: str, to_: str, pulse: Pulse):
        self.from_ = from_
        self.to_ = to_
        self.pulse = pulse

    def __repr__(self):
        return f"Message({self.from_} -> {self.to_} [{self.pulse}])"