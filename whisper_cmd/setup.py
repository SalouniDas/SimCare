from setuptools import setup

package_name = 'whisper_cmd'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rucha',
    maintainer_email='your@email.com',
    description='Voice command integration with Whisper for TurtleBot3',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'whisper_node = whisper_cmd.whisper_node:main',
            #'voice_control_node = whisper_cmd.voice_control_node:main',
        ],
    },
)

