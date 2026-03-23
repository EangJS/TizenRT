#!/bin/bash

echo "🔍 Running coverage analysis with lcov inside Docker..."

echo "⚠️  Cleaning up old coverage data..."
find . -type f -name "*.gcda" -delete

echo "⚙️  Building TizenRT with coverage flags..."
docker run -it --rm \
  -v /home/eugeneang/Workspace/TizenRT:/root/tizenrt \
  -v /home/eugeneang/.local/rtk-toolchain/asdk-10.3.1-4523/linux/newlib/bin:/root/arm-toolchain/bin \
  -e PATH=/root/arm-toolchain/bin:$PATH \
  tizenrt-coverage:latest \
  bash /root/tizenrt/run_coverage.sh

echo "✅ Coverage analysis completed. Check the generated HTML report in coverage_html/index.html"
