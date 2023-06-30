# -*- coding: utf-8 -*-

DESCRIPTION = """update papers pl-marker"""

import sys, os, time
from pathlib import Path
from datetime import datetime
from timeit import default_timer as timer
try:
    from humanfriendly import format_timespan
except ImportError:
    def format_timespan(seconds):
        return "{:.2f} seconds".format(seconds)

import logging
root_logger = logging.getLogger()
logger = root_logger.getChild(__name__)

from entrypoint import run_command

def main(args):
    dirpath = Path("/scierc")
    for fp in dirpath.glob("titles_abstracts_*plmarker_scierc*.json"):
        logfp = Path(f"/output/{fp.stem}.log")
        logger.info(f"processing file {fp}. logfile: {logfp}")
        use_gpu = not args.no_gpu
        run_command(str(fp), logfp, gpu=use_gpu, batch=args.batch)

if __name__ == "__main__":
    total_start = timer()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(name)s.%(lineno)d %(levelname)s : %(message)s", datefmt="%H:%M:%S"))
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    logger.info(" ".join(sys.argv))
    logger.info( '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) )
    logger.info("pid: {}".format(os.getpid()))
    import argparse
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--no-gpu", action='store_true', help="don't use gpu")
    parser.add_argument("--batch", type=int, default=60, help="batch size (default: 60")
    parser.add_argument("--debug", action='store_true', help="output debugging info")
    global args
    args = parser.parse_args()
    if args.debug:
        root_logger.setLevel(logging.DEBUG)
        logger.debug('debug mode is on')
    main(args)
    total_end = timer()
    logger.info('all finished. total time: {}'.format(format_timespan(total_end-total_start)))
