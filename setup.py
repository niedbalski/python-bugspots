from setuptools import setup, find_packages

dependencies = [ "vcstools-latest" ]

setup(
    name="bug-hot-spots",
    version="0.1",
    packages=find_packages(),
    install_requires=dependencies,
    author="Punit Goswami",
    description="A Python based implementation of the bug prediction algorithm proposed by Google",
    keywords="bughotspot bug spots bug prediction",
    include_package_data=True,
    license="BSD",
    entry_points={
	'console_scripts' : [
		'bughotspots = bughotspots:main'
	]
    },

    classifiers=['Development Status :: 1 - Alpha',
                'Intended Audience :: Developers',
                'Operating System :: Unix ']
)
