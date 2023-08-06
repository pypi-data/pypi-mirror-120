import setuptools

setuptools.setup(
    name='tracardi-scaffold',
    version='1.6',
    # scripts=['./cmd/tracardi-scaffold'],
    entry_points={
        'console_scripts': ['mybinary=tracardi_plugin_scaffold.create_plugin:cli'],
    },
    author='Me',
    description='This runs my tracardi plugin scaffold.',
    packages=['tracardi_plugin_scaffold'],
    install_requires=[
        'setuptools',
        'jinja2'
    ],
    python_requires='>=3.5',
    include_package_data=True
)
