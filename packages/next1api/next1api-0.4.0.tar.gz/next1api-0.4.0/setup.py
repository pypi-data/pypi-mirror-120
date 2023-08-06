from setuptools import setup
with open('README.md', 'r', encoding='utf-8-sig') as f:
    readme = f.read()
setup(
    name='next1api',
    version='0.4.0', 
    long_description=readme,
    long_description_content_type='text/markdown',
    description = 'Next1msuic Api', 
    url = 'https://github.com/ali-khalse/next1api',
    download_url = 'https://github.com//ali-khalse/next1api/archive/refs/heads/main.zip',    
    keywords = ['music', 'موزیک', 'next1','api'],    
    author = 'Sudo Khalse', 
    author_email = 'wwwwwq37@gmail.com', 
    license='MIT',
    packages=['next1api'],
    install_requires=['beautifulsoup4',
                      'requests',                     
                      ],

)
