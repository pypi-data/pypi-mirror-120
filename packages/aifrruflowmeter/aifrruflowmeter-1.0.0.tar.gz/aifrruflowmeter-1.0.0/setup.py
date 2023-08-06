import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='aifrruflowmeter',  
     
     version='1.0.0',
     
     author="Elijah Masanga",
     
     author_email="masanga@aifrruislabs.com",

     description="Python Wrapper Implementation of AifrruFlowMeter Written in Java",
     
     long_description=long_description,
     
     long_description_content_type="text/markdown",
     
     url="https://github.com/aifrruislabs/aifrruflowmeter",
     
     project_urls={
        "Bug Tracker": "https://github.com/aifrruislabs/aifrruflowmeter/issues",
     },

     packages=setuptools.find_packages(where="src"),
     
     package_dir={"": "src"},

     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],

     python_requires=">=2.7",
 )