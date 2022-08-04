# The XPU Container Runtime

The XPU Container Runtime is a shim for OCI-compliant low-level runtimes such as [runc](https://github.com/opencontainers/runc). When a `create` command is detected, the incoming [OCI runtime specification](https://github.com/opencontainers/runtime-spec) is modified in place and the command is forwarded to the low-level runtime.

## Configuration

The XPU Container Runtime uses file-based configuration, with the config stored in `/etc/xpu-container-runtime/config.toml`. The `/etc` path can be overridden using the `XDG_CONFIG_HOME` environment variable with the `${XDG_CONFIG_HOME}/xpu-container-runtime/config.toml` file used instead if this environment variable is set.

This config file may contain options for other components of the XPU container stack and for the XPU Container Runtime, the relevant config section is `xpu-container-runtime`

### Logging

The `log-level` config option (default: `"info"`) specifies the log level to use and the `debug` option, if set, specifies a log file to which logs for the XPU Container Runtime must be written.

In addition to this, the XPU Container Runtime considers the value of `--log` and `--log-format` flags that may be passed to it by a container runtime such as docker or containerd. If the `--debug` flag is present the log-level specified in the config file is overridden as `"debug"`.

### Low-level Runtime Path

The `runtimes` config option allows for the low-level runtime to be specified. The first entry in this list that is an existing executable file is used as the low-level runtime. If the entry is not a path, the `PATH` is searched for a matching executable. If the entry is a path this is checked instead.

The default value for this setting is:
```toml
runtimes = [
    "docker-runc",
    "runc",
]
```

and if, for example, `crun` is to be used instead this can be changed to:
```toml
runtimes = [
    "crun",
]
```

### Runtime Mode

The `mode` config option (default `"auto"`) controls the high-level behaviour of the runtime.

#### Auto Mode

When `mode` is set to `"auto"`, the runtime employs heuristics to determine which mode to use based on, for example, the platform where the runtime is being run.

#### Legacy Mode

When `mode` is set to `"legacy"`, the XPU Container Runtime adds a [`prestart` hook](https://github.com/opencontainers/runtime-spec/blob/master/config.md#prestart) to the incomming OCI specification that invokes the XPU Container Runtime Hook for all containers created. This hook checks whether XPU devices are requested and ensures GPU access is configured using the `xpu-container-cli` from the [libxpu-container](https://github.com/zxw3221/libxpu-container) project.

### Notes on using the docker CLI

Note that only the `"legacy"` XPU Container Runtime mode is directly compatible with the `--gpus` flag implemented by the `docker` CLI (assuming the XPU Container Runtime is not used). The reason for this is that `docker` inserts the same XPU Container Runtime Hook into the OCI runtime specification.

If a different mode is explicitly set or detected, the XPU Container Runtime Hook will raise the following error when `--gpus` is set:
```
$ docker run --rm --gpus all ubuntu:18.04
docker: Error response from daemon: failed to create shim: OCI runtime create failed: container_linux.go:380: starting container process caused: process_linux.go:545: container init caused: Running hook #0:: error running hook: exit status 1, stdout: , stderr: Auto-detected mode as 'csv'
invoking the XPU Container Runtime Hook directly (e.g. specifying the docker --gpus flag) is not supported. Please use the XPU Container Runtime instead.: unknown.
```
Here XPU Container Runtime must be used explicitly. The recommended way to do this is to specify the `--runtime=xpu` command line argument as part of the `docker run` commmand as follows:
```
$ docker run --rm --gpus all --runtime=xpu ubuntu:18.04
```

Alternatively the XPU Container Runtime can be set as the default runtime for docker. This can be done by modifying the `/etc/docker/daemon.json` file as follows:
```json
{
    "default-runtime": "xpu",
    "runtimes": {
        "xpu": {
            "path": "xpu-container-runtime",
            "runtimeArgs": []
        }
    }
}
```
