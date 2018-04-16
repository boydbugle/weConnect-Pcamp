import os
import unittest
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.cli.command()
def test():
    """ Run the unit tests"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run()
