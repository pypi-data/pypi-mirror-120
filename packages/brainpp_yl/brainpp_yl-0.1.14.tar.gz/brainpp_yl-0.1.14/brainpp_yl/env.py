#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Sat Jul 20 22:48:51 2019
"""

import os
import socket

RLAUNCH_REPLICA = int(os.environ.get("RLAUNCH_REPLICA", 0))
RLAUNCH_REPLICA_TOTAL = int(os.environ.get("RLAUNCH_REPLICA_TOTAL", 1))

replica_idx = int(os.environ.get("RJOB_REPLICA", RLAUNCH_REPLICA))
replica_total = int(os.environ.get("RJOB_REPLICA_TOTAL", RLAUNCH_REPLICA_TOTAL))

is_replica = replica_total > 1  # `bpp.isReplica`: 判断是否为 replica 模式


try:
    import torch

    gpun = torch.cuda.device_count()
    direction = ["output", "input"][gpun > 0]
    device = torch.device("cpu")
except ImportError:
    gpun = 0
    direction = "output"
    device = "cpu"


def get_host_type():
    """Get type of current container

    :return: either None 'WORKER', 'VM', 'VM2' or 'WORKSPACE'
    """
    if not os.path.exists("/data/"):
        return None
    fqdn = socket.getfqdn()
    if os.getenv("RLAUNCH_WORKER") or os.getenv("rrun_executor_uri"):
        return "WORKER"
    mapping = {
        "brw": "WORKSPACE",
        "brc": "VM",
        "vm2": "VM2",
    }
    if "brainpp" not in fqdn:
        return None
    try:
        type_ = fqdn.split(".")[2]
        return mapping.get(type_)
    except IndexError:
        return None
    """Consider isfile("/usr/local/bin/rlaunch") """


host_type = get_host_type()

if __name__ == "__main__":
    pass
