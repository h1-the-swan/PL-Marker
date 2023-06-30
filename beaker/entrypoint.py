# -*- coding: utf-8 -*-

DESCRIPTION = """entrypoint for running in a beaker task"""

from ast import literal_eval
import shutil
import subprocess
from multiprocessing import Pool, cpu_count
import sys, os, time
import re
from pathlib import Path
from datetime import datetime
from timeit import default_timer as timer
from typing import Iterable, List, Set

try:
    from humanfriendly import format_timespan
except ImportError:

    def format_timespan(seconds):
        return "{:.2f} seconds".format(seconds)


import logging

root_logger = logging.getLogger()
logger = root_logger.getChild(__name__)

FILE_INDEX_PATTERN = re.compile(r"(\d\d\d\d\d\d)")

PATH_TO_SCRIPT = "/stage/run_acener_modified.py"
from command_args import get_arguments


def run_command(
    input_filename: str,
    logfp: Path,
    path_to_script=PATH_TO_SCRIPT,
    gpu=False,
    batch=60,
):
    with logfp.open("w") as logf:
        argv = get_arguments(input_filename, batch_size=batch)
        cmd = ["python", path_to_script] + argv
        if gpu is False:
            cmd.append("--no_cuda")
        logger.info(f"running command: {cmd}")
        subprocess.run(cmd, stdout=logf, stderr=subprocess.STDOUT)


def get_existing_output_files() -> List[str]:
    dirpath = Path("/output")
    existing_files = list(dirpath.rglob("ent_pred*.json"))
    return [fp.name for fp in existing_files]


def get_group_index_from_fname(fname: str) -> int:
    idx_str = FILE_INDEX_PATTERN.search(fname).group(1)
    return int(idx_str)


def output_exists(input_filename: str, output_file_indices: List[int]) -> bool:
    return get_group_index_from_fname(input_filename) in output_file_indices


def remove_existing(file_indices: Iterable[int]) -> Set[int]:
    ignore_files = get_existing_output_files()
    ignore_file_indices = set(
        get_group_index_from_fname(fname) for fname in ignore_files
    )
    return set(file_indices).difference(ignore_file_indices)


def get_file_indices_from_env() -> Set[int]:
    file_indices = os.getenv("FILE_INDICES")
    if isinstance(file_indices, str):
        file_indices = literal_eval(file_indices)
    file_indices = [int(idx) for idx in file_indices]
    return remove_existing(file_indices)


def main(args):
    if args.use_env_file_indices is True:
        file_indices = get_file_indices_from_env()
    else:
        min_idx = args.min_idx
        if min_idx is None:
            min_idx = os.getenv("MIN_IDX")
        max_idx = args.max_idx
        if max_idx is None:
            max_idx = os.getenv("MAX_IDX")
        if min_idx is None or max_idx is None:
            raise ValueError(
                f"Invalid value for min_idx and/or max_idx (min_idx=={min_idx} max_idx=={max_idx}"
            )
        file_indices = remove_existing(set(range(min_idx, max_idx)))

    input_dir = Path("/scierc")
    if not input_dir.exists():
        logger.debug(f"creating directory: {input_dir}")
        os.mkdir(input_dir)
    input_files_to_move = [
        fp
        for fp in Path("/data").rglob("*plmarker*.json")
        if get_group_index_from_fname(fp.name) in file_indices
    ]
    # move files to the input directory
    input_files: List[Path] = []
    for input_file in input_files_to_move:
        dst = input_dir.joinpath(input_file.name)
        logger.debug(f"copying file {input_file} to {dst}")
        shutil.copyfile(input_file, dst)
        input_files.append(dst)

    logdir = Path("/output/logs")
    if not logdir.exists():
        logger.debug(f"creating directory: {logdir}")
        os.mkdir(logdir)
    if args.gpu is True:
        processes = 1
    else:
        processes = args.processes
        if processes is None:
            processes = cpu_count()
    subprocess_args = []
    for fpath in input_files:
        file_idx_str = f"{get_group_index_from_fname(fpath.name):06d}"
        logfp = logdir.joinpath(f"run_acener_modified_{file_idx_str}.log")
        subprocess_args.append(
            (str(fpath), logfp, PATH_TO_SCRIPT, args.gpu, args.batch)
        )
    logger.debug(
        f"starting pool with {len(subprocess_args)} processes, running {processes} processes at a time"
    )
    with Pool(processes=processes) as pool:
        pool.starmap(run_command, subprocess_args)


if __name__ == "__main__":
    total_start = timer()
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(name)s.%(lineno)d %(levelname)s : %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    logger.info(" ".join(sys.argv))
    logger.info("{:%Y-%m-%d %H:%M:%S}".format(datetime.now()))
    logger.info("pid: {}".format(os.getpid()))
    import argparse

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--min-idx",
        type=int,
        default=None,
        help="min file index. if not specified will attempt to get from environment variable MIN_IDX",
    )
    parser.add_argument(
        "--max-idx",
        type=int,
        default=None,
        help="max file index (not included). if not specified will attempt to get from environment variable MAX_IDX",
    )
    parser.add_argument(
        "-e",
        "--use-env-file-indices",
        action="store_true",
        help="ignore min-idx and max-idx and instead use the list of file indices from the environment variable FILE_INDICES",
    )
    parser.add_argument(
        "-p",
        "--processes",
        type=int,
        default=None,
        help="number of cpu processes (default, number of available cpus). If --gpu is true, this will be ignored, and only one process will be run at a time",
    )
    parser.add_argument(
        "--gpu", action="store_true", help="run on gpu instead of cpu(s)"
    )
    parser.add_argument("--batch", type=int, default=60, help="batch size (default: 60")
    parser.add_argument("--debug", action="store_true", help="output debugging info")
    global args
    args = parser.parse_args()
    if args.debug:
        root_logger.setLevel(logging.DEBUG)
        logger.debug("debug mode is on")
    main(args)
    total_end = timer()
    logger.info(
        "all finished. total time: {}".format(format_timespan(total_end - total_start))
    )
