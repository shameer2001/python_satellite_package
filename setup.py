from setuptools import setup, find_packages

setup(
    name="aigeanpy",
    version="0.1.0",
    author="group-01",
    description="TBA",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'requests',
        'datetime',
        'h5py',
        'asdf',
        'pathlib',
        'typing',
        'matplotlib',
        'scikit-image',
        'scikit-learn',
        'argparse'
    ],
    entry_points = {
        'console_scripts':[
            'aigean_today = aigeanpy.command:process_today',
            'aigean_metadata = aigeanpy.command:process_metadata',
            'aigean_mosaic = aigeanpy.command:process_mosaic'
        ]
    }
)
