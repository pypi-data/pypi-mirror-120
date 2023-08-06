from setuptools import setup

setup(
    name="concrete-frontend",
    version="0.0.8",
    author="zama",
    author_email="hello@zama.ai",
    description="Concrete frontend for the Concrete Framework",
    packages=("concrete.frontend",),
    namespace_packages=("concrete",),
    package_dir={"concrete.frontend": "frontend"},
)
