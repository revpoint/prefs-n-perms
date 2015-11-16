from setuptools import setup, find_packages

setup(
    name='prefs-n-perms',
    version='0.2.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'hiredis',
        'redis',
        'redish',
    ],
    zip_safe=True,
    url='https://github.com/revpoint/prefs-n-perms',
    author='RevPoint Media LLC',
    author_email='jangl@revpointmedia.com',
    description='Manage preferences and permissions with hierarchy structure',
)
