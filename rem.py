def remove_all_blank_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Filter out lines that are empty or contain only whitespace
    non_empty_lines = [line for line in lines if line.strip() != '']

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(non_empty_lines)

# Example usage
remove_all_blank_lines('output_clean.txt', 'output_clean.txt')
