# Websocket Proxy Lib

Library that contains a Proxy for KubeVirts VNC Websockets. It uses JWT Tokens for Authentication and to transfer data.

## Installation

- `pip3 install lab-orchestrator-ws-proxy-lib`

## Documentation

Check out the developer documentation at [websocketproxylib.readthedocs.io](https://websocketproxylib.readthedocs.io/en/latest/).

## Usage

The library contains one module called ws_proxy_lib that contains one class. This class contains a `run` and a `run_in_thread` method that can be used to start the proxy.

First you need to initialize an object of the class. For that you need to pass some parameters:

- `remote_url`: The base URL to the Kubernetes api (for example `"ws://localhost:8001"`)
- `api_path`: The path in the api that points to a VMI. This needs to contain the variables `{namespace}` and `{vmi_name}` (for example `"/apis/subresources.kubevirt.io/v1alpha3/namespaces/{namespace}/virtualmachineinstances/{vmi_name}/vnc"`)
- `local_dev_mode`: This is a boolean that indicated if you are running the lib locally in a development mode or running it in a Kubernetes cluster. Running it locally disables ssl. Running it in Kubernetes will automatically include the TLS client certificate from `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt` and use the token from `/var/run/secrets/kubernetes.io/serviceaccount/token`.
- `secret_key`: The key that is used to decrypt the token.

After that you can just start the proxy with the `run` and a `run_in_thread` method. Use the parameters `host` and `port` to specify on which host and port this runs.

The proxy works as follows:

It creates a websocket at the given host and port. Then when you want to access a VM you need to call the websocket with a path that contains the token and the VM-name divided by a slash. Example: `localhost:5001/ABCTOKENDEF/ubuntu`. The example contains the token `ABCTOKENDEF` and tries to access the VM with the name `ubuntu`. The token contains a list of allowed VM-names and if the given VM-name is part of the token you will be able to access the VM.

See more at: [websocketproxylib.readthedocs.io](https://websocketproxylib.readthedocs.io/en/latest/).

## Examples

For an example on how to use this library you can take a look at the [WebsocketProxy Project](https://github.com/LabOrchestrator/WebsocketProxy) which uses this library and integrates it into a docker image.

## Contributing

### Issues

Feel free to open [issues](https://github.com/LabOrchestrator/WebsocketProxyLib/issues).

### Project Structure

The `src` folder contains the source code of the library. The `tests` folder contains the test cases. There is a makefile that contains some shortcuts for example to run the test cases and to make a release. Run `make help` to see all targets. The `docs` folder contains rst docs that are used in [websocketproxylib.readthedocs.io](https://websocketproxylib.readthedocs.io/en/latest/).

### Developer Dependencies

- Python 3.8
- Make
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`

### Releases

Your part:

1. Create branch for your feature (`issue/ISSUE_ID-SHORT_DESCRIPTION`)
2. Code
3. Make sure test cases are running and add new ones for your feature
4. Create MR into master
5. Increase version number in `src/lab_orchestrator_ws_proxy_lib/__init__.py` (semantic versioning)

Admin part:

1. Check and accept MR
2. Merge MR
3. Run `make release`

### Docs

To generate the docs run: `cd docs && make html`.
