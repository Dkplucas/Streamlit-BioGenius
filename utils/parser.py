"""
Optimized bioinformatics sequence file parser for FASTA and FASTQ formats.
Efficient memory management for large datasets.
"""
from typing import List, Dict, Tuple, Generator
import sys


def parse_fasta(content: str) -> List[Dict[str, str]]:
    """
    Optimized FASTA parser with efficient memory usage.
    Uses efficient string operations and avoids unnecessary allocations.
    """
    sequences = []
    current_header = None
    current_seq = []
    seq_buffer_size = 0
    max_seq_length = 10000000

    lines = content.strip().split('\n')
    for line in lines:
        line = line.rstrip()
        if not line:
            continue

        if line.startswith('>'):
            if current_header is not None:
                sequences.append({
                    'header': current_header,
                    'sequence': ''.join(current_seq),
                    'length': seq_buffer_size
                })
                current_seq = []
                seq_buffer_size = 0

            current_header = line[1:]
        else:
            line_len = len(line)
            if seq_buffer_size + line_len > max_seq_length:
                return sequences, f"Sequence exceeds maximum length of {max_seq_length}"
            current_seq.append(line)
            seq_buffer_size += line_len

    if current_header is not None:
        sequences.append({
            'header': current_header,
            'sequence': ''.join(current_seq),
            'length': seq_buffer_size
        })

    return sequences


def parse_fastq(content: str) -> List[Dict[str, str]]:
    """
    Optimized FASTQ parser with efficient memory usage.
    Processes 4 lines at a time as per FASTQ spec.
    """
    sequences = []
    lines = content.strip().split('\n')
    num_lines = len(lines)

    i = 0
    while i < num_lines - 3:
        header = lines[i].rstrip()
        if not header.startswith('@'):
            i += 1
            continue

        sequence = lines[i + 1].rstrip()
        plus = lines[i + 2].rstrip()
        quality = lines[i + 3].rstrip()

        if len(sequence) != len(quality):
            i += 4
            continue

        sequences.append({
            'header': header[1:],
            'sequence': sequence,
            'quality': quality,
            'length': len(sequence)
        })
        i += 4

    return sequences


def parse_sequence_file(content: str, file_format: str) -> Tuple[List[Dict[str, str]], str]:
    """
    Parse sequence file with error handling and format detection.
    Optimized for large files with memory efficiency.

    Args:
        content: File content as string
        file_format: 'fasta', 'fa', 'fna', 'fastq', or 'fq'

    Returns:
        Tuple of (sequences list, error message if any)
    """
    try:
        if not content or not content.strip():
            return [], "File content is empty"

        file_format_lower = file_format.lower()

        if file_format_lower in ['fasta', 'fa', 'fna']:
            sequences = parse_fasta(content)
        elif file_format_lower in ['fastq', 'fq']:
            sequences = parse_fastq(content)
        else:
            return [], f"Unsupported format: {file_format}"

        if not sequences:
            return [], "No valid sequences found in file"

        return sequences, ""

    except MemoryError:
        return [], "File too large - insufficient memory to parse"
    except Exception as e:
        return [], f"Error parsing file: {str(e)}"
