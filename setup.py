from setuptools import setup

setup(
    name='prefs-n-perms',
    version='0.1',
    packages=['prefs_n_perms'],
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
    description='Manage preferences and permissions for Jangl app',
)
