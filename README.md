# XPU Container Toolkit

[![GitHub license](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](https://raw.githubusercontent.com/zxw3221/xpu-container-toolkit/master/LICENSE)
[![Documentation](https://img.shields.io/badge/documentation-wiki-blue.svg?style=flat-square)](https://github.com/zxw3221/xpu-container-toolkit/blob/master/README.md)
[![GitHub release](https://img.shields.io/github/release/zxw3221/xpu-container-toolkit/all.svg?style=flat-square)](https://github.com/zxw3221/xpu-container-toolkit/releases)

## Introduction

The XPU Container Toolkit allows users to build and run XPU accelerated containers. The toolkit includes a container runtime [library](https://github.com/zxw3221/libxpu-container) and utilities to automatically configure containers to leverage XPUs.

Product documentation including an architecture overview, platform support, and installation and usage guides can be found in the [documentation repository](todo).

## Getting Started

### Pre-Requisites

**Before you get started, Make sure you have installed [XRE](https://console.cloud.baidu-int.com/devops/ipipe/workspaces/204599/releases/list)(XPU Runtime Environment) for your Linux Distribution.**

### Install XPU-container-toolkit

1. Get the latest [libxpu-container release package](https://github.com/zxw3221/libxpu-container/releases) and install it.
2. Get the latest [xpu-container-toolkit release package](https://github.com/zxw3221/xpu-container-toolkit/releases) and install it.

**Example on CentOS:**

1. **Install** libxpu-container 

```
$ sudo rpm -ivh libxpu-container0-0.1.0-1.x86_64.rpm
Verifying...                          ################################# [100%]
Preparing...                          ################################# [100%]
Updating / installing...
   1:libxpu-container0-0.1.0-1        ################################# [100%]

$ sudo rpm -ivh libxpu-container-tools-0.1.0-1.x86_64.rpm 
Verifying...                          ################################# [100%]
Preparing...                          ################################# [100%]
Updating / installing...
   1:libxpu-container-tools-0.1.0-1   ################################# [100%]
```

2. **Install** xpu-container-toolkit

```
$ sudo rpm -ivh xpu-container-toolkit-0.1.0-0.1.rc.1.x86_64.rpm
Verifying...                          ################################# [100%]
Preparing...                          ################################# [100%]
Updating / installing...
   1:xpu-container-toolkit-0.1.0-0.1.r################################# [100%]
```

### Test xpu-container-toolkit

```
$ xpu-container-cli info
Driver version: 4.0.third_unknown.1 commit: ded73a5dd24251ec339afb0bf305a0432336e664
XPUML version:  4.0.18.1 commit: ded73a5dd24251ec339afb0bf305a0432336e664

Device Index:   0
Device Minor:   0
Model:          R200
Brand:          Kunlun
Serial Number:  02K00Y6217V00009
Bus Location:   00000000:01:00.00
Architecture:   2.0

Device Index:   1
Device Minor:   2
Model:          K100
Brand:          Kunlun
Serial Number:  000000000000022f
Bus Location:   00000000:06:00.00
Architecture:   1.0
```

## Usage

The [**User Guide**](https://github.com/zxw3221/xpu-container-toolkit/blob/master/doc/UserGuide.md) provides information on the configuration and command line options available when running XPU containers with Docker.

**Example on CentOS:**

1. **Add** xpu docker runtime configuration to `/etc/docker/daemon.json` to register XPU docker runtime.

```
    "default-runtime": "xpu",
    "runtimes": {
        "xpu": {
            "path": "/usr/bin/xpu-container-runtime",
            "runtimeArgs": []
        }
    }
```

2. **Restart** docker to make XPU runtime configuration work.

```
$ sudo systemctl restart docker
```

3. **Run** docker with XPU0 and XPU1 and check devices status by xpu_smi in container.

```
$ docker run -it -e CXPU_VISIBLE_DEVICES=0,1 --rm ubuntu:latest xpu_smi

  DEVICES
--------------------------------------------------------------------------------------------------
| DevID |   PCI Addr   | Model | ... |    INODE   | State | UseRate |    L3     |   Memory   |...| 
--------------------------------------------------------------------------------------------------
|     0 | 0000:01:00.0 | R200  | ... | /dev/xpu0  |     N |     0 % | 0 / 63 MB |0 / 16384MB |...|
|     1 | 0000:06:00.0 | K100  | ... | /dev/xpu1  |     N |     0 % | 0 / 16 MB |0 / 8064 MB |...|
--------------------------------------------------------------------------------------------------
...

```

4. **Run** docker with XPU0 and set container memory limit to 100MB.

```
$ docker run -it -e CXPU_VISIBLE_DEVICES=0 -e CXPU_CONTAINER_MEMORY_LIMIT=100000000 --rm ubuntu:latest xpu_smi

  DEVICES
---------------------------------------------------------------------------------------------------
| DevID |   PCI Addr   | Model | ... |    INODE   | State | UseRate |    L3     |  Memory   | ... |
---------------------------------------------------------------------------------------------------
|     0 | 0000:01:00.0 | R200  | ... | /dev/xpu0  |     N |     0 % | 0 / 63 MB | 0 / 95 MB | ... |
---------------------------------------------------------------------------------------------------
...

```

## Issues and Contributing

[Checkout the Contributing document!](CONTRIBUTING.md)

* Please let us know by [filing a new issue](https://github.com/zxw3221/xpu-container-toolkit/issues/new)
* You can contribute by creating a [pull request](https://github.com/zxw3221/xpu-container-toolkit/pull/new) to our public Github repository
