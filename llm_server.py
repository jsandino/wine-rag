#!/usr/bin/env python
#pylint: disable-all-docstring
'''
A script to download and run a Large Language Model packaged as a stand-alone llamafile.
'''

import os
import stat
import subprocess
from pathlib import Path
import urllib.request

TINY_LLAMA = "TinyLlama-1.1B-Chat-v1.0.F16.llamafile"
MXBAI_EMBED = "mxbai-embed-large-v1-f16.llamafile"

model_locations = {
    TINY_LLAMA: "https://huggingface.co/Mozilla/TinyLlama-1.1B-Chat-v1.0-llamafile/resolve/main/TinyLlama-1.1B-Chat-v1.0.F16.llamafile",
    MXBAI_EMBED: "https://huggingface.co/Mozilla/mxbai-embed-large-v1-llamafile/resolve/main/mxbai-embed-large-v1-f16.llamafile",
}


def main(model):
    llm_path = download_llm(model)
    launch_server(llm_path)


def download_llm(model):
    llm_path = Path(f"llm/{model}")
    if not llm_path.is_file():
        print(f"Downloading LLM: {model}")
        Path("llm").mkdir(parents=True, exist_ok=True)
        url = model_locations[model]
        urllib.request.urlretrieve(url, llm_path)
    return llm_path


def launch_server(llm_path):
    ensure_llm_executable(llm_path)
    llm_cmd = str(Path(llm_path).absolute())
    p = subprocess.Popen(["sh", llm_cmd])
    p.communicate()


def ensure_llm_executable(llm):
    os.chmod(llm, 0o755)


if __name__ == "__main__":
    # main(MXBAI_EMBED)
    main(TINY_LLAMA)
