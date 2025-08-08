from setuptools import setup, find_packages

setup(
    name='audio-mcp-server',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastmcp',
        'python-dotenv',
        'sounddevice',
        'soundfile',
        'numpy',
        'PySoundFile',
        'google-generativeai',
    ],
    entry_points={
        'console_scripts': [
            'audio-mcp-server=audio_server:mcp.run',
        ],
    },
    author='Your Name', # Replace with your name
    author_email='your.email@example.com', # Replace with your email
    description='A FastMCP server for audio interaction and Gemini API communication.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/Audio-MCP-Server', # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
