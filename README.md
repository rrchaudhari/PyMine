----------

[![Join the chat at https://gitter.im/rrchaudhari/PyMine](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/rrchaudhari/PyMine?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
PyMine 1.0.1
----------
PyMine lets you integrate and visualize biological data used for drug discovery purpose. 

------------
REQUIREMENTS
------------
1) Ubuntu 11.04 or above OR Mac OS X 10.7 or above
2) PyMOL 1.7 or above
3) PyMine 1.0.1

------------
INSTALLATION
------------
1) Download and install PyMOL. http://sourceforge.net/projects/pymol/
2) Download PyMine from https://github.com/rrchaudhari/PyMine and unzip using suitable tool. 
3) Open PyMol. Install PyMine: PyMOL -> Plugins -> Manage Plugins -> Install -> (locate pymine.py file).
4) Restart PyMOL

Using MacPyMOL  
1) Rename the "MacPyMOL.app" to "PyMOLX11Hybrid.app" in Applications folder.
2) Install XQuartz found at http://xquartz.macosforge.org/landing/
3) Follow the installation procedure of plugin mentioned above. 

-----
USAGE
-----
1) Start PyMOL and go to PyMOL -> Plugins -> PyMine
2) Type the PDB id and chain id of the interested target and click SUBMIT. 
3) To find similar ligands, enter smile string into smile text box (control-v) and click on Find Similar Ligands button.

-------
RESULTS
-------
1) In PyMOL graphics viewer SAPs and Binding Sites data will be available for viewing.
2) In PyMine GUI data will be available and accessed using relevant tabs/buttons.
3) Output files will be saved in a desktop folder named "PyMine_Outdir_xxxx". 
