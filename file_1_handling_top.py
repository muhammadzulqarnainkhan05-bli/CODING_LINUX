"""
================================================================================
                        PYTHON FILE HANDLING: THE COMPLETE BOOK
        From 10th-Grade Fundamentals to Intermediate & PhD-Level Systems
================================================================================

HOW TO READ THIS BOOK:
- Save this file as: python_file_handling_book.py
- Run it directly:   python3 python_file_handling_book.py
- Every chapter explains:
    1. Core Concept (Theory + Real-World Analogy)
    2. Executable Code Lab
    3. Pitfalls / Edge Cases (Where bugs actually happen)

TABLE OF CONTENTS:
  CHAPTER 1:  What Is a File, Stream, and File Descriptor? (Foundations)
  CHAPTER 2:  Opening & Closing Files Safely (open, close, context managers)
  CHAPTER 3:  File Modes & Pointer Arithmetic (r, w, a, x, +, b, seek, tell)
  CHAPTER 4:  Reading & Writing Strategies (Buffers, chunks, large files)
  CHAPTER 5:  Defensive Programming & Exceptions (OS errors, permissions, locks)
  CHAPTER 6:  Structured Text Formats (CSV, JSON, and schema validation)
  CHAPTER 7:  Binary Data, Structs & Serialization (bytes, struct, pickle)
  CHAPTER 8:  Filesystem Navigation & Pathlib (Path, atomic writes, tempfiles)
  CHAPTER 9:  Low-Level I/O, Buffering & Concurrency (io module, mmap, locking)
  CHAPTER 10: PhD / Research Capstone Lab (Streaming log analyzer + checkpointing)

================================================================================
"""

from __future__ import annotations

import csv
import json
import mmap
import os
import pickle
import shutil
import struct
import tempfile
import time
from pathlib import Path
from typing import Any, Iterator

# Base sandbox directory so all book experiments stay organized and clean
BOOK_DIR = Path("file_handling_book_lab")


def banner(chapter_num: int, title: str, level: str) -> None:
    print("\n" + "=" * 80)
    print(f"CHAPTER {chapter_num}: {title}")
    print(f"Level: {level}")
    print("=" * 80)


# ==============================================================================
# CHAPTER 1: WHAT IS A FILE, STREAM, AND FILE DESCRIPTOR?
# Level: 10th Grade / Beginner
# ==============================================================================
# THEORY:
# RAM (memory) is temporary (volatile): when your program stops or power goes
# out, variables disappear. A file is a named sequence of bytes stored on
# persistent storage (SSD, HDD, SD card) so data survives after exit.
#
# Think of a file on disk like a book in a locked cabinet, and a file object in
# Python like a bookmark + reading glasses at your desk. You don't carry the
# whole library in your head; you open one book, read/write through a stream,
# and put it back properly.
#
# Under the hood on operating systems (Linux/macOS/Windows), an open file is
# tracked by an integer handle called a File Descriptor (fd).
#
# PITFALL:
# Confusing a file *path* (string/Path pointing to a location) with a *file
# object / stream* (active connection used to read/write bytes).

def chapter_1_foundations() -> None:
    banner(1, "Files, Streams & File Descriptors", "10th Grade / Beginner")
    BOOK_DIR.mkdir(exist_ok=True)

    sample_path = BOOK_DIR / "ch1_hello.txt"
    stream = open(sample_path, "w", encoding="utf-8")
    print("File path object :", sample_path)
    print("Python stream type:", type(stream))
    print("OS File Descriptor:", stream.fileno())
    stream.write("Assalam-o-Alaikum! Persistent data lives beyond RAM.\n")
    stream.close()
    print("Is stream closed? :", stream.closed)


# ==============================================================================
# CHAPTER 2: OPENING & CLOSING FILES SAFELY
# Level: 10th Grade / Intermediate
# ==============================================================================
# THEORY:
# Every open file consumes OS resources (file descriptors, buffers, sometimes
# locks). If you forget `f.close()` and an exception happens midway, resources
# leak.
#
# Python's `with` statement uses the Context Manager protocol (`__enter__` and
# `__exit__`) to guarantee `.close()` runs automatically when leaving the block,
# even if an error is raised inside the block.
#
# PITFALL:
# Always specify `encoding="utf-8"` for text files. Relying on system default
# encoding causes subtle bugs across machines, locales, and platforms.

def chapter_2_context_managers() -> None:
    banner(2, "Safe Resource Lifecycle with Context Managers", "10th Grade / Intermediate")
    notes_path = BOOK_DIR / "ch2_notes.txt"

    # Preferred pattern: automatic deterministic cleanup
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write("Chapter 2: 'with' guarantees closing even on errors.\n")
        f.write("Always pass encoding='utf-8' for predictable text I/O.\n")

    print("Wrote:", notes_path)
    print("Closed automatically after 'with' block:", True)


# ==============================================================================
# CHAPTER 3: FILE MODES & POINTER ARITHMETIC (seek / tell)
# Level: Intermediate (FSc / BSCS)
# ==============================================================================
# THEORY:
# File modes control:
#   - Access direction: read ('r'), write ('w'), append ('a'), exclusive ('x')
#   - Update capability: '+' allows both read and write on the same stream
#   - Data representation: text mode (default, translates newlines '\n') vs
#     binary mode ('b', raw bytes without newline translation)
#
# A file stream maintains a byte offset (file pointer / cursor):
#   - `f.tell()` returns current byte position from start of stream.
#   - `f.seek(offset, whence)` moves pointer:
#       * whence=0 (os.SEEK_SET): from beginning of file
#       * whence=1 (os.SEEK_CUR): from current position (in binary mode)
#       * whence=2 (os.SEEK_END): from end of file (in binary mode)
#
# PITFALL:
# 1. Opening with `'w'` truncates (erases) existing content immediately on open.
# 2. In text mode, `seek(offset, whence)` only safely supports `seek(0)` or
#    values returned by `f.tell()` — arbitrary byte offsets in UTF-8 can land
#    inside a multi-byte character!

def chapter_3_modes_and_pointers() -> None:
    banner(3, "File Modes & Pointer Arithmetic (tell / seek)", "Intermediate (FSc / BSCS)")
    ptr_file = BOOK_DIR / "ch3_pointer.txt"

    with open(ptr_file, "w", encoding="utf-8") as f:
        f.write("ABCDEFGH\n12345678\n")

    with open(ptr_file, "r", encoding="utf-8") as f:
        print("Initial offset:", f.tell())
        print("Read 4 chars  :", repr(f.read(4)))
        saved_pos = f.tell()
        print("Offset now    :", saved_pos)
        print("Rest of line  :", repr(f.readline()))

        # Jump back to saved character offset
        f.seek(saved_pos)
        print("After seek    :", repr(f.read(4)))

    # Exclusive mode ('x') prevents accidental overwrite
    try:
        with open(ptr_file, "x", encoding="utf-8") as f:
            f.write("Should not overwrite")
    except FileExistsError:
        print("Protected by 'x' mode: file already exists, overwrite blocked.")


# ==============================================================================
# CHAPTER 4: READING & WRITING STRATEGIES FOR LARGE FILES
# Level: Intermediate / Applied Engineering
# ==============================================================================
# THEORY:
# Calling `f.read()` loads the entire file into RAM at once. On a 5 GB log or
# dataset file on an 8 GB machine, `f.read()` can trigger Out-Of-Memory (OOM)
# crashes or heavy swapping.
#
# Better patterns:
#   - Iterating directly over `for line in f:` reads lazily line-by-line.
#   - `f.read(chunk_size)` reads fixed byte/char blocks for streaming pipelines.
#   - `f.writelines(iterable)` writes any iterable of strings (does NOT add '\n'
#     automatically—you must include '\n' in each item).
#
# PITFALL:
# `f.writelines(["a", "b"])` produces `"ab"`, NOT `"a\nb\n"`.

def chapter_4_streaming_io() -> None:
    banner(4, "Memory-Safe Reading & Writing Strategies", "Intermediate / Applied")
    log_path = BOOK_DIR / "ch4_events.log"

    lines = [f"2026-11-25T10:00:{i:02d}Z INFO event_{i}\n" for i in range(1, 11)]
    with open(log_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Stream line-by-line (O(1) memory with respect to line count)
    info_count = 0
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if "INFO" in line:
                info_count += 1

    print(f"Streamed {log_path.name}: found {info_count} INFO lines using O(1) line buffer.")


# ==============================================================================
# CHAPTER 5: DEFENSIVE PROGRAMMING & OS EXCEPTIONS
# Level: Intermediate / Production
# ==============================================================================
# THEORY:
# Real filesystems fail for reasons outside your code: missing files,
# permission denied, read-only mounts, disk full, broken symlinks, or encoding
# mismatches. Catch specific exceptions (`FileNotFoundError`, `PermissionError`,
# `UnicodeDecodeError`, or base `OSError`) rather than silently swallowing
# everything with bare `except:`.
#
# PITFALL:
# Catching `Exception` or bare `except:` hides bugs like `KeyboardInterrupt` or
# typos in variable names.

def chapter_5_exceptions() -> None:
    banner(5, "Defensive Error Handling & OS Exceptions", "Intermediate / Production")
    missing = BOOK_DIR / "does_not_exist.txt"

    try:
        content = missing.read_text(encoding="utf-8")
        print(content)
    except FileNotFoundError as exc:
        print(f"Handled missing file cleanly: {exc.filename} (errno={exc.errno})")
    except PermissionError as exc:
        print(f"Permission denied accessing {exc.filename}")
    except UnicodeDecodeError as exc:
        print(f"Encoding mismatch at byte {exc.start}: {exc.reason}")
    except OSError as exc:
        print(f"General OS I/O failure: {exc}")


# ==============================================================================
# CHAPTER 6: STRUCTURED DATA — CSV & JSON
# Level: Intermediate / Data & Web Engineering
# ==============================================================================
# THEORY:
# Raw text files require custom parsing rules. Structured formats standardize
# serialization:
#   - CSV (Comma-Separated Values): Tabular rows/columns. Always pass
#     `newline=""` when opening with `csv.writer` or `csv.DictWriter` so
#     Python's CSV module handles line endings cleanly across OSes.
#   - JSON (JavaScript Object Notation): Hierarchical key-value data (dicts,
#     lists, strings, numbers, booleans, null). Use `json.dump`/`json.load`
#     for files, and `json.dumps`/`json.loads` for strings.
#
# PITFALL:
# CSV values are read back as strings (`"95"`, not `95`) unless explicitly
# cast (`int`, `float`). JSON does not natively serialize arbitrary Python sets
# or custom class instances without a custom encoder or conversion.

def chapter_6_csv_and_json() -> None:
    banner(6, "Structured Data: CSV & JSON", "Intermediate / Data & Web")

    csv_path = BOOK_DIR / "ch6_scores.csv"
    rows = [
        {"student": "Amina", "subject": "Physics", "score": 91},
        {"student": "Bilal", "subject": "Math", "score": 88},
        {"student": "Tariq", "subject": "CS", "score": 96},
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["student", "subject", "score"])
        writer.writeheader()
        writer.writerows(rows)

    scores: list[int] = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            scores.append(int(row["score"]))

    print("CSV parsed scores:", scores, "| Average:", sum(scores) / len(scores))

    json_path = BOOK_DIR / "ch6_experiment.json"
    payload = {
        "experiment": "thermal_conductivity_bench",
        "trials": 3,
        "passed": True,
        "metrics": {"mean_k": 1.42, "units": "W/(m*K)"},
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    with open(json_path, "r", encoding="utf-8") as f:
        reloaded = json.load(f)

    print("JSON reloaded experiment:", reloaded["experiment"], "| mean_k:", reloaded["metrics"]["mean_k"])


# ==============================================================================
# CHAPTER 7: BINARY DATA, PACKED STRUCTS & PICKLE
# Level: Advanced (Systems / ML / Research)
# ==============================================================================
# THEORY:
# Binary mode (`'rb'`, `'wb'`) deals directly with raw bytes (`bytes` /
# `bytearray`).
#   - `struct`: Packs/unpacks C-style binary headers or wire protocols with
#     explicit endianness (`<` little-endian, `>` big-endian) and types (`I`
#     uint32, `d` float64).
#   - `pickle`: Serializes Python object graphs (dicts, lists, custom objects,
#     model weights).
#
# PITFALL / SECURITY WARNING:
# NEVER unpickle (`pickle.load` / `pickle.loads`) data from untrusted or
# external sources—`pickle` can execute arbitrary code during deserialization.
# Use JSON or safe binary formats for untrusted inputs.

def chapter_7_binary_and_pickle() -> None:
    banner(7, "Binary Formats, struct & pickle", "Advanced (Systems / ML)")

    # 1. Fixed binary packet: magic header (4 bytes), record_id (uint32), value (float64)
    bin_path = BOOK_DIR / "ch7_packet.bin"
    packet_fmt = "<4sId"
    packed = struct.pack(packet_fmt, b"ZKB1", 4096, 3.1415926535)

    with open(bin_path, "wb") as f:
        f.write(packed)

    with open(bin_path, "rb") as f:
        magic, rec_id, val = struct.unpack(packet_fmt, f.read())

    print(f"Unpacked binary -> magic={magic}, id={rec_id}, val={val:.6f}")

    # 2. Trusted local checkpoint serialization via pickle
    pkl_path = BOOK_DIR / "ch7_state.pkl"
    state = {"epoch": 12, "loss": 0.0184, "weights_summary": [0.1, -0.2, 0.5]}

    with open(pkl_path, "wb") as f:
        pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)

    with open(pkl_path, "rb") as f:
        loaded_state = pickle.load(f)

    print("Loaded trusted pickle state:", loaded_state)


# ==============================================================================
# CHAPTER 8: PATHLIB, ATOMIC WRITES & TEMPORARY FILES
# Level: Advanced / Reliability Engineering
# ==============================================================================
# THEORY:
# `pathlib.Path` provides object-oriented, cross-platform filesystem paths.
#
# Atomic Write Pattern:
# If a program crashes while writing directly to `config.json`, you can end up
# with a half-written, corrupted file. Instead:
#   1. Write complete data to a temporary file in the same directory.
#   2. Call `os.fsync(tmp_file.fileno())` to flush OS buffers to disk.
#   3. Atomically replace the target via `os.replace(tmp_path, target_path)`.
#
# PITFALL:
# `os.replace()` across *different* filesystems/partitions can raise `EXDEV`
# ("Invalid cross-device link"). Keep temp files on the same filesystem/dir as
# the target path.

def atomic_write_text(target: Path, text: str, encoding: str = "utf-8") -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=str(target.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding=encoding) as tmp_file:
            tmp_file.write(text)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
        os.replace(tmp_path, target)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise


def chapter_8_pathlib_and_atomic_io() -> None:
    banner(8, "Pathlib, Tempfiles & Atomic Writes", "Advanced / Reliability")

    cfg_path = BOOK_DIR / "ch8_settings.conf"
    atomic_write_text(cfg_path, "mode=production\nretries=3\n")
    print("Atomically wrote:", cfg_path, "| exists:", cfg_path.exists())

    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=True) as scratch:
        scratch.write("Temporary scratch buffer data")
        scratch.seek(0)
        print("Read from auto-cleaned NamedTemporaryFile:", repr(scratch.read()))
    print("NamedTemporaryFile automatically removed on context exit.")


# ==============================================================================
# CHAPTER 9: LOW-LEVEL BUFFERING & MEMORY-MAPPED FILES (mmap)
# Level: PhD / High-Performance Systems
# ==============================================================================
# THEORY:
# Python's `io` stack layers:
#   RawIOBase (unbuffered OS read/write)
#     -> BufferedReader / BufferedWriter / BufferedRandom (block buffering)
#       -> TextIOWrapper (encoding + universal newlines)
#
# Memory-mapped files (`mmap`) map a file directly into the process's virtual
# address space so you can slice and search it like a `bytes` / `bytearray`
# object without copying everything through standard read buffers first.
#
# PITFALL:
# You cannot `mmap` an empty (0-byte) file on most OSes (`ValueError` /
# `OSError`). Also, resizing an underlying file while mapped can cause
# out-of-bounds faults (`SIGBUS` / `ValueError`).

def chapter_9_mmap_and_low_level() -> None:
    banner(9, "Low-Level Buffering & Memory-Mapped I/O (mmap)", "PhD / Systems")

    mmap_path = BOOK_DIR / "ch9_mapped.dat"
    with open(mmap_path, "wb") as f:
        f.write(b"HEADER:V1|PAYLOAD:ALPHA_BETA_GAMMA_OMEGA|END\n")

    with open(mmap_path, "r+b") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            idx = mm.find(b"GAMMA")
            print("Bytes in mmap region:", len(mm), "| 'GAMMA' found at byte offset:", idx)
            print("Slice around match   :", mm[max(0, idx - 6) : idx + 11])


# ==============================================================================
# CHAPTER 10: PHD / RESEARCH CAPSTONE — STREAMING LOG AGGREGATOR
# Level: PhD / Research Pipeline
# ==============================================================================
# SCENARIO:
# In scientific computing, simulations, or telemetry pipelines, you often process
# streams of measurements (`timestamp,category,value`) and summarize statistics
# reliably while keeping intermediate artifacts structured and inspectable.
#
# This capstone:
#   1. Generates a synthetic telemetry stream file.
#   2. Streams it line-by-line (never loading whole file into RAM).
#   3. Aggregates count, min, max, and mean per category.
#   4. Persists a clean JSON summary report atomically.

def stream_telemetry_stats(source_path: Path) -> dict[str, dict[str, float | int]]:
    stats: dict[str, dict[str, Any]] = {}

    with open(source_path, "r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) != 3:
                raise ValueError(f"Malformed record at line {line_no}: {line!r}")

            _, category, raw_val = parts
            val = float(raw_val)

            if category not in stats:
                stats[category] = {"count": 0, "min": val, "max": val, "sum": 0.0}

            entry = stats[category]
            entry["count"] += 1
            entry["min"] = min(entry["min"], val)
            entry["max"] = max(entry["max"], val)
            entry["sum"] += val

    summary: dict[str, dict[str, float | int]] = {}
    for category, entry in stats.items():
        cnt = entry["count"]
        summary[category] = {
            "count": cnt,
            "min": entry["min"],
            "max": entry["max"],
            "mean": round(entry["sum"] / cnt, 4),
        }
    return summary


def chapter_10_capstone() -> None:
    banner(10, "Capstone: Streaming Telemetry Analyzer & Atomic Report", "PhD / Research")

    stream_file = BOOK_DIR / "ch10_telemetry.csv"
    records = [
        "# ts,channel,reading",
        "1.0,sensor_temp,72.4",
        "2.0,sensor_temp,73.1",
        "3.0,sensor_temp,71.9",
        "1.0,bus_voltage,3.31",
        "2.0,bus_voltage,3.29",
        "3.0,bus_voltage,3.30",
    ]
    stream_file.write_text("\n".join(records) + "\n", encoding="utf-8")

    summary = stream_telemetry_stats(stream_file)
    report_path = BOOK_DIR / "ch10_summary.json"
    atomic_write_text(report_path, json.dumps(summary, indent=2) + "\n")

    print("Computed summary:")
    print(json.dumps(summary, indent=2))
    print("Saved atomic report to:", report_path)


def cleanup_lab(keep_files: bool = False) -> None:
    if keep_files:
        print(f"\nLab files kept in: {BOOK_DIR.resolve()}")
        return
    if BOOK_DIR.exists():
        shutil.rmtree(BOOK_DIR)
        print(f"\nCleaned up lab directory: {BOOK_DIR}")


def run_book(keep_files: bool = False) -> None:
    start = time.perf_counter()
    print("STARTING PYTHON FILE HANDLING COMPLETE BOOK...")

    chapter_1_foundations()
    chapter_2_context_managers()
    chapter_3_modes_and_pointers()
    chapter_4_streaming_io()
    chapter_5_exceptions()
    chapter_6_csv_and_json()
    chapter_7_binary_and_pickle()
    chapter_8_pathlib_and_atomic_io()
    chapter_9_mmap_and_low_level()
    chapter_10_capstone()

    elapsed = time.perf_counter() - start
    print("\n" + "=" * 80)
    print(f"ALL 10 CHAPTERS COMPLETED IN {elapsed:.4f}s")
    print("=" * 80)
    cleanup_lab(keep_files=keep_files)


if __name__ == "__main__":
    # Change keep_files=True if you want to inspect generated files after running
    run_book(keep_files=False)