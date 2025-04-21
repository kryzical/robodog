from setuptools import find_packages, setup

package_name = 'controlled_movement'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='codingmccoderson',
    maintainer_email='codingmccoderson@todo.todo',
    description='for controlled movement',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'key_inpute_node = controlled_movement.key_input_node:main',
            'camera_input = controlled_movement.key_input_node:main',
        ],
    },
)
