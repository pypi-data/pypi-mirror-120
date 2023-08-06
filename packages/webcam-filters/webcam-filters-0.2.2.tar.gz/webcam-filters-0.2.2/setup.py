# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webcam_filters', 'webcam_filters.plugins.python']

package_data = \
{'': ['*']}

install_requires = \
['click-completion>=0.5.2,<0.6.0',
 'click>=8.0.1,<9.0.0',
 'mediapipe>=0.8.6,<0.9.0',
 'numpy>=1.21.2,<2.0.0',
 'opencv-contrib-python>=4.5.3,<5.0.0',
 'rich>=10.7.0,<11.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0']}

entry_points = \
{'console_scripts': ['webcam-filters = webcam_filters.__main__:main']}

setup_kwargs = {
    'name': 'webcam-filters',
    'version': '0.2.2',
    'description': 'Add filters (background blur, etc) to your webcam on Linux',
    'long_description': '|pypi-badge|\n\nwebcam-filters\n==============\n\nAdd filters (background blur, etc) to your webcam on Linux.\n\nVideo conferencing applications tend to either lack video effects altogether or\nsupport only a limited set of capabilities on Linux (e.g. Zoom [#]_, Google Meets [#]_).\n\nGoal here is to provide a virtual webcam via ``v4l2loopback`` with a common\nset of filters that can be used everywhere.\n\nUsage\n-----\nPassthrough (no-op)::\n\n  $ webcam-filters --input-dev /dev/video0 --output-dev /dev/video3\n\nBlur background::\n\n  $ webcam-filters --input-dev /dev/video0 --output-dev /dev/video3 --background-blur 150\n\nDependencies\n------------\nOther than the Python dependencies that can be automatically installed by Pip,\nthere are a few system dependencies that require manual attention.\n\nv4l2loopback\n************\n`v4l2loopback` kernel module is required to emulate a virtual webcam. See your\ndistro\'s docs or v4l2loopback_ on how to install and set it up\n(e.g. https://archlinux.org/packages/community/any/v4l2loopback-dkms/).\n\nYou\'ll probably want to create at least one loopback device (that\'s persistent\non boot)::\n\n  $ sudo tee /etc/modprobe.d/v4l2loopback.conf << "EOF"\n  # /dev/video3\n  options v4l2loopback video_nr=3\n  options v4l2loopback card_label="Virtual Webcam"\n  options v4l2loopback exclusive_caps=1\n  EOF\n  $ sudo modprobe v4l2loopback\n  $ v4l2-ctl --device /dev/video3 --info\n\nGstreamer\n*********\n\n- gstreamer-1.0 (e.g. https://archlinux.org/packages/extra/x86_64/gstreamer/)\n- gst-plugins-base (e.g. https://archlinux.org/packages/extra/x86_64/gst-plugins-base/)\n- gst-plugins-good (e.g. https://archlinux.org/packages/extra/x86_64/gst-plugins-good/)\n- gst-python (e.g. https://archlinux.org/packages/extra/x86_64/gst-python/)\n\n\nInstallation\n------------\n\nNix\n***\nThe provided Nix_ package bundles all the necessary GStreamer dependencies and\nshould "just work" on any distro.\n\nInstall a specific release version/tag::\n\n  $ nix-env --file https://github.com/jashandeep-sohi/webcam-filters/archive/refs/tags/v0.2.2.tar.gz --install\n\nInstall a specific branch (e.g. ``master``)::\n\n  $ nix-env --file https://github.com/jashandeep-sohi/webcam-filters/archive/refs/heads/master.tar.gz --install\n\n\nPipx/Pip\n********\nYou can also use `pipx` or `pip`. Pipx_ is recommend to keep Python dependencies\nisolated. Keep in mind this will not install ``gst-python`` or any of the other\nGStreamer dependencies, so you\'ll have to install that yourself.\n\nLatest stable::\n\n  $ pipx install --system-site-packages webcam-filters\n  $ # Or\n  $ pip install --user webcam-filters\n\nLatest pre-release::\n\n  $ pipx install --system-site-packages --pip-args=\'--pre\' webcam-filters\n  $ # Or\n  $ pip install --user --pre webcam-filters\n\nGit::\n\n  $ url="git+https://github.com/jashandeep-sohi/webcam-filters.git"\n  $ pipx install --system-site-packages "$url"\n  $ # Or\n  $ pip install --user "$url"\n\n\n.. [#] Zoom desktop client supports background blur as of version 5.7.6. Zoom on web does not.\n\n.. [#] Google Meets supports background blur only on Chrome.\n\n.. _Pipx: https://github.com/pypa/pipx\n\n.. _Nix: https://nixos.org/download.html#nix-quick-install\n\n.. _v4l2loopback: https://github.com/umlaeute/v4l2loopback\n\n.. |pypi-badge| image:: https://img.shields.io/pypi/v/webcam-filters\n    :alt: PyPI\n    :target: https://pypi.org/project/webcam-filters/\n',
    'author': 'Jashandeep Sohi',
    'author_email': 'jashandeep.s.sohi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jashandeep-sohi/webcam-filters',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
