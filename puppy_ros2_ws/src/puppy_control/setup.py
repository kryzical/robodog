from setuptools import setup

package_name = 'puppy_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='Control node for the Puppy robot',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'puppy_walk_node = puppy_control.puppy_walk_node:main',
        ],
    },
)
