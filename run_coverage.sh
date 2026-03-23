#!/bin/bash
set -e

python3 gen.py

# Ensure ARM toolchain is in PATH
export PATH=/root/arm-toolchain/bin:$PATH

# Capture coverage with lcov
lcov --gcov-tool arm-none-eabi-gcov \
     --capture \
     --directory . \
     --output-file coverage.info \
     --rc geninfo_unexecuted_blocks=1 \
     --ignore-errors source

# Generate HTML report
genhtml coverage.info --output-directory coverage_html

echo "✅ Coverage HTML report generated at coverage_html/index.html"
