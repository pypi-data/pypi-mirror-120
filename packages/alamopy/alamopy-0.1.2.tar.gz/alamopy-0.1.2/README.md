# alamopy

This is an interface for using ALAMO through a Python pip package.

<h2> Preparation : </h2>

<h4> for MacOS users: </h4>

Download the ALAMO application from minlp.com, and unzip the package.

<h4>  for Windows users: </h4>

Download the ALAMO application from minlp.com, and install with the provided installer.

<h2> Data to run ALAMO:</h2>

Add the directory of the folder with your Python file to your PATH variable.
Get your ALAMO license from minlp.com and place it inside the same folder as the Python file.

Before running ALAMO, you should decide if you will provide your own data. If so, make sure your data are all in numpy arrays.
Otherwise, select the appropriate simulator to run ALAMO.

pip3 install alamopy

<h2>import alamopy as alamopy</h2>

<h2> Outputs from ALAMO </h2>

You would get the result dictionary with a best-fitted function and other variables when calling ALAMO using this python interface.

<h2> To run test files </h2>
Simply call the test files, you will get no outputs if all tests are passed. Otherwise, you will see the AssertionErrors accordingly.

If problems occur for:

- utilsTest.py, you may refer to almutils.py
- optsTest.py, you may refer to almopts.py
- tests in the Tests folder, you may reference the ALAMO executable and see if there are differences between outputs.

## Example

'''
Test 1 to see if we can generate model for z = x\*\*2
Most notably tests if the given example 1 works from ALAMO UI.
'''

import alamopy as alamo
import numpy as np

xdata = np.random.rand(11, 1)
xdata[:, 0] = [-5,-4,-3,-2,-1,0,1,2,3,4,5]

zdata = xdata[:, 0]\*\*2

opts = alamo.doalamo(xdata, zdata, linfcns = 1, logfcns = 1, sinfcns = 1, cosfns = 1, constant = 1, expfcns = 1,
monomialpower = [2,3], keep_alm_file=True, keep_lst_file=True)
