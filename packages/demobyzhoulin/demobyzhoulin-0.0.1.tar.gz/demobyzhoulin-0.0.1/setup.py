import os
import setuptools

setuptools.setup(
    name="demobyzhoulin", 
    version="0.0.1",                       
    author="jiademandu",               
    author_email="727340437@qq.com",     
    description="A small example package", 
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bigone1/py_code",   
    packages=setuptools.find_packages(),    
    classifiers=[                    
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
