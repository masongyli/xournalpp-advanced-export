from pathlib import Path

from PIL import Image


def assert_image_equal_image(a: Image.Image, b: Image.Image, msg: str | None = None) -> None:
    if a.tobytes() != b.tobytes():
        a.show()
        b.show()
        raise AssertionError(msg or "got different content")

def assert_image_equal_file(img: Image.Image, filename: Path, msg: str | None = None) -> None:
    with Image.open(filename) as img2:
        assert_image_equal_image(img, img2, msg)

def assert_file_equal_file(path1: Path, path2: Path, msg: str | None = None) -> None:
    with Image.open(path1) as img:
        with Image.open(path2) as img2:
            assert_image_equal_image(img, img2, msg)

def assert_no_png_files(dir_path: Path) -> None:
    for file in dir_path.iterdir():
        if file.suffix == '.png':
            raise AssertionError(f"Shoudn't generate image {file}")

def assert_file_exists(file_path: Path) -> None:
    if not file_path.exists():
        raise AssertionError(f"File '{file_path}' does not exist.")