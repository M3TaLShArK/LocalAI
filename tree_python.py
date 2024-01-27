"""
This script generates a JSON representation of a directory structure.
It scans the specified directory and its subdirectories, building a nested dictionary that represents the directory structure.
The dictionary includes information about each file and directory, such as its name, type, size, permissions, owner, group, and last modification time.
The dictionary is then written to the specified output file in JSON format.
"""

import os
import json
import pwd
import grp
import time
import logging
import argparse
from tqdm import tqdm

def build_tree(path):
    """
    Recursively scans the specified directory and its subdirectories, building a nested dictionary that represents the directory structure.
    The dictionary includes information about each file and directory, such as its name, type, size, permissions, owner, group, and last modification time.
    """
    try:
        stat_info = os.stat(path)
        tree = {
            "type": "directory" if os.path.isdir(path) else "file",
            "name": os.path.basename(path),
            "size": stat_info.st_size,
            "permissions": oct(stat_info.st_mode)[-3:],
            "owner": pwd.getpwuid(stat_info.st_uid).pw_name,
            "group": grp.getgrgid(stat_info.st_gid).gr_name,
            "last_modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_info.st_mtime)),
            "children": []
        }
        if tree["type"] == "directory":
            for child_path in tqdm(os.listdir(path), desc=f"Scanning {path}"):
                child_path = os.path.join(path, child_path)
                tree["children"].append(build_tree(child_path))
        return tree
    except Exception as e:
        logging.error(f"Error processing {path}: {e}")
        return None

def main():
    """
    Parses command-line arguments, checks if the output file already exists, and calls the build_tree function to start the directory scan.
    If the build_tree function returns a result, writes the directory structure to the output file in JSON format.
    """
    parser = argparse.ArgumentParser(description="Generate a JSON representation of a directory structure.")
    parser.add_argument("directory", help="The directory to scan.")
    parser.add_argument("output", help="The output file name.")
    args = parser.parse_args()

    if os.path.exists(args.output):
        confirm = input(f"{args.output} already exists. Overwrite? (y/n) ")
        if confirm.lower() != "y":
            print("Aborting.")
            return

    logging.basicConfig(filename="tree.log", level=logging.INFO)
    logging.info("Starting directory scan.")

    project_tree = build_tree(args.directory)

    if project_tree is not None:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(project_tree, f, indent=2)

    logging.info("Finished directory scan.")

if __name__ == "__main__":
    main()
from tqdm import tqdm
import sys

def build_tree(path):
    """
    Recursively scans the specified directory and its subdirectories, building a nested dictionary that represents the directory structure.
    The dictionary includes information about each file and directory, such as its name, type, size, permissions, owner, group, and last modification time.
    """
    try:
        stat_info = os.stat(path)
        tree = {
            "type": "directory" if os.path.isdir(path) else "file",
            "name": os.path.basename(path),
            "size": stat_info.st_size,
            "permissions": oct(stat_info.st_mode)[-3:],
            "owner": pwd.getpwuid(stat_info.st_uid).pw_name,
            "group": grp.getgrgid(stat_info.st_gid).gr_name,
            "last_modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_info.st_mtime)),
            "children": []
        }
        if tree["type"] == "directory":
            for child_path in tqdm(os.listdir(path), desc=f"Scanning {path}"):
                child_path = os.path.join(path, child_path)
                tree["children"].append(build_tree(child_path))
        return tree
    except Exception as e:
        logging.error(f"Error processing {path}: {e}")
        return None

def main():
    """
    Parses command-line arguments, checks if the output file already exists, and calls the build_tree function to start the directory scan.
    If the build_tree function returns a result, writes the directory structure to the output file in JSON format.
    """
    parser = argparse.ArgumentParser(description="Generate a JSON representation of a directory structure.")
    parser.add_argument("directory", help="The directory to scan.")
    parser.add_argument("output", help="The output file name.")
    args = parser.parse_args()

    if os.path.exists(args.output):
        confirm = input(f"{args.output} already exists. Overwrite? (y/n) ")
        if confirm.lower() != "y":
            print("Aborting.")
            return

    logging.basicConfig(filename="tree.log", level=logging.INFO)
    logging.info("Starting directory scan.")

    project_tree = build_tree(args.directory)

    if project_tree is not None:
        with open(args.output, "w") as f:
            json.dump(project_tree, f, indent=2)

    logging.info("Finished directory scan.")

if __name__ == "__main__":
    main()