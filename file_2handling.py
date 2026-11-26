"""
================================================================================
              PYTHON FILE HANDLING: THE COMPLETE TEXTBOOK IN CODE
          From 10th-Grade Foundations to PhD & Systems-Level Engineering
================================================================================

HOW TO USE THIS BOOK:
  1. Save this entire script as:  python_file_handling_book_full.py
  2. Run it from your terminal:   python3 python_file_handling_book_full.py
  3. Read each chapter's `#` notes alongside its runnable lab code.
  4. Toggle `KEEP_ARTIFACTS = True` at the bottom if you want to inspect every
     generated file on disk after execution finishes.

CURRICULUM MAP:
  PART I:   10th Grade / Beginner Foundations
            - Ch 1:  What Is a File, Volatile RAM vs Persistent Storage, Streams & FDs
            - Ch 2:  Opening & Closing Files, Context Managers (`with`), Encodings
            - Ch 3:  File Modes (`r`, `w`, `a`, `x`, `+`, `t`, `b`) & Overwrite Hazards

  PART II:  Intermediate (FSc / BSCS / Applied Programming)
            - Ch 4:  Reading Strategies (`read`, `readline`, `readlines`, lazy iteration)
            - Ch 5:  Writing & Appending Strategies (`write`, `writelines`, buffering)
            - Ch 6:  File Pointer Control (`tell`, `seek`, `SEEK_SET/CUR/END`, UTF-8 caveats)
            - Ch 7:  Defensive File Handling & OS Exceptions (`FileNotFoundError`, `OSError`)
            - Ch 8:  Tabular & Hierarchical Text Formats (`csv`, `DictReader`/`DictWriter`, `json`)

  PART III: Advanced & PhD / Systems-Level Engineering
            - Ch 9:  Binary Data, Byte Packing (`struct`), & Object Serialization (`pickle`)
            - Ch 10: Filesystem Paths (`pathlib.Path`), Atomic Writes (`fsync` + `os.replace`)
            - Ch 11: Temporary Files, `io` Buffering Layers, & Memory-Mapped Files (`mmap`)
            - Ch 12: Capstone Lab — Streaming Telemetry Engine, Checkpointing & Summary Report

================================================================================
"""

from __future__ import annotations

import csv
import io
import json
import mmap
import os
import pickle
import shutil
import struct
import tempfile
import time
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

# Sandbox root directory where all chapters create and inspect files.
LAB_ROOT = Path("python_file_handling_ textbook_lab".replace(" ", "_"))
KEEP_ARTIFACTS = False


def chapter_header(number: int, title: str, audience: str) -> None:
    # Prints a clean visual banner for each chapter when running the script.
    print("\n" + "#" * 80)
    print(f"# CHAPTER {number:02d}: {title}")
    print(f"# Audience Level: {audience}")
    print("#" * 80)


# ==============================================================================
# CHAPTER 01: FILES, STREAMS, STORAGE & FILE DESCRIPTORS
# Audience Level: 10th Grade / Beginner
# ==============================================================================
# 1. WHY DO FILES EXIST? (RAM vs DISK)
#    When a Python variable like `score = 95` is created, it lives in RAM
#    (Random Access Memory). RAM is fast, but volatile: as soon as your program
#    exits, your laptop restarts, or power is lost, RAM contents vanish.
#    A FILE is a named collection of bytes stored on non-volatile storage (SSD,
#    HDD, NVMe, SD card) managed by the operating system's filesystem.
#
# 2. PATH vs STREAM (FILE OBJECT)
#    - A PATH (`notes.txt` or `Path("data/notes.txt")`) is just the address or
#      name telling the OS *where* the file lives.
#    - A STREAM / FILE OBJECT is the active bridge/channel Python opens to
#      read bytes from or write bytes to that file.
#
# 3. FILE DESCRIPTOR (FD)
#    On Unix/Linux/macOS (and wrapped in Python's runtime), when a process asks
#    the OS kernel to open a file, the kernel assigns a small non-negative
#    integer called a File Descriptor (fd). Standard streams already exist in
#    every process:
#      fd 0 -> stdin  (standard input)
#      fd 1 -> stdout (standard output)
#      fd 2 -> stderr (standard error)
#    Every newly opened file gets the lowest available fd (e.g., 3, 4, 5...).
#
# 4. COMMON BEGINNER MISTAKE
#    Calling a variable `open` or `file` can shadow built-in names or confuse
#    path strings with open stream objects. Always use clear names like `path`
#    and `stream` or `f`.

def ch01_files_streams_and_descriptors() -> None:
    chapter_header(1, "Files, Streams, Storage & File Descriptors", "10th Grade / Beginner")
    LAB_ROOT.mkdir(parents=True, exist_ok=True)

    hello_path = LAB_ROOT / "ch01_hello.txt"

    # Open the file in write mode ('w') with explicit UTF-8 text encoding.
    stream = open(hello_path, "w", encoding="utf-8")

    print(f"[Ch 01] Path object        : {hello_path}")
    print(f"[Ch 01] Stream class       : {type(stream).__name__}")
    print(f"[Ch 01] OS File Descriptor : {stream.fileno()}")
    print(f"[Ch 01] Closed before close: {stream.closed}")

    stream.write("Assalam-o-Alaikum! Data written to disk stays after exit.\n")
    stream.write("RAM is temporary; files give programs persistent memory.\n")

    # Closing flushes buffered output and releases the OS file descriptor.
    stream.close()
    print(f"[Ch 01] Closed after close : {stream.closed}")


# ==============================================================================
# CHAPTER 02: SAFE OPENING, CLOSING & CONTEXT MANAGERS (`with`)
# Audience Level: 10th Grade / Beginner to Intermediate
# ==============================================================================
# 1. WHY MANUAL `.close()` CAN FAIL
#    Suppose you open a file, write part of your data, and an unexpected error
#    happens on the next line before `f.close()` is reached. Without proper
#    cleanup, the file stays open, buffered data may not flush cleanly, and open
#    file descriptors accumulate.
#
# 2. HOW THE `with` STATEMENT WORKS
#    Python's `with` statement uses the Context Manager protocol:
#      - `__enter__()` sets up the resource and returns the file object (`as f`).
#      - `__exit__()` runs automatically when the indented block finishes—whether
#        normally OR via an exception—and calls `f.close()`.
#
# 3. WHY `encoding="utf-8"` MATTERS
#    Different operating systems and locales have different default text
#    encodings (for example, legacy Windows code pages vs UTF-8 on Linux).
#    Passing `encoding="utf-8"` ensures Urdu, Arabic, emojis, symbols, and
#    accents behave consistently across machines.

def ch02_context_managers_and_encoding() -> None:
    chapter_header(2, "Context Managers ('with') & UTF-8 Encoding", "10th Grade / Beginner")
    journal_path = LAB_ROOT / "ch02_journal.txt"

    # Recommended standard pattern for text files:
    with open(journal_path, "w", encoding="utf-8") as f:
        f.write("Entry 1: 'with' closes the file automatically.\n")
        f.write("Entry 2: UTF-8 supports international text cleanly.\n")
        f.write("Entry 3: Never rely on accidental implicit closing.\n")

    # Outside the `with` block, `f` is already closed.
    print(f"[Ch 02] Wrote journal to   : {journal_path}")
    print(f"[Ch 02] Stream closed state: {f.closed}")


# ==============================================================================
# CHAPTER 03: FILE MODES (`r`, `w`, `a`, `x`, `+`, `t`, `b`) & OVERWRITE RULES
# Audience Level: 10th Grade / FSc Intermediate
# ==============================================================================
# File modes tell Python HOW you intend to interact with the file:
#
#   Mode  | Meaning      | If file exists?           | If file does NOT exist?
#   ------|--------------|---------------------------|-------------------------
#   'r'   | Read (text)  | Opens at start (offset 0) | Raises FileNotFoundError
#   'w'   | Write (text) | TRUNCATES (wipes) to 0B   | Creates new file
#   'a'   | Append (text)| Opens at end for appending| Creates new file
#   'x'   | Exclusive    | Raises FileExistsError    | Creates new file
#
# Modifiers you can combine with modes:
#   - 't' : Text mode (default). Translates platform newlines and decodes/encodes
#           strings using `encoding`.
#   - 'b' : Binary mode. Reads/writes raw `bytes` without text encoding or
#           newline translation (`encoding` is NOT used in binary mode).
#   - '+' : Read + Write update mode (e.g., 'r+', 'w+', 'a+').
#
# CRITICAL WARNING:
#   `'w'` destroys existing contents the moment the file is opened! If you want
#   to add new lines at the end without losing old ones, use `'a'`. If you want
#   to guarantee you aren't clobbering an existing file, use `'x'`.

def ch03_file_modes_and_safety() -> None:
    chapter_header(3, "File Modes ('r', 'w', 'a', 'x', '+') & Safety", "10th Grade / FSc")
    modes_file = LAB_ROOT / "ch03_modes.txt"

    # Step A: Create fresh file with 'w'
    with open(modes_file, "w", encoding="utf-8") as f:
        f.write("First version of file.\n")

    # Step B: Append with 'a' (preserves existing lines)
    with open(modes_file, "a", encoding="utf-8") as f:
        f.write("Second line appended with 'a'.\n")

    # Step C: Exclusive create with 'x' (fails safely if file already exists)
    try:
        with open(modes_file, "x", encoding="utf-8") as f:
            f.write("This will not be written because file exists.\n")
    except FileExistsError:
        print("[Ch 03] 'x' mode blocked overwrite because file already exists.")

    # Step D: Read-Write mode ('r+')
    # Note: 'r+' opens without truncating, starting at byte/char position 0.
    with open(modes_file, "r+", encoding="utf-8") as f:
        original = f.read()
        print(f"[Ch 03] Read via 'r+' ({len(original)} chars) before writing.")
        f.seek(0, os.SEEK_END)
        f.write("Third line added after seeking to end in 'r+'.\n")

    # Step E: Demonstrating that 'w' truncates existing content
    with open(modes_file, "w", encoding="utf-8") as f:
        f.write("Overwritten completely by 'w'.\n")

    print(f"[Ch 03] Final content of {modes_file.name}: {repr(modes_file.read_text(encoding='utf-8'))}")


# ==============================================================================
# CHAPTER 04: READING STRATEGIES (read, readline, readlines, LAZY LOOPS)
# Audience Level: FSc Intermediate / BSCS
# ==============================================================================
# Different reading methods fit different file sizes and tasks:
#   1. `f.read()`        -> Reads the ENTIRE remaining file into a single `str`
#                          (or `bytes` in binary mode). Simple for small files,
#                          dangerous for multi-gigabyte files on limited RAM.
#   2. `f.read(size)`    -> Reads at most `size` characters (text) or `size`
#                          bytes (binary). Great for fixed-size chunk readers.
#   3. `f.readline()`    -> Reads a SINGLE line up to and including `\n` (or EOF,
#                          returning `""` when end-of-file is reached).
#   4. `f.readlines()`   -> Reads all remaining lines into a `list[str]`. Each
#                          element usually ends with `\n` unless it's the last
#                          line without a trailing newline.
#   5. `for line in f:`  -> Iterates lazily over the file object using its
#                          internal read buffer. Best general pattern for large
#                          line-oriented files because it avoids building a huge
#                          list of all lines in RAM at once.
#
# TIP ON `.strip()` vs `.rstrip("\r\n")`:
#   `line.strip()` removes leading AND trailing whitespace (including spaces and
#   tabs). `line.rstrip("\r\n")` removes ONLY line endings while keeping
#   intentional indentation or trailing spaces.

def ch04_reading_strategies() -> None:
    chapter_header(4, "Reading Strategies: read, readline, readlines & Loops", "FSc / BSCS")
    sample = LAB_ROOT / "ch04_poem.txt"

    sample.write_text(
        "  Line 1: Code compiles step by step.\n"
        "  Line 2: Small functions stay easy to test.\n"
        "  Line 3: Large files need streaming at their best.\n"
        "  Line 4: Clean structure prevents every mess.\n",
        encoding="utf-8",
    )

    # 1. Whole-file read
    with open(sample, "r", encoding="utf-8") as f:
        whole = f.read()
    print(f"[Ch 04] f.read() total characters: {len(whole)}")

    # 2. Single-line reads with readline()
    with open(sample, "r", encoding="utf-8") as f:
        first_line = f.readline()
        second_line = f.readline()
    print(f"[Ch 04] readline #1: {first_line.rstrip(chr(10))!r}")
    print(f"[Ch 04] readline #2: {second_line.rstrip(chr(10))!r}")

    # 3. List of lines with readlines()
    with open(sample, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    print(f"[Ch 04] readlines() count: {len(all_lines)} items in list")

    # 4. Memory-friendly line-by-line loop with enumerate()
    print("[Ch 04] Lazy line-by-line iteration:")
    with open(sample, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            print(f"    [{idx}] {line.strip()}")

    # 5. Chunked reading with f.read(chunk_size)
    chunks: list[str] = []
    with open(sample, "r", encoding="utf-8") as f:
        while True:
            piece = f.read(25)
            if not piece:
                break
            chunks.append(piece)
    print(f"[Ch 04] Read in {len(chunks)} chunks of up to 25 chars each.")


# ==============================================================================
# CHAPTER 05: WRITING & APPENDING STRATEGIES (`write` vs `writelines`)
# Audience Level: FSc Intermediate / BSCS
# ==============================================================================
# Key rules when writing text:
#   - `f.write(s)` returns the number of CHARACTERS (not necessarily bytes!)
#     written to the text stream.
#   - `f.write()` does NOT add `\n` automatically. You must include `\n`
#     explicitly whenever you want a new line.
#   - `f.writelines(iterable)` accepts ANY iterable of strings (a list, tuple,
#     generator expression, set, etc.), NOT just a list.
#   - `f.writelines()` ALSO does NOT insert `\n` between items! Each string
#     must already contain its own newline if separate lines are desired.

def ch05_writing_and_writelines() -> None:
    chapter_header(5, "Writing & Appending: write() vs writelines()", "FSc / BSCS")
    out_path = LAB_ROOT / "ch05_output.txt"

    with open(out_path, "w", encoding="utf-8") as f:
        chars_written = f.write("Header Line\n")
        print(f"[Ch 05] f.write() returned character count: {chars_written}")

        # Generator expression avoids building an intermediate list in memory
        generated_lines = (f"Record #{n:03d}: value={n * 10}\n" for n in range(1, 6))
        f.writelines(generated_lines)

    # Appending more records later
    with open(out_path, "a", encoding="utf-8") as f:
        f.writelines(["Appended Line A\n", "Appended Line B\n"])

    line_count = sum(1 for _ in open(out_path, "r", encoding="utf-8"))
    print(f"[Ch 05] Total lines written to {out_path.name}: {line_count}")


# ==============================================================================
# CHAPTER 06: FILE POINTER CONTROL (`tell()` AND `seek()`)
# Audience Level: BSCS / Systems Fundamentals
# ==============================================================================
# Every open file stream tracks a current position (offset/cursor).
#   - `f.tell()` returns the current position.
#   - `f.seek(offset, whence=os.SEEK_SET)` moves the position:
#       * `os.SEEK_SET` (0): relative to start of file
#       * `os.SEEK_CUR` (1): relative to current position
#       * `os.SEEK_END` (2): relative to end of file
#
# CRITICAL TEXT-MODE RULE:
#   In TEXT mode, `f.tell()` returns an opaque cookie/position, and `seek()`
#   is only portable/reliable when seeking to `0` or to a position previously
#   returned by `f.tell()` on that same open handle. Seeking to arbitrary byte
#   offsets in UTF-8 text can land in the middle of a multi-byte character.
#   In BINARY mode (`'rb'`, `'r+b'`), `offset` is an exact byte count and all
#   three `whence` values (`SEEK_SET`, `SEEK_CUR`, `SEEK_END`) work directly.

def ch06_pointer_seek_and_tell() -> None:
    chapter_header(6, "File Pointer Control: tell() & seek()", "BSCS / Systems")
    text_ptr_path = LAB_ROOT / "ch06_text_cursor.txt"
    text_ptr_path.write_text("0123456789ABCDEF\nGHIJKLMN\n", encoding="utf-8")

    with open(text_ptr_path, "r", encoding="utf-8") as f:
        pos0 = f.tell()
        first_six = f.read(6)
        pos_after_six = f.tell()
        rest_of_line = f.readline()

        # Rewind back to `pos_after_six` and read again
        f.seek(pos_after_six)
        re_read = f.read(4)

        # Jump all the way back to beginning
        f.seek(pos0)
        from_start = f.readline()

    print(f"[Ch 06] Text read(6)={first_six!r}, readline={rest_of_line.strip()!r}, re_read={re_read!r}")
    print(f"[Ch 06] After seek(0), first line again: {from_start.strip()!r}")

    # Binary seek with SEEK_CUR and SEEK_END
    bin_ptr_path = LAB_ROOT / "ch06_binary_cursor.bin"
    bin_ptr_path.write_bytes(b"ABCDEFGHIJKLMNOPQRST")

    with open(bin_ptr_path, "rb") as bf:
        bf.seek(5, os.SEEK_SET)         # Byte 5 -> 'F'
        at_5 = bf.read(1)
        bf.seek(3, os.SEEK_CUR)         # Skip 3 bytes ('G','H','I') -> Byte 9 ('J')
        at_9 = bf.read(2)
        bf.seek(-4, os.SEEK_END)       # 4 bytes before EOF -> 'QRST'
        last_4 = bf.read()

    print(f"[Ch 06] Binary offsets -> at_5={at_5!r}, at_9={at_9!r}, last_4={last_4!r}")


# ==============================================================================
# CHAPTER 07: DEFENSIVE PROGRAMMING & OS EXCEPTIONS
# Audience Level: BSCS / Software Engineering
# ==============================================================================
# Filesystems are external boundaries: files get moved, deleted, locked, or
# encoded differently than expected.
#
# Exception hierarchy to know:
#   `OSError` (base class for OS/I/O errors)
#     ├── `FileNotFoundError`  (errno.ENOENT)
#     ├── `FileExistsError`    (errno.EEXIST)
#     ├── `PermissionError`    (errno.EACCES / EPERM)
#     └── `IsADirectoryError`  (errno.EISDIR)
#   `UnicodeError` -> `UnicodeDecodeError` / `UnicodeEncodeError`
#
# Best practices:
#   - Catch specific exceptions first, then `OSError` if needed.
#   - Never hide bugs behind a silent bare `except:` block.
#   - Include context (filename, operation, error details) in logs/messages.

def safe_read_utf8(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"[Ch 07] FileNotFoundError: '{path}' does not exist.")
    except IsADirectoryError:
        print(f"[Ch 07] IsADirectoryError: '{path}' is a directory, not a file.")
    except PermissionError:
        print(f"[Ch 07] PermissionError: insufficient permissions for '{path}'.")
    except UnicodeDecodeError as err:
        print(f"[Ch 07] UnicodeDecodeError in '{path}' at byte {err.start}: {err.reason}")
    except OSError as err:
        print(f"[Ch 07] OSError on '{path}' (errno={err.errno}): {err.strerror}")
    return None


def ch07_defensive_exceptions() -> None:
    chapter_header(7, "Defensive Programming & OS Exceptions", "BSCS / Engineering")

    # Case 1: Missing file
    _ = safe_read_utf8(LAB_ROOT / "nonexistent_file.txt")

    # Case 2: Invalid UTF-8 byte sequence decoded as UTF-8
    bad_utf8 = LAB_ROOT / "ch07_invalid_utf8.txt"
    bad_utf8.write_bytes(b"\xff\xfe\xfdInvalid UTF-8 bytes")
    _ = safe_read_utf8(bad_utf8)

    # Case 3: Trying to read a directory as a file
    _ = safe_read_utf8(LAB_ROOT)


# ==============================================================================
# CHAPTER 08: STRUCTURED DATA — CSV & JSON
# Audience Level: BSCS / Data & Backend Engineering
# ==============================================================================
# 1. CSV (`csv` module)
#    - Best for flat tables (rows and columns).
#    - ALWAYS open files passed to `csv.reader`, `csv.writer`, `csv.DictReader`,
#      or `csv.DictWriter` with `newline=""`. The `csv` module manages its own
#      line-ending rules; without `newline=""`, extra blank lines can appear on
#      certain platforms.
#    - Remember: every value read from CSV starts as a `str`! Convert numeric
#      fields (`int`, `float`) and booleans explicitly.
#
# 2. JSON (`json` module)
#    - Best for nested objects, lists, configuration files, and API payloads.
#    - `json.dump(obj, file_obj)` / `json.load(file_obj)` work directly with
#      file streams.
#    - `json.dumps(obj)` / `json.loads(str_obj)` convert to/from Python `str`.
#    - JSON supports: `dict`, `list`, `str`, `int`, `float`, `True`/`False`,
#      `None` (`null`). It does NOT directly serialize raw `set`, `bytes`, or
#      arbitrary custom class objects without conversion.

@dataclass
class StudentRecord:
    roll_no: int
    name: str
    marks: float
    passed: bool


def ch08_csv_and_json() -> None:
    chapter_header(8, "Structured Data: CSV & JSON", "BSCS / Data & Backend")

    students = [
        StudentRecord(1, "Zainab", 94.5, True),
        StudentRecord(2, "Hamza", 81.0, True),
        StudentRecord(3, "Maryam", 42.0, False),
    ]

    # --- CSV WRITE & READ ---
    csv_path = LAB_ROOT / "ch08_students.csv"
    fieldnames = ["roll_no", "name", "marks", "passed"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in students:
            writer.writerow(asdict(s))

    loaded_students: list[StudentRecord] = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            loaded_students.append(
                StudentRecord(
                    roll_no=int(row["roll_no"]),
                    name=row["name"],
                    marks=float(row["marks"]),
                    passed=row["passed"].strip().lower() == "true",
                )
            )

    print(f"[Ch 08] Loaded {len(loaded_students)} typed StudentRecord rows from CSV.")

    # --- JSON WRITE & READ ---
    json_path = LAB_ROOT / "ch08_cohort.json"
    cohort_payload = {
        "course": "CS-204 File & Storage Systems",
        "total_students": len(loaded_students),
        "records": [asdict(s) for s in loaded_students],
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cohort_payload, f, indent=2, ensure_ascii=False)

    with open(json_path, "r", encoding="utf-8") as f:
        parsed_json = json.load(f)

    print(f"[Ch 08] JSON course='{parsed_json['course']}', count={parsed_json['total_students']}")


# ==============================================================================
# CHAPTER 09: BINARY FILES, PACKED STRUCTS & PICKLE
# Audience Level: Advanced / PhD / Systems & ML
# ==============================================================================
# 1. RAW BYTES (`bytes` & `bytearray`)
#    Images, audio, compressed archives, network packets, and custom binary
#    formats are sequences of bytes (0..255), not text strings.
#
# 2. `struct` MODULE (Fixed-Layout Binary Records)
#    When reading/writing binary headers, sensor frames, or C-compatible binary
#    structs, `struct.pack(fmt, ...)` and `struct.unpack(fmt, buffer)` convert
#    Python values into exact byte layouts.
#    Format prefixes control byte order (endianness) and alignment:
#      - `<` : little-endian, standard sizes, no extra alignment padding
#      - `>` : big-endian (network byte order), standard sizes
#      - `!` : network (= big-endian), standard sizes
#    Common type codes:
#      - `4s` : 4-byte string (`bytes`)
#      - `I`  : unsigned 32-bit integer (4 bytes)
#      - `q`  : signed 64-bit integer (8 bytes)
#      - `d`  : IEEE-754 64-bit double float (8 bytes)
#
# 3. `pickle` MODULE (Python Object Serialization)
#    `pickle` serializes Python object graphs into a byte stream (`pickle.dump` /
#    `pickle.load`). Very common for local ML checkpoints or experiment caches.
#    SECURITY RULE: Never unpickle untrusted data from the network or unknown
#    users, because crafted pickle streams can execute arbitrary code when
#    loaded.

def ch09_binary_struct_and_pickle() -> None:
    chapter_header(9, "Binary Data, struct Packing & pickle", "Advanced / PhD / Systems")

    # Binary record layout:
    #   magic   : 4 bytes ("PKT1")
    #   seq_id  : uint32 (4 bytes)
    #   sample  : float64 (8 bytes)
    # Total per record = 16 bytes.
    record_fmt = "<4sId"
    record_size = struct.calcsize(record_fmt)
    bin_path = LAB_ROOT / "ch09_packets.bin"

    samples = [
        (b"PKT1", 101, 12.75),
        (b"PKT1", 102, -4.50),
        (b"PKT1", 103, 99.125),
    ]

    with open(bin_path, "wb") as f:
        for magic, seq_id, val in samples:
            f.write(struct.pack(record_fmt, magic, seq_id, val))

    unpacked_records: list[tuple[bytes, int, float]] = []
    with open(bin_path, "rb") as f:
        while True:
            raw_rec = f.read(record_size)
            if not raw_rec:
                break
            if len(raw_rec) < record_size:
                raise EOFError("Truncated binary record encountered.")
            unpacked_records.append(struct.unpack(record_fmt, raw_rec))

    print(f"[Ch 09] Unpacked {len(unpacked_records)} binary packets ({record_size}B each): {unpacked_records}")

    # Pickle checkpoint example (trusted local experiment state only)
    pkl_path = LAB_ROOT / "ch09_checkpoint.pkl"
    checkpoint = {
        "model": "gradient_surrogate_v1",
        "iteration": 500,
        "metrics": {"rmse": 0.0042, "r2": 0.9981},
    }

    with open(pkl_path, "wb") as f:
        pickle.dump(checkpoint, f, protocol=pickle.HIGHEST_PROTOCOL)

    with open(pkl_path, "rb") as f:
        restored = pickle.load(f)

    print(f"[Ch 09] Restored pickle checkpoint iteration={restored['iteration']}, rmse={restored['metrics']['rmse']}")


# ==============================================================================
# CHAPTER 10: `pathlib.Path` & ATOMIC FILE WRITES (`fsync` + `os.replace`)
# Audience Level: Advanced / Reliability & Systems Engineering
# ==============================================================================
# 1. WHY DIRECT IN-PLACE OVERWRITES CAN CORRUPT STATE
#    If you open `state.json` with `'w'` and start writing, the file is
#    immediately truncated to 0 bytes. If power fails or your process is killed
#    mid-write, you end up with partial/corrupted data.
#
# 2. ATOMIC WRITE PATTERN
#    1. Create a temporary file in the SAME directory as the destination file
#       (same filesystem avoids cross-device rename errors).
#    2. Write all data to the temporary file.
#    3. Flush Python buffers (`tmp.flush()`) and ask the OS to push dirty
#       buffers toward storage (`os.fsync(tmp.fileno())`).
#    4. Close the temporary file, then call `os.replace(tmp_path, target_path)`.
#       On POSIX/Windows filesystems, `os.replace` atomically swaps the
#       directory entry so readers see either the old complete file or the new
#       complete file—never a half-written state.

def atomic_write_bytes(target_path: Path, data: bytes) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target_path.name}.", dir=str(target_path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as tmp_stream:
            tmp_stream.write(data)
            tmp_stream.flush()
            os.fsync(tmp_stream.fileno())
        os.replace(tmp_path, target_path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def ch10_pathlib_and_atomic_writes() -> None:
    chapter_header(10, "pathlib.Path & Atomic Writes (fsync + os.replace)", "Advanced / Reliability")

    nested_dir = LAB_ROOT / "ch10_nested" / "sub"
    target_cfg = nested_dir / "runtime.json"

    atomic_write_bytes(target_cfg, b'{"status": "healthy", "workers": 4}\n')

    stat_info = target_cfg.stat()
    print(f"[Ch 10] Target path : {target_cfg}")
    print(f"[Ch 10] File exists : {target_cfg.exists()} | Size: {stat_info.st_size} bytes")
    print(f"[Ch 10] Parent dir  : {target_cfg.parent} | Suffix: {target_cfg.suffix}")


# ==============================================================================
# CHAPTER 11: TEMPORARY FILES, `io` BUFFERS & MEMORY-MAPPED FILES (`mmap`)
# Audience Level: PhD / High-Performance Systems
# ==============================================================================
# 1. TEMPORARY FILES (`tempfile`)
#    - `TemporaryFile()` creates an unnamed temporary file (often unlinked on
#      POSIX immediately after creation), ideal for scratch space.
#    - `NamedTemporaryFile(delete=True)` creates a named file on disk and
#      deletes it automatically when closed.
#
# 2. `io.StringIO` & `io.BytesIO` (In-Memory File-Like Streams)
#    Implement the same `.read()`, `.write()`, `.seek()`, and `.getvalue()`
#    stream interface in RAM—super useful for unit testing code that expects a
#    file object without touching the disk.
#
# 3. MEMORY-MAPPED FILES (`mmap`)
#    `mmap.mmap(fileno, length, ...)` maps file contents directly into your
#    process's address space. You can slice, index, or search (`mm.find(...)`)
#    like a byte sequence while letting the OS virtual memory subsystem page
#    data in on demand.
#    PITFALL: Mapping a 0-byte file raises an error on most OSes; ensure the
#    file has non-zero length before mapping.

def ch11_tempfiles_memory_streams_and_mmap() -> None:
    chapter_header(11, "Tempfiles, StringIO/BytesIO & mmap", "PhD / High-Performance")

    # 1. NamedTemporaryFile
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=True) as tmp:
        tmp.write("Scratch line 1\nScratch line 2\n")
        tmp.flush()
        tmp.seek(0)
        print(f"[Ch 11] NamedTemporaryFile read back: {tmp.read().splitlines()}")

    # 2. In-memory stream via io.StringIO
    mem_buf = io.StringIO()
    mem_buf.write("Alpha,10\nBeta,20\n")
    mem_buf.seek(0)
    print(f"[Ch 11] StringIO lines: {mem_buf.read().splitlines()}")

    # 3. Memory-mapped file search
    mapped_path = LAB_ROOT / "ch11_region.bin"
    mapped_path.write_bytes(b"[START]__MARKER_42__[END]\n" * 50)

    with open(mapped_path, "r+b") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            offset = mm.find(b"MARKER_42")
            snippet = mm[max(0, offset - 2) : offset + 11]
            print(f"[Ch 11] mmap size={len(mm)}B, first 'MARKER_42' at offset={offset}, slice={snippet!r}")


# ==============================================================================
# CHAPTER 12: PHD / RESEARCH CAPSTONE — STREAMING LOG & TELEMETRY PIPELINE
# Audience Level: PhD / Research & Production Systems
# ==============================================================================
# Real scientific, simulation, and systems workloads combine multiple file
# handling techniques:
#   1. Generate a multi-channel measurement log stream (streaming write).
#   2. Process the log line-by-line (O(1) memory per line) while skipping blank
#      lines or comments and validating malformed rows.
#   3. Compute per-channel statistics (count, min, max, mean).
#   4. Persist both a human-readable JSON report and a binary checkpoint via
#      atomic writes so partial runs never leave corrupt output files.

def generate_telemetry_log(log_path: Path, num_rows: int = 120) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    channels = ("temperature_c", "pressure_kpa", "current_ma")

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("# Telemetry stream generated for Chapter 12 Capstone\n")
        for i in range(num_rows):
            ch = channels[i % len(channels)]
            if ch == "temperature_c":
                val = 24.0 + (i % 15) * 0.25
            elif ch == "pressure_kpa":
                val = 100.0 + (i % 10) * 0.4
            else:
                val = 120.0 + (i % 20) * 1.5
            f.write(f"{i * 0.5:.1f},{ch},{val:.4f}\n")


def analyze_telemetry_stream(log_path: Path) -> dict[str, dict[str, float | int]]:
    accum: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "min": float("inf"), "max": float("-inf"), "sum": 0.0}
    )

    with open(log_path, "r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split(",")
            if len(parts) != 3:
                raise ValueError(f"Invalid CSV record at line {line_no}: {line!r}")

            _, channel, raw_val = parts
            value = float(raw_val)

            entry = accum[channel]
            entry["count"] += 1
            if value < entry["min"]:
                entry["min"] = value
            if value > entry["max"]:
                entry["max"] = value
            entry["sum"] += value

    summary: dict[str, dict[str, float | int]] = {}
    for channel, entry in sorted(accum.items()):
        cnt = entry["count"]
        summary[channel] = {
            "count": cnt,
            "min": round(entry["min"], 4),
            "max": round(entry["max"], 4),
            "mean": round(entry["sum"] / cnt, 4),
        }
    return summary


def ch12_capstone_pipeline() -> None:
    chapter_header(12, "Capstone: Streaming Telemetry & Atomic Artifacts", "PhD / Research")

    log_path = LAB_ROOT / "ch12_telemetry.csv"
    report_path = LAB_ROOT / "ch12_summary.json"
    ckpt_path = LAB_ROOT / "ch12_summary.pkl"

    generate_telemetry_log(log_path, num_rows=120)
    summary = analyze_telemetry_stream(log_path)

    # Atomic JSON report
    atomic_write_bytes(report_path, (json.dumps(summary, indent=2) + "\n").encode("utf-8"))

    # Atomic binary checkpoint for fast Python reload
    atomic_write_bytes(ckpt_path, pickle.dumps(summary, protocol=pickle.HIGHEST_PROTOCOL))

    print("[Ch 12] Telemetry summary written atomically:")
    for ch_name, stats in summary.items():
        print(f"    - {ch_name}: {stats}")
    print(f"[Ch 12] Report saved to     : {report_path}")
    print(f"[Ch 12] Checkpoint saved to : {ckpt_path}")


# ==============================================================================
# BOOK RUNNER & CLEANUP
# ==============================================================================
def cleanup_sandbox(keep: bool = False) -> None:
    if keep:
        print(f"\n[Cleanup] Keeping generated lab files at: {LAB_ROOT.resolve()}")
        return
    if LAB_ROOT.exists():
        shutil.rmtree(LAB_ROOT)
        print(f"\n[Cleanup] Removed temporary lab directory: {LAB_ROOT}")


def run_entire_book(keep_artifacts: bool = KEEP_ARTIFACTS) -> None:
    t0 = time.perf_counter()
    print("=" * 80)
    print("RUNNING PYTHON FILE HANDLING COMPLETE TEXTBOOK")
    print("=" * 80)

    ch01_files_streams_and_descriptors()
    ch02_context_managers_and_encoding()
    ch03_file_modes_and_safety()
    ch04_reading_strategies()
    ch05_writing_and_writelines()
    ch06_pointer_seek_and_tell()
    ch07_defensive_exceptions()
    ch08_csv_and_json()
    ch09_binary_struct_and_pickle()
    ch10_pathlib_and_atomic_writes()
    ch11_tempfiles_memory_streams_and_mmap()
    ch12_capstone_pipeline()

    elapsed = time.perf_counter() - t0
    print("\n" + "=" * 80)
    print(f"ALL 12 CHAPTERS EXECUTED SUCCESSFULLY IN {elapsed:.4f}s")
    print("=" * 80)

    cleanup_sandbox(keep=keep_artifacts)


if __name__ == "__main__":
    # Set KEEP_ARTIFACTS = True above if you want to open and inspect every
    # generated text, CSV, JSON, and binary file after the script runs.
    run_entire_book(keep_artifacts=KEEP_ARTIFACTS)