import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='get_mseed_data',  
     version='0.1',
     packages=['get_mseed_data'] ,
     author="Wilson Acero",
     author_email="acerowilson@gmail.com",
     description="Python code to download mseed data from differente services",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/awacero/get_mseed_data",
     #packages=setuptools.find_packages(),
     install_requires = ['obspy>=1.1.0'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )