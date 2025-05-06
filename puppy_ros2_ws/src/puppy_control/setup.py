from setuptools import setup

package_name = 'puppy_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['resource/' + package_name]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Arthur Brown',
    maintainer_email='you@example.com',
    description='Control node for the Puppy robot',
    license='BSD',
    entry_points={
        'console_scripts': [
            'puppy_walk_node = puppy_control.puppy_walk_node:main',
            'puppy_walk_backward_node = puppy_control.puppy_walk_backward_node:main',
            'puppy_motion_node = puppy_control.puppy_motion_node:main',
        ],
    },
)
