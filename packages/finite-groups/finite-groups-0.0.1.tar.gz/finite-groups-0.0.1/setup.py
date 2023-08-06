import setuptools

setuptools.setup(
    name='finite-groups',
    version='0.0.1',    
    description='Finite Groups Computations',
    url='https://github.com/CrisLeaf/finite-groups',
    author='Cris Torres',
    author_email='cristobal_javier@hotmail.com',
    license='MIT License',
    packages=['fgroups'],
    install_requires=[
        'numpy'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
    ],
)

