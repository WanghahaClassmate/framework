#!/usr/bin/env python3
#coding=utf-8
#利用jinja2框架生成配置文件

import argparse
import os
import yaml

from jinja2 import Environment, FileSystemLoader

# command arguments
parser = argparse.ArgumentParser()
parser.add_argument(
        '-d', '--data',
        help = 'data of config template',
        dest = 'data',
        metavar = 'data-filename',
        required = True
        )
parser.add_argument(
        '-r', '--root',
        help = 'root of config template',
        dest = 'root',
        metavar = 'root-directory',
        default = None,
        required = True,
        )
parser.add_argument(
        '-e', '--exclude',
        help = 'exclude config template filenames',
        dest = 'exclude',
        metavar = 'file',
        default = [],
        nargs = '*',
    )
parser.add_argument(
        '-f', '--file',
        help = 'config template filename',
        dest = 'file',
        metavar = 'file',
        default = None,
    )

args = parser.parse_args()

# load data from yaml file
config = yaml.safe_load(open(args.data, 'r', encoding='utf-8'))

# load jinja2 template
env = Environment(loader = FileSystemLoader(args.root, encoding='utf-8'), trim_blocks=True, lstrip_blocks=True)

def generateFile(src, dest):
    '''
    根据模板文件生成结果
    @param src: 模板文件名
    @param dest: 目标文件名
    '''
    template = env.get_template(src)

    with open(dest, 'w', encoding='utf-8') as f:
        print('# AUTO GENERATED BY JINJA2', file=f)
        print(template.render(config), file=f)

    print('[{}] generate [{}] by jinja2 DONE'.format(src, dest))

# find all j2 template file under ../
for root, dirs, files in os.walk(args.root):
    for filename in files:
        if filename in args.exclude: continue
        if args.file is not None and filename != args.file: continue

        name, ext = os.path.splitext(filename)

        if ext != '.j2': continue

        # 模板文件名
        templateFilename = os.path.relpath(os.path.join(root, filename), args.root)
        # 新的文件名
        newFilename = os.path.join(root, name)

        generateFile(templateFilename, newFilename)
