from setuptools import find_packages, setup
from glob import glob
package_name = 'controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/policies',
            ['policies/HIM_policy.pt',
             'policies/kp_kd_random_policy.pt', 
             'policies/policy_with_45_obs.pt']),
        ('share/' + package_name + '/config',
            ['config/go2.yaml']),
    ],
    install_requires=[
        'setuptools',
        'torch>=2.0.0',
        'numpy',
        'pyyaml',
    ],
    zip_safe=True,
    maintainer='lukat',
    maintainer_email='lukat@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'controller_node = controller.convex_mpc_controller:main',
            'rl_controller = controller.rl_controller:main',
        ],
        'ros2.components': [
            'MPCControllerNode = controller.convex_mpc_controller:MPCControllerNode',
        ],
    },
)
