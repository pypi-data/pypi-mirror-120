from setuptools import setup


setup(
    name="opex",
    description="Exchange format for predictions from object detection algorithms (JSON).",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
    ],
    license='MIT License',
    package_dir={
        '': 'src'
    },
    packages=[
        'opex',
    ],
    install_requires=[
        "wai.json",
    ],
    version="0.0.1",
    author='Corey Sterling',
    author_email='corey.sterling@waikato.ac.nz',
)
