import os
import sys
import logging
import click

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command()
@click.option('--input_reference', '-i', 'input_reference', help='')
def main(input_reference, aoi):

    logging.info('Hello World!')

if __name__ == '__main__':
    main()
