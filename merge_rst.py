"""
This script is to parse all the .rst files in the current directory and merge them into a single .rst file.
"""

import os
import sys
from tqdm import tqdm 

def main():

    # Check if the user provided the input and output directories as command line arguments
    if len(sys.argv) != 3:
        print("Please provide the input directory and output directory as command line arguments.")
        print("Usage: python merge_rst.py <input_directory> <output_directory>")
        return

    # Get the input directory and output directory from the command line arguments
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    # Get the current directory
    current_directory = os.getcwd()

    # Change the current directory to the input directory
    os.chdir(input_directory)

    # Create a list to store the content of each .rst file
    file_content = []
    document_length = 0

    # Loop through all the files in the input directory using BFS
    queue = [input_directory]
    while queue:
        current_directory = queue.pop(0)
        for file_name in os.listdir(current_directory):
            file_path = os.path.join(current_directory, file_name)
            if os.path.isdir(file_path):
                queue.append(file_path)
            elif file_name.endswith(".rst"):
                # Print the file path
                print(file_path)
                # Open the file and read its content
                with open(file_path, "r", encoding="utf-8", errors='ignore') as file:
                    content = file.read()
                    # Append the content to the list
                    file_content.append(content)
                    # count document content length
                    document_length += len(content)

    # Wait for the user to check
    input("Press Enter to continue...")

    # # Change the current directory back to the original directory
    # os.chdir(current_directory)

    # Create the output file path
    merged_file = os.path.join(output_directory, "merged.rst")
    print("Merged file path:", merged_file)

    # Open the merged file in write mode
    with open(merged_file, "w", encoding="utf-8") as file:
        # Write the content of each .rst file to the merged file
        for content in tqdm(file_content):
            file.write(content)
            
    # validate the length of the file_content
    if document_length == os.path.getsize(merged_file):
        print("The merge was successful!")
    else:
        print("The merge was not successful! original length: {}, merged length: {}".format(document_length, os.path.getsize(merged_file)))
    

if __name__ == "__main__":
    main()