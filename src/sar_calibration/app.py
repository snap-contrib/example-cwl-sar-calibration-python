import os
import sys
import click
from click2cwl import dump
from .calibration_s1 import graph_calibrate_s1
import logging


logging.basicConfig(
    stream=sys.stderr,
    level=logging.CRITICAL,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

@click.command(
    short_help="Sentinel-1 GRD calibration",
    help="Sentinel-1 GRD calibration",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.option(
    "--safe",
    "-s",
    "safe",
    help="Path the Sentinel-1 SAFE folder",
    type=click.Path(),
    required=True,
)
@click.pass_context
def main(ctx, safe):

    dump(ctx)

    logging.info(f"{safe} calibration")

    graph = graph_calibrate_s1(safe)

    logging.info(graph.view())

    graph.run()

    logging.info("Hello World!")


if __name__ == "__main__":
    main()
