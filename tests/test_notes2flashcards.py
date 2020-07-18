import sys
import os
from pytest import raises
sys.path.insert(0, '..')
from notes2flashcards.main import Notes2FlashcardsTest
import tempfile
import shutil


def test_notes2flashcards():
    # test notes2flashcards without any subcommands or arguments
    with Notes2FlashcardsTest() as app:
        app.run()
        assert app.exit_code == 0


def test_notes2flashcards_debug():
    # test that debug mode is functional
    argv = ['--debug']
    with Notes2FlashcardsTest(argv=argv) as app:
        app.run()
        assert app.debug is True


def test_convert_tsv_traverse():
    with tempfile.TemporaryDirectory() as test_dir_path:
        res_dir_path = os.path.join(os.path.dirname(__file__), 'res')
        input_file_name = 'test.yml'
        res_input_file_path = os.path.join(res_dir_path, input_file_name)
        test_input_file_path = os.path.join(test_dir_path, input_file_name)
        shutil.copy(res_input_file_path, test_dir_path)

        argv = ['convert', test_input_file_path, 'tsv_traverse']
        with Notes2FlashcardsTest(argv=argv) as app:
            app.run()

            output_file_name = 'test_tsv_traverse.txt'
            res_output_file_path = os.path.join(res_dir_path, output_file_name)
            test_output_file_path = os.path.join(test_dir_path,
                                                 output_file_name)
            with open(res_output_file_path, encoding='utf-8') as res_file:
                res_data = res_file.read()
            with open(test_output_file_path, encoding='utf-8') as test_file:
                test_data = test_file.read()

            assert test_data == res_data


def test_convert_level_lists():
    with tempfile.TemporaryDirectory() as test_dir_path:
        res_dir_path = os.path.join(os.path.dirname(__file__), 'res')
        input_file_name = 'test.yml'
        res_input_file_path = os.path.join(res_dir_path, input_file_name)
        test_input_file_path = os.path.join(test_dir_path, input_file_name)
        shutil.copy(res_input_file_path, test_dir_path)

        argv = ['convert', test_input_file_path, 'level_lists']
        with Notes2FlashcardsTest(argv=argv) as app:
            app.run()

            output_file_name = 'test_level_lists.txt'
            res_output_file_path = os.path.join(res_dir_path, output_file_name)
            test_output_file_path = os.path.join(test_dir_path,
                                                 output_file_name)
            with open(res_output_file_path, encoding='utf-8') as res_file:
                res_data = res_file.read()
            with open(test_output_file_path, encoding='utf-8') as test_file:
                test_data = test_file.read()

            assert test_data == res_data
