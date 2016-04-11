from setuptools import setup, find_packages

dependencies = [ "vcstools-latest" ]

setup(
    name="bug-spots",
    version="0.3",
    packages=find_packages(),
    install_requires=dependencies,
    author="Jorge Niedbalski R.",
    author_email="jnr@pyrosome.org",
    description="A Python based implementation of the bug prediction algorithm proposed by Google",
    keywords="bugspot bug spots bug prediction",
    include_package_data=True,
    license="BSD",
    entry_points={
	'console_scripts' : [
		'bugspots = bugspots:main'
	]
    },

    classifiers=['Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Operating System :: Unix ']
)
