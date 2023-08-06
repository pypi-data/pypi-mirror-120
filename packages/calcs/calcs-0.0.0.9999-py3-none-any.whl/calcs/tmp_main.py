###############################################################################
# Import modules
###############################################################################

# buidin modules
from time import time as tt  # ?-------------------===
import sys
from concurrent.futures import ProcessPoolExecutor
from itertools import compress
from itertools import chain

# custom modules
import parse
import load
import trim
import annotate
import call_cstag
import convert

###############################################################################
# MAIN
###############################################################################

# ARGS_QUERY = open("../tests/data/subindel/subindel.sam") # ?-------------------
# ARGS_REFERENCE = "../tests/data/random_100bp.fa" # ?-------------------


def main():
    # Argument parse
    ARGS_QUERY, ARGS_REFERENCE, ARGS_LONG, ARGS_PAF, ARGS_THREADS = parse.parse_args()

    # Parse Query SAM file
    t = tt()  # ?-------------------
    QUESAM = tuple(load.sam(ARGS_QUERY))
    readsam_time = tt() - t  # ?-------------------
    print(f"Read Query: {readsam_time:.3} sec",
          file=sys.stderr)  # ?-------------------

    t = tt()  # ?-------------------
    is_header = [_.startswith("@") for _ in QUESAM]
    HEADER = tuple(list(compress(QUESAM, is_header)))
    IS_MINIMAP2 = any(["minimap2" in _ for _ in HEADER])

    is_alignment = [not _ for _ in is_header]
    alignments = tuple(list(compress(QUESAM, is_alignment)))
    is_mapped = ["*" != s.split("\t")[5] for s in alignments]
    is_unmapped = [not _ for _ in is_mapped]

    ALIGNMENTS_MAPPED = tuple(list(compress(alignments, is_mapped)))
    ALIGNMENTS_UNMAPPED = tuple(list(compress(alignments, is_unmapped)))

    RNAMES = tuple([s.split("\t")[2] for s in ALIGNMENTS_MAPPED])
    STARTS = tuple([int(s.split("\t")[3]) - 1 for s in ALIGNMENTS_MAPPED])
    CIGARS = tuple([s.split("\t")[5] for s in ALIGNMENTS_MAPPED])
    QUESEQS = tuple([s.split("\t")[9].upper() for s in ALIGNMENTS_MAPPED])
    CHUNKSIZE = int(len(QUESEQS)/ARGS_THREADS)

    print(f"Parse sam: {tt() - t:.3} sec",
          file=sys.stderr)  # ?-------------------

    # Trim soft clip into query sequence
    t = tt()  # ?--------------------------------------
    # LEN_CLIPS = list(map(trim.get_softclip_lengths, CIGARS))
    with ProcessPoolExecutor(max_workers=ARGS_THREADS) as executor:
        LEN_CLIPS = list(executor.map(
            trim.get_softclip_lengths, CIGARS,
            chunksize=CHUNKSIZE)
        )

    # QUESEQS_TRIMMED = map(trim.softclips, QUESEQS, LEN_CLIPS)
    with ProcessPoolExecutor(max_workers=ARGS_THREADS) as executor:
        QUESEQS_TRIMMED = executor.map(
            trim.softclips, QUESEQS, LEN_CLIPS,
            chunksize=CHUNKSIZE
        )

    print(f"Trim softclips: {tt() - t:.3} sec",
          file=sys.stderr)  # ?-------------------

    # Parse Reference FASTA file
    dict_fasta = load.fasta(ARGS_REFERENCE)
    REFSEQS = (dict_fasta[rname] for rname in RNAMES)
    REFLENS = (len(dict_fasta[rname]) for rname in RNAMES)

    # Trim start sites in reference sequence
    t = tt()  # ?-------------------
    # REFSEQS_TRIMMED = map(trim.unmapped_region, REFSEQS, STARTS, CIGARS)
    with ProcessPoolExecutor(max_workers=ARGS_THREADS) as executor:
        REFSEQS_TRIMMED = executor.map(
            trim.unmapped_region, REFSEQS, STARTS, CIGARS,
            chunksize=CHUNKSIZE
        )
    print(f"Trim unmapped region: {tt() - t:.3} sec",
          file=sys.stderr)  # ?-------------------

    # Annotate Insertion in reference sequence
    t = tt()  # ?-------------------
    # REFSEQS_ANNO = map(annotate.insertion, REFSEQS_TRIMMED, CIGARS)
    with ProcessPoolExecutor(max_workers=ARGS_THREADS) as executor:
        REFSEQS_ANNO = list(
            executor.map(
                annotate.insertion, REFSEQS_TRIMMED, CIGARS,
                chunksize=CHUNKSIZE)
        )
    print(f"Annotate Insertion: {tt() - t:.3} sec",
          file=sys.stderr)  # ?-------------------

    # Annotate Deletion into query seuqence
    t = tt()  # ?-------------------
    # QUESEQS_ANNO = map(annotate.deletion, QUESEQS_TRIMMED, CIGARS)
    with ProcessPoolExecutor(max_workers=ARGS_THREADS) as executor:
        QUESEQS_ANNO = executor.map(
            annotate.deletion, QUESEQS_TRIMMED, CIGARS,
            chunksize=CHUNKSIZE)
    print(f"Annotate Deletion: {tt() - t:.3} sec",
          file=sys.stderr)  # ?-------------------

    # Calculate CS tags
    t = tt()  # ?-------------------
    # cstags = map(call_cstag.long_form, REFSEQS_ANNO, QUESEQS_ANNO)
    with ProcessPoolExecutor(max_workers=ARGS_THREADS) as executor:
        cstags = executor.map(
            call_cstag.long_form, REFSEQS_ANNO, QUESEQS_ANNO,
            chunksize=CHUNKSIZE)
    print(f"Call CSlong: {tt() - t:.3} sec",
          file=sys.stderr)  # ?-------------------

    if ARGS_LONG:
        CSTAGS = cstags
    else:
        t = tt()  # ?-------------------
        # CSTAGS = map(call_cstag.short_form, cstags)
        with ProcessPoolExecutor(max_workers=ARGS_THREADS) as executor:
            CSTAGS = executor.map(
                call_cstag.short_form, cstags,
                chunksize=CHUNKSIZE
            )
        # CSTAGS = tuple(_)
        print(f"Call CSshort: {tt() - t:.3} sec",
              file=sys.stderr)  # ?-------------------

    # Output PAF or SAM
    if ARGS_PAF:
        t = tt()  # ?-------------------
        with ProcessPoolExecutor(max_workers=ARGS_THREADS) as executor:
            paf_cstags = list(
                executor.map(
                    convert.to_paf,
                    ALIGNMENTS_MAPPED, CSTAGS, LEN_CLIPS,
                    STARTS, REFLENS, REFSEQS_ANNO,
                    chunksize=CHUNKSIZE
                )
            )
        print(f"Convert to PAF: {tt() - t:.3} sec",
              file=sys.stderr)  # ?-------------------
        try:
            sys.stdout.write('\n'.join(paf_cstags + [""]))
        except (BrokenPipeError, IOError):
            pass
    else:
        t = tt()  # ?-------------------
        # ALIGNMENT_CSTAGS = map(
        #     convert.insert_cstag,
        #     ALIGNMENTS_MAPPED,
        #     CSTAGS,
        #     [IS_MINIMAP2] * len(ALIGNMENTS_MAPPED)
        # )
        with ProcessPoolExecutor(max_workers=ARGS_THREADS) as executor:
            ALIGNMENT_CSTAGS = executor.map(
                convert.insert_cstag,
                ALIGNMENTS_MAPPED,
                CSTAGS,
                [IS_MINIMAP2] * len(ALIGNMENTS_MAPPED),
                chunksize=CHUNKSIZE)

        print(f"Insert CStag: {tt() - t:.3} sec",
              file=sys.stderr)  # ?-------------------

        # SAM_CSTAGS = HEADER + \
        #     tuple(ALIGNMENT_CSTAGS) + \
        #     tuple(ALIGNMENTS_UNMAPPED)
        t = tt()  # ?-------------------
        SAM_CSTAGS = chain(HEADER, ALIGNMENT_CSTAGS, ALIGNMENTS_UNMAPPED)
        print(f"chain: {tt() - t:.3} sec",
              file=sys.stderr)  # ?-------------------
        try:
            t = tt()  # ?-------------------

            # def write(sam_cstag):
            #     sys.stdout.write('\n'.join(map(str, sam_cstag)))

            # with ThreadPoolExecutor(max_workers=ARGS_THREADS) as executor:
            #     executor.map(write, SAM_CSTAGS,
            #                  chunksize=CHUNKSIZE)
            sys.stdout.write('\n'.join(map(str, SAM_CSTAGS)))
            print(f"stdout: {tt() - t:.3} sec",
                  file=sys.stderr)  # ?-------------------
            # sys.stdout.write('\n'.join(SAM_CSTAGS + ("",)))
        except (BrokenPipeError, IOError):
            pass


###############################################################################
# Call MAIN
###############################################################################

if __name__ == "__main__":
    main()
