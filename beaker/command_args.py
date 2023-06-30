# These are the arguments to pass to run_acener_modified.py

from typing import List


def get_arguments(input_file: str, batch_size=60) -> List[str]:
    return [
        "--model_type",
        "bertspanmarker",
        "--model_name_or_path",
        "../models/sciner-scibert",
        "--do_lower_case",
        "--data_dir",
        "/net/s3/s2-research/jasonp/data2022/bridger/scierc/",
        "--learning_rate",
        "2e-5",
        "--num_train_epochs",
        "50",
        "--per_gpu_train_batch_size",
        "8",
        "--per_gpu_eval_batch_size",
        str(batch_size),
        "--gradient_accumulation_steps",
        "1",
        "--max_seq_length",
        "256",
        "--max_mention_ori_length",
        "8",
        "--do_eval",
        "--fp16",
        "--seed",
        "42",
        "--onedropout",
        "--lminit",
        "--train_file",
        "train.json",
        "--dev_file",
        "dev.json",
        "--test_file",
        # "/scierc/test_titles_abstracts_plmarker_scierc_004974.json",
        input_file,
        "--output_dir",
        "/output",
        "--output_results",
    ]