import setuptools
setuptools.setup(
    name='tracardi-scaffold',
    version='1.1',
    scripts=['./cmd/tracardi-scaffold'],
    author='Me',
    description='This runs my tracardi plugin scaffold.',
    packages=['tracardi_plugin_scaffold'],
    install_requires=[
        'setuptools',
        'jinja2'
    ],
    python_requires='>=3.8',
    include_package_data=True
)