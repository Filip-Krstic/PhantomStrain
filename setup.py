from setuptools import setup, find_packages

setup(
    name='your_project_name',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python',      # for cv2
        'numpy',              # for numpy
        'langdetect',         # for langdetect
        'mtranslate',         # for mtranslate
        'pyautogui',          # for pyautogui
        'Pillow',             # for PIL (Image module)
    ],
    entry_points={
        'console_scripts': [
            'your_project=your_project.module:main_function',  # replace with your actual module and function
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
