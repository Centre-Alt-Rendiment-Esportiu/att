# -*- coding: utf-8 -*-

class ConfigurationReader:
    props = {}

    def __init(self):
        pass

    def loadFromFile(self, strFilePath):
        lines = [line.strip() for line in file(strFilePath) if not line.startswith("#")]
        for line in lines:
            lineSplit = line.split("=")
            if len(lineSplit) > 1:
                self.props[lineSplit[0]] = lineSplit[1]


"""
strFilePath = "../../resources/att.conf"

c = ConfigurationReader()
c.loadFromFile(strFilePath)
print c.props
"""
