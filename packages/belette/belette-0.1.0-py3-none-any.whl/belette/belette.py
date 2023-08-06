#!/usr/bin/env python3
'''Belette - Generates licensing information for dependencies for Conan projects

Usage:
  belette generate [-s=<setting>...] [-o=<option>...] <path> <output_file>
  belette (-h | --help)
  belette --version

Commands:
  generate  Creates a file that contains information about all the dependencies
            of a project and their associated licenses. <path> must point to the
            root of a Conan project, which should contain conanfile.py or
            conanfile.txt. <output_file> must be a .hpp file.

Options:
  -o=<option>   Options. Similar to the `-o` parameter of the conan command
  -s=<setting>  Settings. Similar to the `-s` parameter of the conan command
  -h --help     Show this screen.
  --version     Show version.

'''

import os

from conans.client.conan_api import ConanAPIV1
from textwrap import dedent
from docopt import docopt
import jinja2


def main():
    arguments = docopt(__doc__, version='Belette')
    if arguments['generate']:
        generate(arguments['<path>'], arguments['-s'], arguments['-o'],
                 arguments['<output_file>'])


def generate(path, settings, options, output_file):
    if not output_file.endswith('.hpp'):
        raise ValueError("Output file should end in .hpp")

    cwd = os.path.dirname(os.path.realpath(__file__))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.join(cwd, 'templates')),
                             undefined=jinja2.StrictUndefined,
                             trim_blocks=True)
    template = env.get_template('template.hpp')

    info = {
        'generated_file_warning':
        dedent('''\
            WARNING: this file is generated, do not edit manually, nor commit
            to source control. Your changes will be overriden'''),
        'packages': [],
        'licenses': {}
    }

    api = ConanAPIV1()
    graph, _ = api.info(path, options=options, settings=settings)
    for node in graph.nodes:
        if node is graph.root:
            continue  # this node is not a dependency
        if ((not node.conanfile.license)
                or (node.conanfile.license == "proprietary")):
            continue  # this node is not open-source
        license = node.conanfile.license
        if type(license) in [list, tuple]:
            # If the package supports multiple licenses, make things simple by
            # choosing the first one
            license = license[0]
        info['packages'].append({
            'name': node.name,
            'license': license,
            'version': node.conanfile.version,
            'homepage': node.conanfile.homepage
        })

    for package in info['packages']:
        lic = package['license']
        if lic not in info['licenses']:
            licpath = "{}/licenses/{}.txt".format(cwd, lic)
            if not os.path.isfile(licpath):
                raise ValueError(
                    "Could not find full license text for license {} for package {}"
                    .format(lic, package['name']))
            with open(licpath, 'r') as licfile:
                info['licenses'][lic] = licfile.read()

    with open(output_file, 'w') as ofile:
        ofile.write(template.render(info))


if __name__ == "__main__":
    main()
