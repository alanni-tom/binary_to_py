#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/9/9 13:16
# @Author  : Alanni
import os
import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def decompile_pyc(pyc_path, output_dir, input_dir):
    rel_path = os.path.relpath(os.path.dirname(pyc_path), input_dir)
    target_dir = os.path.join(output_dir, rel_path)
    os.makedirs(target_dir, exist_ok=True)

    subprocess.run([
        "uncompyle6",
        "-o", target_dir,
        pyc_path
    ])

    logger.info(f"[*] Decompilation completed: {pyc_path} -> {target_dir}")

def pyc_to_py(input_dir, output_dir, max_workers=4):
    os.makedirs(output_dir, exist_ok=True)
    pyc_files = []

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".pyc"):
                pyc_files.append(os.path.join(root, file))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(decompile_pyc, f, output_dir, input_dir) for f in pyc_files]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"[!] Error decompiling: {e}")

    try:
        os.rmdir(input_dir)
        logger.info(f"[!] Cache directory {input_dir} deleted!")
    except OSError as e:
        logger.warning(f"[!] Failed to delete {input_dir}: {e}")

