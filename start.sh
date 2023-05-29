#!/bin/bash
# 启动服务

set -e
set -x

__base__=$(readlink -f $(dirname $(readlink -f $0))/..)
__framework__=${__base__}/framework
__bin__=${__base__}/bin
__conf__=${__base__}/framework/conf

# 动态配置模板
if [ $# -gt 0 ]; then
    template=$1
else
    template=${__conf__}/templates/local.yml
fi

# # 运行前编译
# if [ -e Makefile ]; then
#     make all
# fi

# 生成配置
if [ -e ${template} ]; then
    python3 ${__framework__}/scripts/generate_config.py -d ${template} -r ${__conf__} -e etcd.yml.j2
fi

# # 启动 grpc 服务
# python3 -m src.grpc conf/grpc.yml
