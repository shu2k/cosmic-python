import hashlib
import os
import shutil
from pathlib import Path

BLOCKSIZE = 65536


def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()


#
# def sync(source, dest):
#     # walk the source folder and build a dict of filenames and their hashes
#     source_hashes = {}
#     for folder, _, files in os.walk(source):
#         for f in files:
#             source_hashes[hash_file(Path(folder) / f)] = f
#
#     seen = set() # keep track of files we've found in the target
#
#     # walk the target folder and get the file names and hashes
#     for folder, _, files in os.walk(dest):
#         for f in files:
#             dest_path = Path(folder) / f
#             dest_hash = hash_file(dest_path)
#             seen.add(dest_hash)
#
#             # if there's a file in target that's not in source, delete it
#             if dest_hash not in source_hashes:
#                 dest_path.remove()
#             # if there's a file in target that has a different path in source,
#             # move it to the correct path
#             elif dest_hash in source_hashes and f != source_hashes[dest_hash]:
#                 shutil.move(dest_path, Path(folder) / source_hashes[dest_hash])
#
#     # for every file that appears in source but not target, copy the file to
#     # the target
#     for source_hash, f in source_hashes.items():
#         if source_hash not in seen:
#             shutil.copy(Path(source) / f, Path(dest) / f)

def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for f in files:
            hashes[hash_file(Path(folder) / f)] = f
    return hashes


def determine_actions(source_hashes, dest_hashes, source_folder, dest_folder):
    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
            sourcepath = Path(source_folder) / filename
            destpath = Path(dest_folder) / filename
            yield "COPY", sourcepath, destpath

        elif dest_hashes[sha] != filename:
            olddestpath = Path(dest_folder) / dest_hashes[sha]
            newdestpath = Path(dest_folder) / filename
            yield "MOVE", olddestpath, newdestpath

    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            yield "DELETE", dest_folder / filename


# def sync(source, dest):
#     # imperative shell step 1, gather inputs
#     source_hashes = read_paths_and_hashes(source)
#     dest_hashes = read_paths_and_hashes(dest)
#
#     # step 2: call the functional core
#     actions = determine_actions(source_hashes, dest_hashes, source, dest)
#
#     #
#     for action, *paths in actions:
#         if action == 'COPY':
#             shutil.copyfile(*paths)
#         elif action == 'MOVE':
#             shutil.move(*paths)
#         elif action == 'DELETE':
#             os.remove(paths[0])

class FileSystem:
    def read(self, path):
        return read_paths_and_hashes(path)

    def copy(self, source, dest):
        shutil.copyfile(source, dest)

    def move(self, source, dest):
        shutil.move(source, dest)

    def delete(self, dest):
        os.remove(dest)


def sync(source, dest, filesystem=FileSystem()):
    source_hashes = filesystem.read(source)
    dest_hashes = filesystem.read(dest)

    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
            sourcepath = Path(source) / filename
            destpath = Path(dest) / filename
            filesystem.copy(sourcepath, destpath)
        elif dest_hashes[sha] != filename:
            olddestpath = Path(dest) / dest_hashes[sha]
            newdestpath = Path(dest) / filename
            filesystem.move(olddestpath, newdestpath)

    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            filesystem.delete(dest / filename)


class FakeFilesystem:
    def __init__(self, path_hashes):  # (1)
        self.path_hashes = path_hashes
        self.actions = []  # (2)

    def read(self, path):
        return self.path_hashes[path]  # (1)

    def copy(self, source, dest):
        self.actions.append(('COPY', source, dest))  # (2)

    def move(self, source, dest):
        self.actions.append(('MOVE', source, dest))  # (2)

    def delete(self, dest):
        self.actions.append(('DELETE', dest))  # (2)
