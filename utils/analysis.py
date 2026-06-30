"""
Optimized bioinformatics sequence analysis utilities.
Efficient computation for large-scale sequence analysis.
"""
from typing import Dict, Any, List
from collections import Counter


def calculate_gc_content(sequence: str) -> float:
    """
    Optimized GC content calculation using fast iteration.
    Formula: (G + C) / Total * 100
    """
    if not sequence:
        return 0.0

    seq_upper = sequence.upper()
    gc_count = sum(1 for base in seq_upper if base in 'GC')
    gc_content = (gc_count / len(seq_upper)) * 100

    return round(gc_content, 2)


def calculate_nucleotide_composition(sequence: str) -> Dict[str, int]:
    """
    Optimized nucleotide counting using Counter.
    More efficient than multiple .count() calls.
    """
    seq_upper = sequence.upper()
    counter = Counter(seq_upper)

    return {
        'A': counter.get('A', 0),
        'T': counter.get('T', 0),
        'G': counter.get('G', 0),
        'C': counter.get('C', 0),
        'N': counter.get('N', 0),
        'Other': len(seq_upper) - sum(counter.get(base, 0) for base in 'ATGCN')
    }


def analyze_sequence(sequence: str, header: str = "") -> Dict[str, Any]:
    """
    Comprehensive sequence analysis with optimized memory usage.
    Processes sequence once to extract all metrics.
    """
    if not sequence:
        return {'header': header, 'length': 0, 'gc_content': 0, 'at_content': 0}

    length = len(sequence)
    nucleotide_counts = calculate_nucleotide_composition(sequence)
    gc_content = calculate_gc_content(sequence)
    at_content = 100 - gc_content

    return {
        'header': header,
        'length': length,
        'gc_content': gc_content,
        'at_content': round(at_content, 2),
        'nucleotide_counts': nucleotide_counts,
        'a_percent': round((nucleotide_counts['A'] / length * 100) if length > 0 else 0, 2),
        't_percent': round((nucleotide_counts['T'] / length * 100) if length > 0 else 0, 2),
        'g_percent': round((nucleotide_counts['G'] / length * 100) if length > 0 else 0, 2),
        'c_percent': round((nucleotide_counts['C'] / length * 100) if length > 0 else 0, 2),
    }


def analyze_multiple_sequences(sequences: List[Dict[str, str]], limit: int = 10000) -> Dict[str, Any]:
    """
    Optimized analysis for multiple sequences with optional limit.
    Provides summary statistics and individual sequence data.
    """
    if not sequences:
        return {
            'total_sequences': 0,
            'total_length': 0,
            'average_length': 0,
            'average_gc_content': 0,
            'sequences': [],
            'truncated': False
        }

    truncated = False
    seq_list = sequences

    if len(sequences) > limit:
        seq_list = sequences[:limit]
        truncated = True

    analyses = [
        analyze_sequence(seq['sequence'], seq.get('header', ''))
        for seq in seq_list
    ]

    if not analyses:
        return {
            'total_sequences': len(sequences),
            'total_length': 0,
            'average_length': 0,
            'average_gc_content': 0,
            'sequences': [],
            'truncated': truncated
        }

    total_length = sum(a['length'] for a in analyses)
    average_length = total_length / len(analyses)
    average_gc = sum(a['gc_content'] for a in analyses) / len(analyses)

    return {
        'total_sequences': len(sequences),
        'total_length': total_length,
        'average_length': round(average_length, 2),
        'average_gc_content': round(average_gc, 2),
        'sequences': analyses,
        'truncated': truncated,
        'note': f"Showing {len(analyses)} of {len(sequences)} sequences" if truncated else None
    }


def detect_open_reading_frames(sequence: str, min_length: int = 30, max_orfs: int = 1000) -> List[Dict[str, Any]]:
    """
    Optimized ORF detection with frame-based search.
    Limits results to prevent memory issues with large sequences.
    """
    if not sequence or len(sequence) < min_length:
        return []

    sequence = sequence.upper()
    orfs = []
    start_codon = 'ATG'
    stop_codons = {'TAA', 'TAG', 'TGA'}

    seq_len = len(sequence)

    for frame in range(3):
        i = frame
        while i < seq_len - 5:
            if sequence[i:i+3] == start_codon:
                start_pos = i

                for j in range(i + 3, seq_len - 2, 3):
                    if sequence[j:j+3] in stop_codons:
                        orf_length = j + 3 - start_pos

                        if orf_length >= min_length:
                            orfs.append({
                                'start': start_pos,
                                'end': j + 3,
                                'length': orf_length,
                                'sequence': sequence[start_pos:j+3] if len(orfs) < max_orfs else None
                            })

                            if len(orfs) >= max_orfs:
                                return orfs
                        break
            i += 1

    return orfs[:max_orfs]
