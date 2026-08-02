import json
from setuptools import setup
from pathlib import Path

here = Path(__file__).parent
with open('package.json') as f:
    package = json.load(f)
long_description = (here / 'README.md').read_text()

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    long_description=long_description,
    long_description_content_type="text/markdown",
    # 4.1.0 floor: the first Dash release with the multi-backend (flask /
    # fastapi / quart) constructor this component targets. The wheel carries
    # ONLY the component package — none of the docs site's dependencies
    # (requirements-docs.txt) belong here.
    install_requires=['dash>=4.1.0'],
    classifiers = [
        'Framework :: Dash',
    ],    
)
