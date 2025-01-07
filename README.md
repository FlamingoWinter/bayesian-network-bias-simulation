## Installation

#### Condas and Pip Packages

- Install condas from https://www.anaconda.com/download/
- create a new environment from the environment.yml file with
  `conda env create -n bayesian-network-bias-simulation --file environment.yml`
- To export the environment use `conda export > environment.yml`
- To update a local environment to be consistent with the environment file use `conda env update --file environment.yml --prune
`

#### Problems with PyMC on Windows

- The installation of PyMC has a lot of issues on Windows. First, add the following lines to your path or some Numpy
  functions won't be recognised: `C:\ProgramData\anaconda3\Scripts`, `C:\ProgramData\anaconda3\bin`,
  `C:\ProgramData\anaconda3\Library\bin`, `C:\ProgramData\anaconda3\Library\mingw-w64\bin`,
  `C:\ProgramData\anaconda3\Library\mingw-w64`, `C:\ProgramData\anaconda3\condabin`
    - See
      here (https://stackoverflow.com/questions/54063285/numpy-is-already-installed-with-anaconda-but-i-get-an-importerror-dll-load-fail).
      If you installed condas per user, this step will be different.
- There's an incompatibility with Numpy, Pytensor and PyMc. Numpy used to expose information on Blas libraries (
  optimised mathematical libraries), which PyMC used to configure Pytensor. But numpy doesn't do this anymore. So add an
  environment variable with name `PYTENSOR_FLAGS` and value
  `blas__ldflags="-L\"C:\Users\<YOUR USERNAME>\.conda\envs\bayesian-network-bias-simulation\Library\bin\" -lmkl_core -lmkl_intel_thread -lmkl_rt"`.
  This will differ depending on processors, so you can try installing pytensor to a clean environment and printing
  `pytensor.config` to see what the value of this should be.

#### GraphViz

- For plotting (which should only be necessary for debugging),
  install C++ from https://visualstudio.microsoft.com/visual-cpp-build-tools/, install graphviz
  from https://graphviz.org/download/,
  then install pygraphviz with the command:

```python -m pip install --config-settings="--global-option=build_ext" --config-settings="--global-option=-IC:\Program Files\Graphviz\include" --config-settings="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz```

- There's another weird error when plotting where `removehandler()` is called on a None object. That can be suppressed
  by modifying the library.

#### Django

- Call `<python> api/api/manage.py runserver` to run the development server.

#### PyCharm

- I used Pycharm for this, with autoformatting on save. I recommend setting up both the backend and frontend command as
  a run configuration.
- I installed the typescript and svelte extension and configured prettier to run on save.

### Svelte/Frontend

- Install node and npm from https://docs.npmjs.com/downloading-and-installing-node-js-and-npm
- Navigate into `/frontend/bias-sim` and run `npm install` to update dependencies.
- In the same directory run `npm run dev` to start the development environment.
    - The site won't work if the backend server isn't running.