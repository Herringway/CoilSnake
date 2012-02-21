#! /usr/bin/env python

import argparse
import sys
import os

import Rom

def loadModules():
    modules = []
    with open('modulelist.txt', 'r') as f:
        for line in f:
            line = "modules." + line.rstrip('\n')
            mod = __import__(line)
            components = line.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            modules.append(getattr(mod,components[-1])())
    return modules

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleanrom', dest='cleanrom', required=False,
        type=argparse.FileType('rb'), help="a clean, unmodified ROM")
    parser.add_argument('input', metavar='INPUT', type=argparse.FileType('r'),
        help="either a ROM or a CoilSnake project file")
    parser.add_argument('output', metavar='OUTPUT',
        help="either a ROM or a CoilSnake project file")
    args = parser.parse_args()

    output_is_proj = os.path.splitext(args.output)[1] == ".csp"
    if (not output_is_proj) and (args.cleanrom == None):
        print >> sys.stderr, "ERROR: Need a clean ROM to export to ROM"
        return

    modules = loadModules()

    # Load data into modules
    if os.path.splitext(args.input.name)[1] == ".csp":
        # TODO load project file
        pass
    else:
        input = Rom.Rom("romtypes.yaml")
        input.load(args.input)
        for m in filter(lambda x: x.compatibleWithRom(input), modules):
            m.readFromRom(input)

    # Save data from modules
    if output_is_proj:
        # TODO save project file
        pass
    else:
        output = Rom.Rom("romtypes.yaml")
        output.load(args.cleanrom)
        for m in filter(lambda x: x.compatibleWithRom(output), modules):
            m.writeToRom(output)
        output.save(args.output)

if (__name__ == '__main__'):
    sys.exit(main())