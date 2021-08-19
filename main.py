#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from project import *


def main():
    
    args = initialize()

    if hasattr(args, 'file'):
        args.dir = os.path.dirname(args.file) + '/'
        seq = read_fasta(args.file)
        _ = seq_analysis(args, seq)
        
    elif hasattr(args, 'dir'):
        data_cds, data_intergenic = read_dir_database(args.dir, args.min_length_seq)
        print(len(data_cds),len(data_intergenic))
        _ = database_analysis(args, data_cds)
        _ = database_analysis(args, data_intergenic)
        _ = write_summarized_results_database(args.dir)
    
    elif hasattr(args, 'dir_statistics'):
        statistics(args)


if __name__ == "__main__":
    main()
