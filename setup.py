from setuptools import setup, find_packages

setup(
    name='image_editor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'opencv-python-headless>=4.5',
        'pillow>=9.0',
        'numpy>=1.20'
    ],
    entry_points={
        'console_scripts': [
            'image-editor=image_editor.main:main'
        ]
    },
    author='Your Name',
    description='Графический редактор изображений',
    keywords='image editor opencv',
    python_requires='>=3.7',
)