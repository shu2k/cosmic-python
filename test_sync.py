import shutil
import tempfile
from pathlib import Path
from sync import sync, determine_actions, FakeFilesystem


# def test_when_a_file_exists_in_the_source_but_not_the_destination():
#     try:
#         source = tempfile.mkdtemp()
#         destination = tempfile.mkdtemp()
#
#         content = "I am a very useful file"
#         (Path(source) / "my-file").write_text(content)
#
#         sync(source, destination)
#
#         expected_path = Path(destination) / "my-file"
#         assert expected_path.exists()
#         assert expected_path.read_text() == content
#
#     finally:
#         shutil.rmtree(source)
#         shutil.rmtree(destination)
#
#
# def test_when_a_file_has_been_renamed_in_the_source():
#     try:
#         source = tempfile.mkdtemp()
#         destination = tempfile.mkdtemp()
#
#         content = "I am a file that was renamed"
#         source_path = Path(source) / "source-filename"
#         old_destination_path = Path(destination) / "destination-filename"
#         expected_destination_path = Path(destination) / "source-filename"
#         source_path.write_text(content)
#         old_destination_path.write_text(content)
#
#         sync(source, destination)
#         assert expected_destination_path.exists()
#         assert expected_destination_path.read_text() == content
#         assert not old_destination_path.exists()
#
#     finally:
#         shutil.rmtree(source)
#         shutil.rmtree(destination)

# def test_when_a_file_exists_in_the_source_but_not_the_destination():
#     source_hashes = {"hash1": "fn1"}
#     dest_hashes = {}
#     actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
#     assert list(actions) == [("COPY", Path("/src/fn1"), Path("/dst/fn1"))]
#
#
# def test_when_a_file_has_been_renamed_in_the_source():
#     source_hashes = {"hash1": "fn1"}
#     dest_hashes = {"hash1": "fn2"}
#     actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
#     assert list(actions) == [("MOVE", Path("/dst/fn2"), Path("/dst/fn1"))]

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    fakefs = FakeFilesystem({
        '/src': {"hash1": "fn1"},
        '/dst': {},
    })
    sync('/src', '/dst', filesystem=fakefs)
    assert fakefs.actions == [("COPY", Path("/src/fn1"), Path("/dst/fn1"))]


def test_when_a_file_has_been_renamed_in_the_source():
    fakefs = FakeFilesystem({
        '/src': {"hash1": "fn1"},
        '/dst': {"hash1": "fn2"},
    })
    sync('/src', '/dst', filesystem=fakefs)
    assert fakefs.actions == [("MOVE", Path("/dst/fn2"), Path("/dst/fn1"))]
