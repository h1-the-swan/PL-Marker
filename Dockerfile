FROM ghcr.io/allenai/cuda:11.3-cudnn8-dev-ubuntu20.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# This is the directory that files will be copied into.
# It's also the directory that you'll start in if you connect to the image.
WORKDIR /stage/

# Update new packages
RUN apt-get update

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy the `requirements.txt` to `/stage/requirements.txt/` and then install them.
# We do this first because it's slow and each of these commands are cached in sequence.
COPY requirement.txt .
RUN pip install -r requirement.txt
COPY transformers ./transformers/
RUN pip install --editable ./transformers

RUN mkdir /models
# COPY models/sciner-scibert /models/sciner-scibert/
COPY run_acener_modified.py .
COPY beaker/entrypoint.py .
COPY beaker/command_args.py .
COPY beaker/update_papers_script.py .
RUN mkdir /output
