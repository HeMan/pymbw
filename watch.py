import datetime, re

class parser(object):
        def __init__(self):
                pass
        def do_atstarseam(self, argument):
                print "Create menu (%s)" % argument
                return "*SEAM: 6101"

        def do_atstarseadio(self, argument):
                print "Set audio"
                return "ERROR"

        def do_atpluscclk(self, argument):
                print "Set clock"
                return datetime.datetime.now().strftime("+CCLK: \"%y/%m/%d,%H:%M:%S+04\"")

        def do_default(self, argument):
                print "Default action"
                return "OK"                        
        def do_atstarsemp(self, argument):
            print "Multimedia"
            print argument
            if argument == 1:
                print "Play"
            elif argument == 2:
                print "Pause"
            elif argument == 5:
                print "Next"
            return "OK"

        def parse(self, string):
                setget = False
                query = False
                if "=" in string:
                        (command,argument) = string.split("=")
                        setget = True
                elif "?" in string:
                        (command,argument) = string.split("?")
                        query = True
                new_command = re.sub("\+", "plus", re.sub("\*", "star", command.lower()))
                function = getattr(self, "do_%s" % new_command, self.do_default)
                return function(argument)
