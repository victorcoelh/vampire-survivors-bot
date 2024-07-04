# Vampire Survivors Bot

![Showcase:](./assets/gif_bot.gif "Bot Showcase")

A bot that automatically plays the game Vampire Survivors. Uses the YOLOv8 model to identify enemies and other items of interest.

## Installation

It is recommended to perform the following steps on a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/).

**Installing PyTorch**

To correctly use this project, PyTorch must be manually installed, with CUDA support enabled. A CUDA-capable GPU must also be detected by PyTorch on your system.

To install PyTorch, check out https://pytorch.org/get-started/locally/

**Installing other dependencies**

After installing PyTorch, you can install the other dependencies by running the following command on a virtual environment:

``pip install -r requirements.txt``

## Usage

To activate the bot, run ``main.py`` with the following command:

``python main.py``

After a short period of time, a window will open showing you what the bot is currently viewing. You can move the viewing area by pressing ``q`` with the "model vision" window active.

To pause the bot, stopping it from controlling your keyboard, press ``p`` with the "model vision" window active.

Please note that all of the previous commands are case-sensitive.

**Testing**

If you want to run one of the testing routines, execute the following command on your terminal:

``python testing.py <testing-code> <arg>``

where ``<testing-code>`` representes a numerical value between 1 and 3, indicating which test should be ran, and ``<arg>`` is any additional argument necessary for running the command. For more information, check ``testing.py``.
