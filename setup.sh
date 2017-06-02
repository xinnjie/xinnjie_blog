#! /bin/bash
# set up redis
redis-server
config set maxmemory 10mb
maxmemory-policy allkeys-lru