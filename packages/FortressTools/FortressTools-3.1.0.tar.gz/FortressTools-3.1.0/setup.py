import setuptools
import os


def get_entry_points():
    apps = os.listdir(os.path.join("src", "fortresstools", "app"))
    scripts = []
    for script in apps:
        script = os.path.splitext(script)[0]
        string = "%s=fortresstools.app.%s:main" % (script, script)
        scripts.append(string)
    entry_points = {'console_scripts': scripts}
    return entry_points


with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()


setuptools.setup(
    name="FortressTools",
    author="Gembcior",
    author_email="gembcior@gmail.com",
    description="Personal Tools for development",
    url="https://github.com/gembcior/FortressTools.git",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    license="MIT",
    python_requires='>=3.6',
    setup_requires=['setuptools_scm'],
    install_requires=[
        'pyyaml',
        'rich',
        'paramiko',
    ],
    use_scm_version=True,
    include_package_data=True,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    entry_points=get_entry_points(),
)
