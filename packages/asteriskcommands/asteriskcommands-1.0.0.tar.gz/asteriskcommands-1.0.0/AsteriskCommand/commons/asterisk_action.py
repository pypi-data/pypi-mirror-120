class Action(object):
    def __init__(self, name, keys=None, variables=None):
        self.name = name
        self.keys = keys or dict()
        self.variables = variables or dict()

    def __str__(self):
        package = "Action: %s\r\n" % self.name
        for key in self.keys:
            if key != "Action" and key != "Variables":
                package += "%s: %s\r\n" % (key, self.keys[key])
        for var in self.variables:
            package += "Variable: %s=%s\r\n" % (var, self.variables[var])
        return package

    def __getattr__(self, item):
        return self.keys[item]

    def __setattr__(self, key, value):
        if key in ("name", "keys", "variables"):
            return object.__setattr__(self, key, value)
        self.keys[key] = value

    def __setitem__(self, key, value):
        self.variables[key] = value

    def __getitem__(self, item):
        return self.variables[item]
