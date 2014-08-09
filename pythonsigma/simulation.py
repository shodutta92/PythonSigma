from Queue import PriorityQueue
from itertools import count
from copy import copy
from time import time
import random

from parser import parse
from pythonsigma.model import Event
from pythonsigma.model import Output


class Simulation:
    def __init__(self, model_file, runtime, initial_values, input_data):
        globals()['clock'] = 0
        self.model = parse(model_file)
        self.model.initialValues = initial_values
        self.queue = PriorityQueue()
        self.counter = count()
        self.runtime = runtime
        self.output = Output()
        self.input_data = input_data

    def run_simulation(self, random_seed):
        self.initialize()
        random.seed(random_seed)
        while globals()['clock'] < self.runtime and self.queue.qsize() > 0:
            self.execute_event()
        return self.output

    def initialize(self):
        global datastore
        datastore = []
        globals()['data'] = {}
        for datafilename in self.input_data:
            globals()['data'][datafilename] = iter(self.input_data[datafilename])
        self.output.events = []
        self.output.statistics = dict()
        for var in self.model.traceVars:
            self.output.statistics[var] = dict()
            self.output.statistics[var]['maximum'] = float('-Inf')
            self.output.statistics[var]['minimum'] = float('Inf')
        self.output.traceHeaders = self.model.traceVars
        for var in self.model.stateVariables:
            if var.size == 1:
                globals()[var.name] = 0
            elif var.size > 1:
                globals()[var.name] = [0] * var.size
        event_name = self.model.firstEvent
        self.queue.put(Event(0, 1, self.model.initialValues,
                             event_name, next(self.counter)))

    def execute_event(self):
        event = self.queue.get()
        globals()['clock'] = event.time
        vertex = self.model.vertexes[event.vertex]
        for (index, parameter) in enumerate(vertex.parameters):
            if len(parameter) > 0:
                globals()['event'] = event
                globals()['index'] = index
                exec parameter + '= float(event.attributes[index])' in globals()

        for change in vertex.stateChanges:
            if len(change) > 0:
                exec self.model.compiled[change] in globals()

        edge_eval = []
        for edge in self.model.edges[event.vertex]:
            if eval(self.model.compiled[edge.condition]):
                edge_eval.append(edge)
        for edge in edge_eval:
            attribute_list = []
            for attribute in edge.attributes:
                if len(attribute) > 0:
                    attribute_list.append(eval(self.model.compiled[attribute]))
            self.queue.put(Event(globals()['clock'] + eval(self.model.compiled[edge.delay]),
                                 edge.priority, attribute_list, edge.destination,
                                 next(self.counter)))

        event = dict()
        event['Time'] = globals()['clock']
        for var in self.model.traceVars:
            val = eval(var)
            event[var] = val
            self.output.statistics[var]['maximum'] = max(self.output.statistics[var]['maximum'], val)
            self.output.statistics[var]['minimum'] = min(self.output.statistics[var]['maximum'], val)
        self.output.events.append(event)


def put(listindex):
    if listindex >= len(datastore):
        datastore.extend([None]*(listindex + 1 - len(datastore)))
        datastore[listindex] = []
    datastore[listindex].append(copy(globals()['ENT']))
    return 1


def get(listindex):
    globals()['ENT'] = datastore[listindex].pop(0)
    return 1
