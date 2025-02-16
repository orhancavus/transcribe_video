def split_file(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    block_size = 4500
    num_parts = (
        len(content) + block_size - 1
    ) // block_size  # Calculate number of parts

    for i in range(num_parts):
        part_content = content[i * block_size : (i + 1) * block_size]
        part_filename = f"{input_file}_part_{i+1}.txt"

        with open(part_filename, "w", encoding="utf-8") as part_file:
            part_file.write(part_content)

        print(f"Saved {part_filename}")


# Usage example
split_file("input/archive/VP_sram_i_glupost.txt")
