rem Python 3
python setup.py bdist_wheel

rem Python 2.7
python.exe setup.py bdist_wheel

twine upload dist/*