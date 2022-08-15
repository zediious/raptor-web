# Environment setup

## Requirements

- [anaconda3 Distribution](https://www.anaconda.com/products/distribution)

- [NPM via node.js](https://nodejs.org/en/download/)

- [Visual Studio Code](https://code.visualstudio.com/) (You could use something else, but I highly reccomend it for this stack)

## Steps

### Conda

*If you are using Linux, you can skip using the anaconda3 PS prompt, and run it in VS Code/any terminal*

1) Press your Windows Key, and type "anaconda power". You should see a "Anaconda Powershell Prompt" appear. Open the shell, and type the following commands in sequence "`conda update conda`", "`conda init`". This will allow conda to access libraries properly from Powershell/CMD. Note that you may have to prepend a `_` to any `conda` commands.

2) Open VSC, and clone your forked repository locally. Ensure you are working from a newly created branch. Open the cloned project.

3) Open the terminal, and confirm that conda has loaded the base environment into your shell (you will see a `(base)` somewhere in your command prompt if so)

4) Ensuring you are within the `raptor-web` top level directory in your terminal, run the following command; `conda env create`. This will read the `environment.yml` file and set up a conda environment with the required dependencies.

**Incomplete**