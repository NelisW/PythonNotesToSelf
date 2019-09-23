# Plotly packages for Anaconda

## Offline install

It seems possible to install Anaconda packages offline as described in the following pages:  

https://support.anaconda.com/hc/en-us/articles/360023861814-Installing-conda-packages-offline-  
https://support.anaconda.com/hc/en-us/articles/360023857894-Install-Package-from-your-system  

### Installing conda packages offline

To install conda packages offline, run:

    conda install /path-to-package/package-filename.tar.bz2

Replace `/path-to-package/` with the actual path, and `package-filename` with the actual filename. Packages installed by conda are normally found in the `/pkgs/` directory in the Anaconda installation directory.

If you prefer, you can create a `/tar/` archive file containing many conda packages and install them all with one command:

    conda install /packages-path/packages-filename.tar

NOTE: If an installed package does not work, it may be missing dependencies that need to be resolved manually.

Installing packages directly from the file does not resolve dependencies.

### Install Package from your system

**Problem**

Installing a conda package using a full filesystem path does not install the dependencies.

Example:

    conda install /path-to-package/packagename-version-pythonversion.tar.bz2

**Solution**

To install dependencies, use the `--use-local` flag to install a local package from the `~/pkgs` folder or `~/conda-bld/subdir` folder.

Example:

    conda install --use-local packagename




## Plotly package downloads and install

Plotly packages seem to be here:  
https://anaconda.org/plotly  
https://anaconda.org/plotly/repo  
There are 17 packages, located under the package name, Files tab:
https://anaconda.org/plotly/plotly/files  
or   
https://anaconda.org/plotly/dash/files  

Dash installation page `https://dash.plot.ly/installation` assumes that you are installing from the internet. Note the stated dependencies (which must now be installed manually).

For the `pyqt-dash.py` demo  you need to install these components:

    conda install dash
    conda install dash-html-components
    conda install dash-core-components
    conda install dash-table
    conda install dash-daq


C:\Users\wher.KENTRONNET\AppData\Local\Continuum\Anaconda3\

    conda install dash-0.39.0-py_0.tar.bz2
    conda install flask-compress-1.4.0-py_0.tar.bz2
    conda install plotly-4.1.1-py_0.tar.bz2
    conda install dash-html-components-0.14.0-py_0.tar.bz2
    conda install dash-core-components-0.44.0-py_0.tar.bz2
    conda install dash-table-3.6.0-py_0.tar.bz2
    conda install dash-daq-0.1.4-py_0.tar.bz2
    conda install plotly-orca-1.2.1-1.tar.bz2
    conda install retrying-1.3.3-py36_1.tar.bz2
    conda install dash-renderer-0.20.0-py_0.tar.bz2


