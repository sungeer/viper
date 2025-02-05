#!/bin/bash

# 检查是否为目标服务器
if [ "$RUN_HUEY" = "true" ]; then
    # 启动 Huey worker
    huey_consumer viper.delays.huey_instance.huey
else
    echo "Huey is not configured to run on this server."
fi
