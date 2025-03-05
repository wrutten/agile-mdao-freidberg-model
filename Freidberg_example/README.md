This is a small example for how MDAO using the AGILE framework could work. Using the model from the book Plasma Physics and Fusion Energy by Jeffrey Freidberg (2007)

The point of the AGILE framework is to quickly set up MDAO systems, allowing optimisation over modular disciplines. It does this by separately defining the MDAO system (ie. which models are included, how they are connected, and which optimisation architecture is applied - ie. monolithic or hierarchical, etc). As the models are stored separately in the so-called knowledge base (KB), they can be called as necessary. The MDAO is assembled using openLEGO, which provides the interface with openMDAO. In this way, openMDAO is the actual optimisation platform used to solve the problem.

A whole methodology has been developed to systematically define such MDAO systems, supported by the KADMOS package. This is out-of-scope for this example, here we will just use predefined MDAO systems as stored in CMDOWS files.


In this example you find the following:
- CMDOWS folder
    The AGILE framework uses a specific procedure to formulate MDAO systems, and stores these in CMDOWS files (.xml format). In this folder you find various examples, such as a design-of-experiment (DOE, basically parameter scan), and various Optimisation architectures corresponding to slight reformulations of the Freidberg model.

- KB folder
    The AGILE framework calls the collection of models to be integrated the 'knowledge base' (KB). In this folder you find python files containing all the Freidberg equations, wrapped in a specific format such that they are usable as individual models within AGILE. Along with these python files, .xml files are present for each model to specify their I/O in terms of the specified data exchange standard. This data exchange standard (the 'dataSchema') is defined in its totallity in a separate file, in this case Freidberg-base-v5.xml. This base file also contains the initial values for the optimisation parameters.

- output_files folder
    This folder contains some example output. The main output produced by an optimisation are the "case_reader_<description>.sql", which is produced by the openMDAO caseReader class, and contains all the data traces from the optimisation. The .csv and .png files are derived from this caseReader, using the post_process.py file (with help of my_utils.py). (see https://openmdao.org/newdocs/versions/latest/features/recording/case_reader.html)

- output-opt.xml 
    This file contains the resulting optimum point in the defined dataSchema. In principle this data is also present in the caseReader files. The structure of this file should always match the base dataScheme (in this case Freidberg-base-v5.xml), to my understanding.

- reports folder
    Contains miscelaneous output from openMDAO. Not sure what is here, hasn't been relevant for me so far.

And last but not least:
- main.py
    This is the driving python file. By instantiating a so-called openLEGO problem the entire optimisation problem is created, using a selected CMDOWS file as structure, with a KB folder containing the models to be included. Furthermore, the output folder and base XML file need to be defined (the latter ends up containing the optimal data point)

References:
Freidberg, Jeffrey P. Plasma Physics and Fusion Energy. Cambridge University Press, 2007.
Gent, I. van. “Agile MDAO Systems: A Graph-Based Methodology to Enhance Collaborative Multidisciplinary Design.” Delft University of Technology, 2019. https://doi.org/10.4233/UUID:C42B30BA-2BA7-4FFF-BF1C-F81F85E890AF. (KADMOS)
Vries, Daniël de. “Towards the Industrialization of MDAO: Evolving 1st Generation MDAO to an Industry Ready Level of Maturity.” Master’s Thesis, Delft University of Technology, 2017. https://repository.tudelft.nl/islandora/object/uuid%3Accc91e95-a790-4fbc-bcaf-effedc9dbd4d. (openLEGO)
Gray, Justin S., John T. Hwang, Joaquim R. R. A. Martins, Kenneth T. Moore, and Bret A. Naylor. “OpenMDAO: An Open-Source Framework for Multidisciplinary Design, Analysis, and Optimization.” Structural and Multidisciplinary Optimization 59, no. 4 (April 1, 2019): 1075–1104. https://doi.org/10.1007/s00158-019-02211-z.

Software:
https://pypi.org/project/kadmos/
https://github.com/OpenMDAO
https://bitbucket.org/imcovangent/cmdows/issues?status=new&status=open
https://github.com/daniel-de-vries/OpenLEGO

For more information see also:
https://www.agile-project.eu/open-mdo-suite/
https://www.agile4.eu/