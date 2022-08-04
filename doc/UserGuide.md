# User Guide

The architecture of the XPU Container Toolkit allows for different container engines in the ecosystem(docker) to be supported easily.

## Docker

The XPU Container Toolkit provides different options for enumerating XPUs and the capabilities that are supported for XPU containers. This user guide demonstrates the following features of the XPU Container Toolkit:

- Registering the XPU runtime as a custom runtime to Docker
- Using environment variables to enable the following:
    - Enumerating XPUs and controlling which XPUs are visible to the container
    - Controlling which features of the driver are visible to the container using capabilities
    - Controlling the behavior of the runtime using constraints

### Adding the XPU Runtime

> Warning: Do not follow this section if you installed the `xpu-docker` package, it already registers the runtime.

To register the **xpu container runtime**, use the method below that is best suited to your environment. You might need to merge the new argument with your existing configuration. Three options are available:

#### Systemd drop-in file

```
$ sudo mkdir -p /etc/systemd/system/docker.service.d
```
```
$ sudo tee /etc/systemd/system/docker.service.d/override.conf <<EOF
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd --host=fd:// --add-runtime=xpu=/usr/bin/xpu-container-runtime
EOF
```
```
$ sudo systemctl daemon-reload \
  && sudo systemctl restart docker
```

#### Daemon configuration file

The **xpu container runtime** can also be registered with Docker using the `daemon.json` configuration file:

```
$ sudo tee /etc/docker/daemon.json <<EOF
{
    "runtimes": {
        "xpu": {
            "path": "/usr/bin/xpu-container-runtime",
            "runtimeArgs": []
        }
    }
}
EOF
```
```
$ sudo pkill -SIGHUP dockerd
```

You can optionally reconfigure the default runtime by adding the following to `/etc/docker/daemon.json`:

```
"default-runtime": "xpu"
```

#### Command Line

Use dockerd to add the xpu container runtime:

```
$ sudo dockerd --add-runtime=xpu=/usr/bin/xpu-container-runtime [...]
```

### Environment variables (OCI spec)

Users can control the behavior of the XPU container runtime using environment variables - especially for enumerating the XPUs and the capabilities of the driver. Each environment variable maps to an command-line argument for `xpu-container-cli` from `libnvidia-container`. These variables are already set in the KunLunXin provided base XPU images.

#### XPU Enumeration

XPUs can be specified to the Docker CLI using the environment variable `CXPU_VISIBLE_DEVICES`. This variable controls which XPUs will be made accessible inside the container.

The possible values of the `CXPU_VISIBLE_DEVICES` variable are:

| Possible values        | Description |
|------------------------|-------------|
| 0,1,2,                 | a comma-separated list of XPU index(es) |
| all                    | all XPUs will be accessible, this is the default value in base XPU container images |
| none                   | no XPU will be accessible, but driver capabilities will be enabled. |
| void or empty or unset | xpu-container-runtime will have the same behavior as runc |

> When using the `CXPU_VISIBLE_DEVICES` variable, you may need to set `--runtime` to `xpu` **unless already set as default**.

Some examples of the usage are shown below:

1. Starting a XPU enabled XPU container; Using XPU_VISIBLE_DEVICES and specify the xpu runtime
```
docker run --rm --runtime=xpu -e CXPU_VISIBLE_DEVICES=all ubuntu:latest xpu_smi
```

2. Start a XPU enabled container on two XPUs

```
docker run --rm --runtime=xpu -e CXPU_VISIBLE_DEVICES=0,1 ubuntu:latest xpu_smi
```

### Dockerfiles

Capabilities and XPU enumeration can be set in images via environment variables. If the environment variables are set inside the Dockerfile, you don’t need to set them on the `docker run` command-line.

For instance, if you are creating your own custom XPU container, you should use the following:

```
ENV CXPU_VISIBLE_DEVICES all
```

The environment variables are already set in the XPU provided CXPU images.

### Troubleshooting

Generating debugging logs
For most common issues, debugging logs can be generated and can help us root cause the problem. In order to generate these:

- Edit your runtime configuration under `/etc/xpu-container-runtime/config.toml` and uncomment the `debug=...` line.
- Run your container again, thus reproducing the issue and generating the logs.

### Generating core dumps

In the event of a critical failure, core dumps can be automatically generated and can help us troubleshoot issues. Refer to core(5) in order to generate these, in particular make sure that:

- `/proc/sys/kernel/core_pattern` is correctly set and points somewhere with write access
- ulimit -c is set to a sensible default

In case the `xpu-container-cli` process becomes unresponsive, gcore(1) can also be used.

### Sharing your debugging information

You can attach a particular output to your issue with a drag and drop into the comment section.
