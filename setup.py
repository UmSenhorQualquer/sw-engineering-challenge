from setuptools import setup, find_packages

setup(
    name="bloqit",
    version="0.1.0",
    description="Bloqit API",
    author="Ricardo Ribeiro",
    author_email="ricardojvr@gmail.com",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "sqlmodel>=0.0.11",
        "python-multipart>=0.0.6",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "pydantic>=2.5.1",
        "psycopg2-binary>=2.9.10",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: FastAPI",
    ],
    include_package_data=True,
    package_data={
        'bloqit': ['data/*.json'],
    },
)
