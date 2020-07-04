
from pytest import raises
from notes2flashcards.main import Notes2FlashcardsTest

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


def test_command1():
    # test command1 without arguments
    argv = ['command1']
    with Notes2FlashcardsTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        assert data['foo'] == 'bar'
        assert output.find('Foo => bar')


    # test command1 with arguments
    argv = ['command1', '--foo', 'not-bar']
    with Notes2FlashcardsTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        assert data['foo'] == 'not-bar'
        assert output.find('Foo => not-bar')
