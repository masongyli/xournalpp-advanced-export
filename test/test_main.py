import sys
import unittest
from pathlib import Path

from helper import assert_file_equal_file, assert_no_png_files, assert_file_exists
from jsonschema.exceptions import ValidationError
import pathvalidate
from tempfile import TemporaryDirectory

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from main import main


global_input_dir = Path('test/input')

global_answer_dir = Path('test/answer/linux')
# Images generated by xournalpp command line tool in Windows are slightly different from those in Linux,
if sys.platform.startswith("win"):
    global_answer_dir = Path('test/answer/windows')


page_count = {
            'empty': 1,
            'one_page': 1,
            'three_pages_with_pdf': 3,
            'three_pages': 3
}



def cleanup_pngs_in_dir(dir_path: Path) -> None:
    for file in dir_path.iterdir():
        if file.suffix == '.png':
            # remove file
            file.unlink()

def execute_main(xopp_stem: str, config_path: Path):
    arg_list = ['-x', str(global_input_dir / f"{xopp_stem}.xopp"),
                '-n', str(page_count[xopp_stem]),
                '-c', str(config_path)
    ]

    if (global_input_dir / f"{xopp_stem}.xopp.bg.pdf").exists():
        arg_list.append('-p')
        arg_list.append(str(global_input_dir / f"{xopp_stem}.bg.pdf"))
    
    main(arg_list)
    

@unittest.skipIf(sys.version_info < (3, 12),"This plugin requires Python 3.12 or higher")
class TestMainIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tempdir = TemporaryDirectory(dir=global_input_dir, prefix='config_')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tempdir.cleanup()

    def tearDown(self) -> None:
        cleanup_pngs_in_dir(global_input_dir)
    
    def test_1_one_page(self):
        xopp_stem = 'one_page'

        CONFIG_JSON = """
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "paper_background_preserved": true,
                "pdf_background_transparent": false,
                "trim": true,
                "trim_directions": [false, true, false, true],
                "trim_paddings": [0, 50, 0, 50]
            }
        },
        {
            "type": "save"
        }
    ]
}
"""        
        config_path =  Path(self.__class__.tempdir.name) / "config.json"
        with config_path.open(mode="w") as config_file:
            config_file.write(CONFIG_JSON) 

        expected_png_name = xopp_stem + '.png'

        execute_main(xopp_stem, config_path)

        assert_file_exists(global_input_dir / expected_png_name)
        assert_file_equal_file(global_input_dir / expected_png_name, global_answer_dir / 'test_1' / expected_png_name) 
            

    def test_2_three_pages_with_pdf(self):
        xopp_stem = 'three_pages_with_pdf'
        
        CONFIG_JSON = """
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "paper_background_preserved": false,
                "pdf_background_transparent": true,
                "trim": false
            }
        },
        {
            "type": "combine",
            "config": {
                "direction": "ltr",
                "vertical_align": "top"
            }
        },
        {
            "type": "save",
            "config": {
                "filename": "{{xoppStem}}_exported"
            }
        }
    ]
}
"""
        config_path =  Path(self.__class__.tempdir.name) / "config.json"
        with config_path.open(mode="w") as config_file:
            config_file.write(CONFIG_JSON)

        expected_png_name = xopp_stem + "_exported" + '.png'

        execute_main(xopp_stem, config_path)

        assert_file_exists(global_input_dir / expected_png_name)
        assert_file_equal_file(global_input_dir / expected_png_name, global_answer_dir / 'test_2' / expected_png_name)


    def test_3_empty_note(self):
        xopp_stem = 'empty'

        CONFIG_JSON = """
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "trim": true
            }
        },
        {
            "type": "save"
        }
    ]
}
"""
        config_path =  Path(self.__class__.tempdir.name) / "config.json"
        with config_path.open(mode="w") as config_file:
            config_file.write(CONFIG_JSON)

        execute_main(xopp_stem, config_path)

        assert_no_png_files(global_input_dir)


    def test_4_invalid_operation_type(self):
        xopp_stem = 'one_page'

        CONFIG_JSON = """
{
    "pipeline": [
        {
            "type": "load"
        },
        {
            "type": "Avada Kedavra",
            "config": {
                "direction": "ttb",
                "horizontal_align": "center",
                "vertical_align": "center"
            }
        },
        {
            "type": "save"
        }
    ]
}
"""
        config_path =  Path(self.__class__.tempdir.name) / "config.json"
        with config_path.open(mode="w") as config_file:
            config_file.write(CONFIG_JSON)

        with self.assertRaises(ValueError):
            execute_main(xopp_stem, config_path)

        assert_no_png_files(global_input_dir)
    

    def test_5_ttb_center(self):
        xopp_stem = 'three_pages'

        CONFIG_JSON = """
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "trim": true
            }
        },
        {
            "type": "combine",
            "config": {
                "direction": "ttb",
                "horizontal_align": "center",
                "vertical_align": "bottom"
            }
        },
        {
            "type": "save"
        }
    ]
}
"""
        config_path =  Path(self.__class__.tempdir.name) / "config.json"
        with config_path.open(mode="w") as config_file:
            config_file.write(CONFIG_JSON)

        expected_png_name = xopp_stem + '.png'

        execute_main(xopp_stem, config_path)

        assert_file_exists(global_input_dir / expected_png_name)
        assert_file_equal_file(global_input_dir / expected_png_name, global_answer_dir / 'test_5' / expected_png_name)

    def test_6_rtl_top(self):
        xopp_stem = 'three_pages'

        CONFIG_JSON = """
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "trim": true
            }
        },
        {
            "type": "combine",
            "config": {
                "direction": "rtl",
                "vertical_align": "top"
            }
        },
        {
            "type": "save"
        }
    ]
}
"""
        config_path =  Path(self.__class__.tempdir.name) / "config.json"
        with config_path.open(mode="w") as config_file:
            config_file.write(CONFIG_JSON)

        expected_png_name = xopp_stem + '.png'

        execute_main(xopp_stem, config_path)

        assert_file_exists(global_input_dir / expected_png_name)
        assert_file_equal_file(global_input_dir / expected_png_name, global_answer_dir / 'test_6' / expected_png_name)
    
    def test_7_rtl_bottom(self):
        xopp_stem = 'three_pages'

        CONFIG_JSON = """
{
    "pipeline": [
        {
            "type": "load",
            "config": {
                "trim": true
            }
        },
        {
            "type": "combine",
            "config": {
                "direction": "rtl",
                "vertical_align": "bottom"
            }
        },
        {
            "type": "save"
        }
    ]
}
"""
        config_path =  Path(self.__class__.tempdir.name) / "config.json"
        with config_path.open(mode="w") as config_file:
            config_file.write(CONFIG_JSON)

        expected_png_name = xopp_stem + '.png'

        execute_main(xopp_stem, config_path)

        assert_file_exists(global_input_dir / expected_png_name)
        assert_file_equal_file(global_input_dir / expected_png_name, global_answer_dir / 'test_7' / expected_png_name)

if __name__ == '__main__':
    unittest.main()
