# 2022-09-16T07:54:18.544341524Z 07:54:18 __main__.42 INFO : running command: ['python', '/stage/run_acener_modified.py', '--model_type', 'bertspanmarker', '--model_name_or_path', '../models/sciner-scibert', '--do_lower_case', '--data_dir', '/net/s3/s2-research/jasonp/data2022/bridger/scierc/', '--learning_rate', '2e-5', '--num_train_epochs', '50', '--per_gpu_train_batch_size', '8', '--per_gpu_eval_batch_size', '60', '--gradient_accumulation_steps', '1', '--max_seq_length', '256', '--max_mention_ori_length', '8', '--do_eval', '--fp16', '--seed', '42', '--onedropout', '--lminit', '--train_file', 'train.json', '--dev_file', 'dev.json', '--test_file', '/scierc/titles_abstracts_plmarker_scierc_000689.json', '--output_dir', '/output', '--output_results']



python3 /stage/run_acener_modified.py --model_type bertspanmarker --model_name_or_path ../models/sciner-scibert --do_lower_case --data_dir /net/s3/s2-research/jasonp/data2022/bridger/scierc/ --learning_rate 2e-5 --num_train_epochs 50 --per_gpu_train_batch_size 8 --per_gpu_eval_batch_size 60 --gradient_accumulation_steps 1 --max_seq_length 256 --max_mention_ori_length 8 --do_eval --fp16 --seed 42 --onedropout --lminit --train_file train.json --dev_file dev.json --test_file /scierc/titles_abstracts_plmarker_scierc_000503.json --output_dir /output --output_results



beaker dataset fetch jasonp/sciner-scibert-model -o /models/sciner-scibert/

mkdir /scierc

cp /net/s3/s2-research/jasonp/data2022/bridger/scierc/titles_abstracts_plmarker_scierc_000501.json /scierc

cd /stage

/opt/miniconda3/bin/python3 /stage/run_acener_modified.py --model_type bertspanmarker --model_name_or_path ../models/sciner-scibert --do_lower_case --data_dir /net/s3/s2-research/jasonp/data2022/bridger/scierc/ --learning_rate 2e-5 --num_train_epochs 50 --per_gpu_train_batch_size 8 --per_gpu_eval_batch_size 60 --gradient_accumulation_steps 1 --max_seq_length 256 --max_mention_ori_length 8 --do_eval --fp16 --seed 42 --onedropout --lminit --train_file train.json --dev_file dev.json --test_file /scierc/titles_abstracts_plmarker_scierc_000501.json --output_dir /output --output_results

split -l 500 --numeric-suffixes titles_abstracts_plmarker_scierc_000501.json titles_abstracts_plmarker_scierc_000501.json