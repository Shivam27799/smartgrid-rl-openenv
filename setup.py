from setuptools import setup, find_packages

setup(
    name="smartgrid-rl-v1",
    version="0.2.0",
    description="SmartGrid RL Environment - Phase 2 (OpenEnv 2.0)",
    author="Amit Seth",
    packages=find_packages(exclude=["tests", "*.tests"]),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "gymnasium>=0.29.0",
    ],
    entry_points={
        "console_scripts": [
            "smartgrid-inference=inference:run_all_tasks",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.9+",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
