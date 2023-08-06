#!/usr/bin/env python
# coding: utf-8

# In[2]:


from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='equationLibrayyy',
  version='0.0.1',
  description='An equation solver',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Gaurav Thakur',
  author_email='gaurav.thakur1998@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='equation_solver', 
  packages=find_packages(),
  install_requires=['numpy'] 
)


# In[ ]:




