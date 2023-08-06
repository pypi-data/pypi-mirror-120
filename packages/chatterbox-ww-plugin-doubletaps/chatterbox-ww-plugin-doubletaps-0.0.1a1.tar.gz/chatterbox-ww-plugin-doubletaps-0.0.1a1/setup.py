#!/usr/bin/env python3
from setuptools import setup


PLUGIN_ENTRY_POINT = 'chatterbox-ww-plugin-doubletaps=chatterbox_wake_word_plugin_doubletap:DoubleTapsHotwordPlugin'
setup(
    name='chatterbox-ww-plugin-doubletaps',
    version='0.0.1a1',
    description='A wake word plugin for Chatterbox',
    url='https://github.com/HelloChatterbox/chatterbox_wake_word_plugin_doubletaps',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['chatterbox_wake_word_plugin_doubletaps'],
    install_requires=["precise_lite_runner>=0.3.2",
                      "ovos-plugin-manager>=0.0.1a7"],
    zip_safe=True,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mycroft ovos plugin wake word',
    entry_points={'mycroft.plugin.wake_word': PLUGIN_ENTRY_POINT}
)
