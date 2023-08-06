# Usage

1. Clone the repository
> git clone https://github.com/goodcodebadcode/pypi-helloworld.git

1. Using VSCode open folder "pypi-helloworld"

2. Install build tools
> pip install --user --upgrade setuptools wheel twine

4. Build the project
> python3 setup.py sdist bdist_wheel

5. Upload to PyPI
> python3 -m twine upload dist/*
