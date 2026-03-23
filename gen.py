
import re
import os

# Path to the UART dump file
dump_file = "teraterm.log"

# Directory to save reconstructed GCDA files
output_dir = "os/board/rtl8730e/src"

os.makedirs(output_dir, exist_ok=True)

file_start_re = re.compile(r"Emitting (\d+) bytes for (.+\.gcda[0-9a-f]*):?\s*(.*)")
hex_line_re = re.compile(r"^[0-9a-f]+:\s+([0-9a-f ]+)$")

current_file = None
expected_bytes = 0
hex_data = []

def clean_hex(s):
    return re.sub(r"[^0-9a-f]", "", s.lower())

def save_gcda(filename, hex_chunks, expected):
    hex_str = "".join([clean_hex(h) for h in hex_chunks])
    actual_bytes = len(hex_str) // 2
    if actual_bytes != expected:
        print(f"ERROR: {filename} expected {expected} bytes but got {actual_bytes}. Skipping.")
        return
    gcda_name = os.path.basename(filename)
    gcda_name = re.sub(r'(\.gcda)\d+$', r'\1', gcda_name)
    path = os.path.join(output_dir, gcda_name)
    with open(path, "wb") as f:
        f.write(bytes.fromhex(hex_str))
    print(f"Saved {path} ({actual_bytes} bytes)")

with open(dump_file, "r") as f:
    for line in f:
        line = line.strip()
        # Check for new file start
        match_file = file_start_re.match(line)
        if match_file:
            # Save previous file
            if current_file and hex_data:
                save_gcda(current_file, hex_data, expected_bytes)
            expected_bytes = int(match_file.group(1))
            current_file = match_file.group(2)
            hex_data = []
            # Capture any hex immediately after ":"
            first_hex = match_file.group(3)
            if first_hex:
                hex_data.append(first_hex)
            continue

        # Match hex lines like 00000010: ...
        match_hex = hex_line_re.match(line)
        if match_hex:
            hex_data.append(match_hex.group(1))

    # Save last file
    if current_file and hex_data:
        save_gcda(current_file, hex_data, expected_bytes)

print("All GCDA files processed!")


