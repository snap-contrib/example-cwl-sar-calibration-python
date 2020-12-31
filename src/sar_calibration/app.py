import os
import sys
import logging
import click

# from snapista import Graph
from .calibration_s1 import graph_calibrate_s1

logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


@click.command()
@click.option("--safe", "safe", help="Path to Sentinel-1 SAFE folder")
def main(safe):

    logging.info(f"{safe} calibration")

    graph = graph_calibrate_s1(safe)

    logging.info(graph.view())

    graph.run()

    logging.info("Hello World!")


if __name__ == "__main__":
    main()
