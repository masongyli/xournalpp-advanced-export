import subprocess
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path

import pdf2image
from PIL import Image


class Context():
    def __init__(self, xopp_file_path: Path, page_count: int, annotation_pdf_path: Path | None):
        self.xopp_file_path = xopp_file_path
        self.page_count = page_count
        self.annotation_pdf_path = annotation_pdf_path
        self.output_images: list[Image.Image] = []

class Operation(ABC):
    def __init__(self, config: dict):
        self.validate(config)

    @abstractmethod
    def operate(self, context: Context) -> Context:
        ...  # pragma: no cover
    
    @abstractmethod
    def validate(self, config: dict) -> None:
        """ Validates the given configuration.
        Args:
            config (dict): The configuration to be validated.

        Returns:
            None
        
        Raises:
            ValidationError: If config is invalid.
        """

class XoppExportFactory:
    _image_cache: dict[tuple[Path, bool, bool], list[Image.Image]] = {}

    @classmethod
    def get_xopp_export(
        cls,
        xopp_file_path: Path,
        paper_background_preserved: bool,
        transparent_pdf_background: bool,
        page_count: int,
        has_pdf: bool = True
    ) -> list[Image.Image]:
        """
        Get images of a XOPP file.

        Args:
            xopp_file_path (str): The path to the XOPP file.
            paper_background_preserved (bool): Whether to preserve the paper background.
            transparent_pdf_background (bool): Whether the PDF background should be made transparent.
            page_count (int): The number of pages in the XOPP file.
            has_pdf (bool, optional): Whether the XOPP file has a PDF. Defaults to True. 
                    If the xopp file doesn't have annotation pdf, then we could acerate the image creation process. 
                    If this information is missing, then we would assume that the xopp file has a pdf.

        Returns:
            list[Image.Image]: A list of images created from the XOPP file export.
        """

        images = cls._image_cache.get((
            xopp_file_path,
            paper_background_preserved,
            transparent_pdf_background
        ))

        # if images have been created, we can simply return the cached images
        if images is not None:
            return images

        # if images have not been created, then we need to ues xournalpp to create images
        images = cls._create_xounrnalpp_images(
            xopp_file_path,
            paper_background_preserved,
            transparent_pdf_background,
            page_count,
            has_pdf
        )

        cls._image_cache[(
            xopp_file_path,
            paper_background_preserved,
            transparent_pdf_background
        )] = images

        if not has_pdf:
            cls._image_cache[(
                xopp_file_path,
                paper_background_preserved,
                not transparent_pdf_background
            )] = images

        return images
        
    @classmethod
    def _create_xounrnalpp_images(
        cls,
        xopp_file_path: Path,
        paper_background_preserved: bool,
        transparent_pdf_background: bool,
        page_count: int,
        has_pdf: bool
    ) -> list[Image.Image]:
        """ Create Xournal++ images by using xournalpp command line tool.

        Args:
            xopp_file_path (str): The path to the Xournal++ file.
            paper_background_preserved (bool): Whether to preserve the paper background in the exported images.
            transparent_pdf_background (bool): Whether to use a transparent PDF background in the exported images.
            has_pdf (bool): Whether the Xournal++ file has an associated PDF.
            page_count (int): The number of pages in the Xournal++ file.

        Returns:
            list[Image.Image]: A list of PIL Image objects representing the exported images.
        """

        # export_option
        if paper_background_preserved:
            background_option = ""
        else:
            background_option = "--export-no-ruling"

        if not has_pdf or not transparent_pdf_background:
            images = cls._create_image_with_opaque_pdf(
                xopp_file_path,
                page_count,
                background_option,
            )
        else:
            images = cls._create_image_with_transparent_pdf(
                xopp_file_path,
                page_count,
                background_option,
            )
            
        return images 

    @classmethod
    def _create_image_with_transparent_pdf(
        cls,
        xopp_file_path: Path,
        page_count: int,
        background_option: str,
    ) -> list[Image.Image]:

        with tempfile.TemporaryDirectory() as tmp_directory:
            export_pdf_path = Path(tmp_directory) / (str(xopp_file_path.stem) + ".pdf")
            export_format = "-p"   # "-p" for pdf export
            cls._execute_xournalpp_command(
                xopp_file_path,
                export_pdf_path,
                export_format,
                background_option
            )
            images = pdf2image.convert_from_path(export_pdf_path, fmt='png', transparent=True)

            # resize images converted from pdf
            ## generate reference images
            export_png_path = Path(tmp_directory) / str(xopp_file_path.stem + ".png")
            export_format = "-i"  # "-i" for png or svg export
            background_option = "--export-no-background"
            cls._execute_xournalpp_command(
                xopp_file_path,
                export_png_path,
                export_format,
            background_option)

            ref_images = cls._load_pngs(export_png_path, page_count)

            ## resize
            for i in range(len(images)):
                images[i] = images[i].resize(ref_images[i].size)
        
        return images
    
    @classmethod
    def _create_image_with_opaque_pdf(
        cls,
        xopp_file_path: Path,
        page_count: int,
        background_option: str,
    ) -> list[Image.Image]:

        with tempfile.TemporaryDirectory() as tmp_directory:
            export_png_path = Path(tmp_directory) / (str(xopp_file_path.stem) + ".png")

            export_format = "-i"  # "-i" for png or svg export
            cls._execute_xournalpp_command(
                xopp_file_path,
                export_png_path,
                export_format,
                background_option
            )

            images = cls._load_pngs(export_png_path, page_count)

        return images

    @classmethod
    def _get_png_filepaths(cls, png_file_path: Path, count: int) -> list[Path]:
        """
        Get a list of PNG file paths based on the given PNG file path and count.

        Args:
            png_file_path (Path): The path to the PNG file.
            count (int): The number of PNG files.

        Returns:
            list[Path]: A list of PNG file paths.

        Examples:
            >>> png_file_path = Path("/path/to/image.png")
            >>> count = 1
            >>> _get_png_filepaths(png_file_path, count)
            [Path('/path/to/image.png')]

            >>> png_file_path = Path("/path/to/image.png")
            >>> count = 3
            >>> _get_png_filepaths(png_file_path, count)
            [Path('/path/to/image-1.png'), Path('/path/to/image-2.png'), Path('/path/to/image-3.png')]
        """
        if count == 1:
            return [png_file_path]
        
        png_path_list = []
        for i in range(1, count+1):
            png_path_list.append(png_file_path.parent / f"{str(png_file_path.stem)}-{i}.png")
        
        return png_path_list
        
    @classmethod
    def _load_pngs(cls, png_file_path: Path, page_count: int) -> list[Image.Image]:
        png_path_list: list[Path] = cls._get_png_filepaths(png_file_path, page_count)

        images = []

        for file in png_path_list:
            with Image.open(file) as im:
                # `Image.open()` lazily load image's information
                # so we must use load() before the file is closed
                im.load()
                images.append(im)
        
        return images

    @classmethod
    def _execute_xournalpp_command(
        cls,
        xopp_file_path: Path,
        export_file_path: Path,
        export_format: str,
        export_option: str
    ) -> None:

        subprocess.run(
            [
                "xournalpp",
                str(xopp_file_path),
                export_format,
                str(export_file_path),
                export_option
            ],
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
