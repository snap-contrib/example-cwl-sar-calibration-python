# Using CWL and docker to calibrate Sentinel-1 GRD with SNAP

This repo contains an example of how to use the Common Workflow Language (CWL) and containers to process Sentinel-1 GRD data with SNAP.

The Python project implements a simple command line tool that takes a Sentinel-1 SAFE path and generates a SAR calibrated geotiff.

The command line tool self describes itself as a CWL tool using the click2cwl Python module

## Requirements

### CWL runner

The CWL runner executes CWL documents. 

Follow the installation procedure provided [here](https://github.com/common-workflow-language/cwltool#install)

### Docker

The SNAP processing runs in a docker container so docker is required. 

Follow the installation steps for your computer provided [here](https://docs.docker.com/get-docker/)

If needed follow the additional steps described [here](https://docs.docker.com/engine/install/linux-postinstall/) to allow the CWL runner to manage docker as a non-root user.

## Getting started 

### Setting-up the container

Clone this repository and build the docker image with:

```console
git clone https://github.com/snap-contrib/example-cwl-sar-calibration-python.git
cd example-cwl-sar-calibration
docker build -t sar-calibration:latest  -f .docker/Dockerfile .
```

Check the docker image exists with:

```console
docker images | grep sar-calibration
```

This returns one line with the docker image just built.

Check if SNAP `gpt` utility is available in the container:

```console
docker run --rm -it sar-calibration gpt -h
```

This dumps the SNAP `gpt` utiliy help message.

Check the SNAP/snappy installation:

```console
docker run --rm -it sar-calibration python -c "from snappy import GPF"
```

This won't return anything if everything is ok.

Check the `sar-calibration` command line tool is properly built and installeg with:

```console
docker run --rm -it sar-calibration sar-calibration --help
```

This will dump:

```bash
Usage: sar-calibration [OPTIONS]

  Sentinel-1 GRD calibration

Options:
  -s, --safe PATH  Path the Sentinel-1 SAFE folder  [required]
  --help           Show this message and exit.
```

### Getting the CWL document

The `sar-calibration` Python project uses the `click2cwl` Python module to generate the CWL document. 

The CWL document is produced with:

```console
docker run --rm -it sar-calibration sar-calibration --safe dummy --docker sar-calibration:latest --scatter safe --dump cwl > sar-calibration.cwl
```

Breaking down the parameters used:

- `--safe dummy`: the `--safe` is a mandatory parameter so a dummy value is provided
- `--docker sar-calibration:latest`: this sets the docker image inside the CWL document and thus tells CWL which container image to spin to run the `sar-calibration` command line utility
- `--scatter safe`: this sets the CWL document to scatter the inputs, i.e. to fan-out the Sentinel-1 GRD acquisitions to process several acquisitions
- `--dump cwl`: this dumps the CWL

The output is redirected to a file called `sar-calibration.cwl`

### Getting a few Sentinel-1 GRD acquistions

Download a couple of Sentinel-1 GRD acquisitions and unzip them.

### Preparing the input parameters for the CWL step

The CWL parameters file is a YAML file with an array of input directories pointing to the SAFE folders:

```yaml
safe: 
- {'class': 'Directory', 'path': '/home/fbrito/Downloads/S1A_IW_GRDH_1SDV_20210615T050457_20210615T050522_038346_048680_F42E.SAFE'}
```

Save this content in a file called `params.yml`.

### Process the data

```console
cwltool sar-calibration.cwl#sar-calibration params.yml
```

This will process the Sentinel-1 GRD acquisitions with an output as:

```
INFO /srv/conda/bin/cwltool 3.0.20210319143721
INFO Resolved 'sar-calibration.cwl#sar-calibration' to 'file:///home/fbrito/work/example-cwl-sar-calibration-python/sar-calibration.cwl#sar-calibration'
INFO [workflow ] start
INFO [workflow ] starting step step_1
INFO [step step_1] start
INFO [job step_1] /tmp/y0hlh2bp$ docker \
    run \
    -i \
    --mount=type=bind,source=/tmp/y0hlh2bp,target=/IGyPIl \
    --mount=type=bind,source=/tmp/vn06wbni,target=/tmp \
    --mount=type=bind,source=/home/fbrito/Downloads/S1A_IW_GRDH_1SDV_20210615T050457_20210615T050522_038346_048680_F42E.SAFE,target=/var/lib/cwl/stg13469f92-512a-4d61-b79d-1049b97f4bf7/S1A_IW_GRDH_1SDV_20210615T050457_20210615T050522_038346_048680_F42E.SAFE,readonly \
    --workdir=/IGyPIl \
    --read-only=true \
    --log-driver=none \
    --user=1000:1000 \
    --rm \
    --env=TMPDIR=/tmp \
    --env=HOME=/IGyPIl \
    --cidfile=/tmp/seos20fo/20210616095504-971995.cid \
    --env=PATH=/srv/conda/envs/env_sar_calibration/bin:/srv/conda/envs/env_sar_calibration/snap/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    sar-calibration:latest \
    sar-calibration \
    --safe \
    /var/lib/cwl/stg13469f92-512a-4d61-b79d-1049b97f4bf7/S1A_IW_GRDH_1SDV_20210615T050457_20210615T050522_038346_048680_F42E.SAFE > /tmp/y0hlh2bp/std.out 2> /tmp/y0hlh2bp/std.err
```

At the end, it will list the files generated.

