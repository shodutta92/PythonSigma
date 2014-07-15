import pprint
import json


class ModelInfo:
    def __init__(self):
        self.name = None
        self.description = None
        self.outputFile = None
        self.traceVars = None
        self.randomSeed = None
        self.initialValues = None
        self.endingCondition = None
        self.endingTime = None

        self.firstEvent = None

        self.stateVariables = []
        self.vertexes = {}
        self.edges = {}

        self.compiled = {}


class StateVariable:
    def __init__(self):
        self.name = None
        self.description = None
        self.type = None
        self.size = None

    def __repr__(self):
        return pprint.pformat(self.__dict__)


class Vertex:
    def __init__(self):
        self.name = None
        self.description = None
        self.stateChanges = None
        self.parameters = None

    def __repr__(self):
        return pprint.pformat(self.__dict__)


class Edge:
    def __init__(self):
        self.description = None
        self.type = None
        self.origin = None
        self.destination = None
        self.condition = None
        self.delay = None
        self.priority = None
        self.attributes = None

    def __repr__(self):
        return str(self.__dict__)


class Event:
    def __init__(self, time, priority, attributes, vertex, count):
        self.time = time
        self.priority = priority
        self.attributes = attributes
        self.vertex = vertex
        self.count = count

    def __lt__(self, other):
        if self.time < other.time:
            return True
        elif self.time == other.time:
            if self.priority < other.priority:
                return True
            elif self.priority == other.priority:
                if self.count > other.count:
                    return True
        else:
            return False


class Output:
    def __init__(self):
        self.statistics = None
        self.events = None
        self.inputs = None
        self.traceHeaders = None
        self.optimized = False

    def to_json(self):
        data = dict()
        data['statistics'] = self.statistics
        data['events'] = self.events
        data['inputs'] = self.inputs
        data['traceHeaders'] = self.traceHeaders
        data['optimized'] = self.optimized
        return json.dumps(data)

    def set_events(self, events):
        self.events = events

    def set_statistics(self, statistics):
        self.statistics = statistics

    def set_inputs(self, inputs):
        self.inputs = inputs

    def set_trace_headers(self, headers):
        self.traceHeaders = headers

    def set_optimized(self, optimized):
        self.optimized = optimized