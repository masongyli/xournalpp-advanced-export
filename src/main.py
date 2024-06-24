import argparse
from pathlib import Path

from core import Context
from pipeline import Pipeline, LinearPipeline


def get_args(arg_list: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-x",
                        "--xopp-filepath",
                        help="Absolute file path of the xopp file",
                        type=str,
                        required=True)
    parser.add_argument("-p",
                        "--pdf-filepath",
                        help="Absolute path of the annotation pdf file. \n" \
                            "If there is no annotation pdf file, then no need to provide this argument",
                        required=False)
    parser.add_argument("-n",
                        "--page-count",
                        help="total number of pages in xournalpp file (.xopp)",
                        type=int,
                        required=True)
    parser.add_argument("-c",
                        "--config-filepath",
                        help="The absolute path of the config file",
                        type=str,
                        required=True)

    args = parser.parse_args(arg_list)
    return args

def main(arg_list: list[str] | None = None):
    # create context
    args = get_args(arg_list)

    if args.pdf_filepath is None:
        annotation_pdf_path = None
    else:
        annotation_pdf_path = Path(args.pdf_filepath)

    context = Context(
        Path(args.xopp_filepath),
        args.page_count,
        annotation_pdf_path
    )

    pipeline: Pipeline = LinearPipeline(args.config_filepath)
    pipeline.run(context)

if __name__ == "__main__":
    main()  # pragma: no cover
