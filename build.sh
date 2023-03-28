#!/bin/bash

# 安装 PostgreSQL 客户端和库文件
sudo apt-get install -y postgresql
sudo apt-get install -y libpq-dev

# 创建数据库
sudo -u postgres createdb mydb

# 克隆、编译、安装 pgvector 扩展
git clone --branch v0.4.0 https://github.com/pgvector/pgvector.git /tmp/pgvector
cd /tmp/pgvector
make
sudo make install
