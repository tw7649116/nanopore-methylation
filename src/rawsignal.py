#! /usr/bin/env python
"""
__author__ = Yao LI
__email__ = yao.li.binf@gmail.com
__date__ = 07/02/2018
"""
import os
import numpy as np
from src.handlefiles import get_id, get_raw_segment, search_fastq


def get_raw_dirc(directory, savepath, ir_pos, fastqpath="/shares/coin/yao.li/data/fastq/", basecall_group='Basecall_1D_001'):
    """
    :param directory: (string) the folder of fast5 files
    :param savepath: (string) path of output numpy files
    :param ir_pos: (dictionary) a NanoporeReads overlap dict
    :param fastqpath: (string) path of fastq files
    :param basecall_group
    :return: (dict)
    """
    raw_signal = {}
    for fst5 in os.listdir(directory):
        try:
            if fst5.endswith(".fast5"):
                #sid = getID(directory+fst5)
                sid = get_id(search_fastq(fst5, fastqpath))
                if sid in ir_pos:
                    poses = ir_pos[sid][2]
                    raw, fastq = get_raw_segment(directory+fst5, poses[0], poses[1], basecall_group)
                    raw_signal[sid] = (raw, fastq)
                    np.save(savepath + fst5.replace(".fast5", ".npy"), (raw, fastq))
        except StopIteration:
            np.save(savepath + fst5.replace(".fast5", ".npy"), (raw, fastq))
            continue
    return raw_signal


def find_haplotype(raw_signals, haplotypes):
    """For each raw_signal array, decide its haplotype."""
    h1 = []
    h2 = []
    for signal_id in raw_signals:
        h1.append(raw_signals[signal_id])
    return h1, h2


#if __name__ == "__main__":
    #raw_signals = get_raw_segment("fast5/", "../data/raw_signals/", ir_pos)  # I probably don't have ir_pos any more, damn it
