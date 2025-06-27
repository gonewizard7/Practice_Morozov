from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name='image_editor',
    version='0.1.0',
    description='Графический редактор изображений с поддержкой веб-камеры',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Egor Morozov',
    author_email='egorm8301@gmail.com',
    url='',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics'
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'opencv-python-headless>=4.5',
        'pillow>=9.0',
        'numpy>=1.20'
    ],
    entry_points={
        'console_scripts': [
            'image-editor=image_editor.__main__:main'
        ]
    },
    python_requires='>=3.7',
    keywords='image editor opencv graphics',
    project_urls={
        'Source': 'https://github.com/gonewizard7/Practice_Morozov',
    },
)