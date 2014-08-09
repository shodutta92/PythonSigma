from pythonsigma.model import ModelInfo, StateVariable, Vertex, Edge
import re


def parse(input_file):
    model = ModelInfo()
    input_file = open(input_file, 'r')
    status = 0  # 0 = info, 1 = variables, 2 = vertexes, 3 = edges
    for line in input_file:
        if status == 0:
            if line.startswith('Model Name:'):
                model.name = line.split('Model Name:')[1].strip()
            elif line.startswith('Model Description:'):
                model.description = line.split('Model Description:')[1].strip()
            elif line.startswith('Trace Vars:'):
                model.traceVars = line.split('Trace Vars:')[1].strip().split(',')
                # Finish other model info
            elif line.startswith('Initial Values:'):
                model.initialValues = line.split('Initial Values:')[1].strip().split(',')
            elif 'STATE VARIABLES' in line:
                status = 1
        if status == 1:
            if 'State Variable #' in line:
                temp = StateVariable()
            elif line.startswith('Name:'):
                temp.name = line.split('Name:')[1].strip()
            elif line.startswith('Description:'):
                temp.description = line.split('Description:')[1].strip()
            elif line.startswith('Type:'):
                temp.type = line.split('Type:')[1].strip()
            elif line.startswith('Size:'):
                temp.size = int(line.split('Size:')[1].strip())
                model.stateVariables.append(temp)
            elif 'VERTICES' in line:
                status = 2
        if status == 2:
            if 'Vertex #' in line:
                temp = Vertex()
            elif line.startswith('Name:'):
                temp.name = line.split('Name:')[1].strip()
            elif line.startswith('Description:'):
                temp.description = line.split('Description:')[1].strip()
            elif line.startswith('State Changes:'):
                temp.stateChanges = line.split('State Changes:')[1].strip().split(',')
                temp.stateChanges = [format_change(x) for x in temp.stateChanges]
                for change in temp.stateChanges:
                    if len(change) > 0:
                        model.compiled[change] = compile(change, '<string>', 'exec')
            elif line.startswith('Parameter(s):'):
                temp.parameters = line.split('Parameter(s):')[1].strip().split(',')
                if not model.vertexes:
                    model.firstEvent = temp.name
                model.vertexes[temp.name] = temp
            elif 'EDGES' in line:
                status = 3
        if status == 3:
            if 'Sub-Edge #' in line:
                temp = Edge()
            elif line.startswith('Description:'):
                temp.description = line.split('Description:')[1].strip()
            elif line.startswith('Type:'):
                temp.type = line.split('Type:')[1].strip()
            elif line.startswith('Origin:'):
                temp.origin = line.split('Origin:')[1].strip()
            elif line.startswith('Destination:'):
                temp.destination = line.split('Destination:')[1].strip()
            elif line.startswith('Condition:'):
                temp.condition = format_change(line.split('Condition:')[1].strip())
                model.compiled[temp.condition] = compile(temp.condition, '<string>', 'eval')
            elif line.startswith('Delay:'):
                temp.delay = format_change(line.split('Delay:')[1].strip())
                model.compiled[temp.delay] = compile(temp.delay, '<string>', 'eval')
            elif line.startswith('Priority:'):
                temp.priority = int(line.split('Priority:')[1].strip())
            elif line.startswith('Attributes:'):
                temp.attributes = line.split('Attributes:')[1].strip().split(',')
                for attribute in temp.attributes:
                    if len(attribute) > 0:
                        model.compiled[attribute] = compile(attribute, '<string>', 'eval')
                if temp.origin not in model.edges:
                    model.edges[temp.origin] = []
                model.edges[temp.origin].append(temp)

    input_file.close()
    return model


def format_change(input_string):
    input_string = input_string.replace('RND', 'random.random()')
    input_string = re.sub(r'DISK\{(.*);0}', r"float(next(data['\1']))", input_string)
    input_string = input_string.replace('PUT{FIF;', 'put(')
    input_string = input_string.replace('GET{FST;', 'get(')
    input_string = input_string.replace('}', ')')
    input_string = input_string.replace('CLK', 'clock')
    input_string = input_string.replace('&', ' and ')
    return input_string
