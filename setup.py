from setuptools import setup, find_packages

setup(
    name="simple-pass",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'streamlit',
        'flask-sqlalchemy',
        'flask-cors',
        'python-dotenv',
        'cryptography',
        'requests',
        'gunicorn',
    ],
    author="Pratik Kumar Chakraborty",
    author_email="chakravartypratik377@gmail.com",
    description="A simple and secure password manager with Flask backend and Streamlit frontend",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Pratik-uzi/simple-pass",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'simple-pass=start:main',
        ],
    },
)
