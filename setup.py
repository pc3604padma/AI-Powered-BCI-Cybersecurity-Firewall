from setuptools import setup, find_packages

with open("README_DEPLOYMENT.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="synora-bci-security",
    version="1.0.0",
    author="Padmanathan and Oviya",
    author_email="contact@synora.io",
    description="AI-Powered Cybersecurity for Brain-Computer Interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bci_cybersecurity_project",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "synora=app:main",
        ],
    },
    include_package_data=True,
    keywords=[
        "cybersecurity",
        "bci",
        "brain-computer-interface",
        "eeg",
        "machine-learning",
        "anomaly-detection",
        "lstm",
        "security",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/bci_cybersecurity_project/issues",
        "Source": "https://github.com/yourusername/bci_cybersecurity_project",
        "Documentation": "https://github.com/yourusername/bci_cybersecurity_project#readme",
    },
)
