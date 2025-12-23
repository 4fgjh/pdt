#!/usr/bin/env python3
"""
Find files containing EIT-related code.

This script searches for files in the PDT repository that contain references to
EIT* (Effort Informed Trees) and EIRM* planners. These planners are conditionally
compiled based on the PDT_EXTRA_EITSTAR_PR preprocessor flag.

Usage:
    python find_eit_files.py [options]
    
Options:
    -h, --help              Show this help message and exit
    -p, --path PATH         Base path to search (default: PDT root directory)
    -e, --extensions EXTS   File extensions to search (default: .h,.cpp,.hpp)
    -v, --verbose           Show detailed information about matches
    -c, --count             Show count of matches per file
"""

import argparse
import os
import re
import sys
from pathlib import Path


def find_pdt_root():
    """Find the root directory of the PDT repository."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'CMakeLists.txt').exists() and (current / 'src').exists():
            return current
        current = current.parent
    return None


def search_file(filepath, patterns, verbose=False, show_count=False):
    """
    Search for patterns in a file.
    
    Args:
        filepath: Path to the file to search
        patterns: List of regex patterns to search for
        verbose: If True, show line numbers and content of matches
        show_count: If True, show count of matches
    
    Returns:
        Tuple of (has_matches, match_details)
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        matches = []
        match_count = 0
        
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if pattern.search(line):
                    match_count += 1
                    if verbose:
                        matches.append((i, line.strip()))
                    break  # Only count once per line
        
        return match_count > 0, (match_count, matches)
    
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return False, (0, [])


def main():
    parser = argparse.ArgumentParser(
        description='Find files containing EIT-related code in PDT repository.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find all files with EIT references
  python find_eit_files.py
  
  # Show detailed matches with line numbers
  python find_eit_files.py -v
  
  # Show match counts per file
  python find_eit_files.py -c
  
  # Search in a specific directory
  python find_eit_files.py -p /path/to/pdt
  
  # Search specific file extensions
  python find_eit_files.py -e ".h,.cpp,.cc"
        """
    )
    
    parser.add_argument(
        '-p', '--path',
        type=str,
        default=None,
        help='Base path to search (default: PDT root directory)'
    )
    
    parser.add_argument(
        '-e', '--extensions',
        type=str,
        default='.h,.cpp,.hpp',
        help='Comma-separated file extensions to search (default: .h,.cpp,.hpp)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed information about matches including line numbers'
    )
    
    parser.add_argument(
        '-c', '--count',
        action='store_true',
        help='Show count of matches per file'
    )
    
    args = parser.parse_args()
    
    # Determine base path
    if args.path:
        base_path = Path(args.path).resolve()
    else:
        base_path = find_pdt_root()
        if base_path is None:
            print("Error: Could not find PDT root directory.", file=sys.stderr)
            print("Please specify the path with -p option.", file=sys.stderr)
            sys.exit(1)
    
    if not base_path.exists():
        print(f"Error: Path {base_path} does not exist.", file=sys.stderr)
        sys.exit(1)
    
    # Parse extensions
    extensions = tuple(ext.strip() for ext in args.extensions.split(','))
    
    # Define patterns to search for
    patterns = [
        re.compile(r'\bEIT[Ss]tar\b'),       # EITstar or EITStar
        re.compile(r'\bEIRM[Ss]tar\b'),      # EIRMstar or EIRMStar
        re.compile(r'\bEIT\b'),              # EIT alone
        re.compile(r'PDT_EXTRA_EITSTAR_PR'), # Preprocessor flag
    ]
    
    # Search for files
    print(f"Searching for EIT-related files in: {base_path}")
    print(f"File extensions: {', '.join(extensions)}")
    print()
    
    found_files = []
    total_matches = 0
    
    for root, dirs, files in os.walk(base_path):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'build', 'thirdparty', '.cache']]
        
        for filename in files:
            if any(filename.endswith(ext) for ext in extensions):
                filepath = Path(root) / filename
                has_matches, (count, details) = search_file(
                    filepath, patterns, args.verbose, args.count
                )
                
                if has_matches:
                    rel_path = filepath.relative_to(base_path)
                    found_files.append((rel_path, count, details))
                    total_matches += count
    
    # Display results
    if not found_files:
        print("No files containing EIT references were found.")
        return
    
    print(f"Found {len(found_files)} file(s) with EIT references:")
    print()
    
    for rel_path, count, details in sorted(found_files):
        if args.count:
            print(f"{rel_path} ({count} match(es))")
        else:
            print(f"{rel_path}")
        
        if args.verbose and details:
            for line_num, line_content in details:
                print(f"  Line {line_num}: {line_content}")
        
        if args.verbose or args.count:
            print()
    
    print(f"Total: {len(found_files)} file(s), {total_matches} match(es)")


if __name__ == '__main__':
    main()
