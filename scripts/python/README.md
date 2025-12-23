# Python Scripts for PDT

This directory contains Python utility scripts for the Planner Developer Tools (PDT) repository.

## Available Scripts

### find_eit_files.py

Searches for files in the PDT repository that contain references to EIT* (Effort Informed Trees) and EIRM* planners. These planners are conditionally compiled based on the `PDT_EXTRA_EITSTAR_PR` preprocessor flag.

**Usage:**
```bash
# Find all files with EIT references (just file names)
python find_eit_files.py

# Show summary with file count
python find_eit_files.py -s

# Show detailed matches with line numbers
python find_eit_files.py -v

# Show match counts per file
python find_eit_files.py -c

# Search in a specific directory
python find_eit_files.py -p /path/to/pdt

# Search specific file extensions
python find_eit_files.py -e ".h,.cpp,.cc"
```

**Options:**
- `-h, --help`: Show help message and exit
- `-p PATH, --path PATH`: Base path to search (default: PDT root directory)
- `-e EXTS, --extensions EXTS`: Comma-separated file extensions to search (default: .h,.cpp,.hpp)
- `-v, --verbose`: Show detailed information about matches including line numbers
- `-c, --count`: Show count of matches per file
- `-s, --summary`: Show summary information (file count, match count)

**Example output (default):**
```
src/common/include/pdt/common/planner_type.h
src/factories/src/planner_factory.cpp
src/utilities/src/get_best_cost.cpp
...
```

**Example output (with -s flag):**
```
Searching for EIT-related files in: /path/to/pdt
File extensions: .h, .cpp, .hpp

Found 11 file(s) with EIT references:

src/common/include/pdt/common/planner_type.h
src/factories/src/planner_factory.cpp
...

Total: 11 file(s), 58 match(es)
```

### computeConfidenceInterval.py

Computes confidence intervals for experimental data.

## Requirements

All scripts require Python 3.6 or later. No additional dependencies are required for `find_eit_files.py`.
