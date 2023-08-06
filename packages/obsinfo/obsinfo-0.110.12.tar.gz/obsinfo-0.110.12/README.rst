obsinfo
===================

A system for for creating FDSN-standard data and metadata for ocean bottom
seismometers using standardized, easy-to-read information files 

Current goal
-------------------

To come out with a first version (v1.x) schema for the information files.  We
would like input from seismologists and ocean bottom seismometer
manufacturers/operators about what information/capabilities are missing.  
Existing questions can be found/modified in QUESTIONS_infofiles.rst

Information files
-------------------------

The system is based on "`information files`_" in JSON or YAML format, which can
be used to create StationXML files and to record data preparation steps.  The
files duplicate the StationXML format where possible, deviating where necessary
to reduce redundancy and to add functionality (see "`information files`_")

There are 2 main file types:

============================ ======================= ================= ================
    Name                         Description              Filled by     When filled   
============================ ======================= ================= ================
  **network**                 Deployed stations,                        after a       
                              their instruments       OBS operator      campaign      
                              and parameters                                          
---------------------------- ----------------------- ----------------- ----------------
  **instrumentation**         Instrument and          OBS operator      new/changed   
   including components       component               and/or            instruments,  
   (sensor, preamplfier,      descriptions            component         components, or
   datalogger), stages                                manufacturers     calibrations  
   and filters
============================ ======================= ================= ================

Each of these files can have subfiles referenced using the `JSONref`_ protocol.
This allows, for example, one to make **response** and **filter** files to
avoid repetition. 

In principle (not yet implemented), the **instrument_components** files could
be replaced by references to the AROL (Atomic Response Objects Library),
but obsinfo provides a simpler and more standards-compliant way to specify
the components, and it can automatically calculate response sensitivities based
on gains and filter characteristics.  **Instrumentation** files should also be
able to make RESP-files and NRL directories (not implemented). 

A third type of Information File is the **campaign** file, which allows the
chief scientist to specify all of the stations and OBS operators used
for a given experiment, as well as periods of data that they would like to
see in order to validate the data preparation.  For the moment, obsinfo doesn't
do anything with these files, but can validate them.

Python code
--------------------

The package name is ``obsinfo``

``obsinfo.network``, ``obsinfo.instrumentation`` and
``obsinfo.instrument_components`` contain code to process the corresponding
information files. ``obsinfo.misc`` contains code common to the above modules

`obspy.addons` contains modules specific to proprietary systems:

- ``obspy.addons.LCHEAPO`` creates scripts to convert LCHEAPO OBS data to
  miniSEED using the ``lc2ms`` software
- ``obspy.addons.SDPCHAIN`` creates scripts to convert basic miniSEED data
  to OBS-aware miniSEED using the ``SDPCHAIN`` software suite
- ``obspy.addons.OCA`` creates JSON metadata in a format used by the
  Observatoire de la Cote d'Azur to create StationXML

Executables
----------------

The following command-line executables perform useful tasks:

- ``obsinfo-validate``: validates an information file against its schema
- ``obsinfo-print``: prints a summary of an information file
- ``obsinfo-makeSTATIONXML``: generates StationXML files from a network +
  instrumentation information files

The following command-line executables make scripts to run specific data conversion software:

- ``obsinfo-make_LCHEAPO_scripts``: Makes scripts to convert LCHEAPO data to miniSEED
- ``obsinfo-make_SDPCHAIN_scripts``: Makes scripts to drift correct miniSEED data and package
  them for FDSN-compatible data centers

Other subdirectories
-----------------------

`obsinfo/data/schema`
------------------------------------------------------------

Contains JSON Schema for each file type.


`obsinfo/_examples/`
------------------------------------------------------------

Contains example information files and scripts:

- ``_examples/Information_Files`` contains a complete set of information files

  * ``.../network`` contains **network** files

  * ``.../instrumentation`` contains **instrumentation** files

  * ``.../sensor`` contains **sensor** files

  * ``.../preamplifier`` contains **preamplifier** files

  * ``.../datalogger`` contains **datalogger** files

Each one of the last three contain directories **response** and **filter** with the respective types of files. Other directories under Information_files contain auxiliary information files and are not part of the main hierarchy.

- ``_examples/scripts`` contains bash scripts to look at and manipulate these files
  using the executables.  Running these scripts is a good way to make sure your
  installation works, looking at the files they work on is a good way to start
  making your own information files.

Versioning
----------------

We use standard MAJOR.MINOR.MAINTENANCE version numbering but, while the
system is in prerelease:

- MAJOR==0

- MINOR increments every time the information 
  file structure changes in a **non-backwards-compatible** way

- MAINTENANCE increments when the code changes or the file structure changes
  in a **backwards-compatible** way

More information
-----------------

All documentation for the project resides `in this repository  <https://obsinfo.readthedocs.io/en/latest/index.html>`_:

The project itself resides `in a Gitlab repository <https://gitlab.com/resif/obsinfo>`_:


Use `reStructuredText
<http://docutils.sourceforge.net/rst.html>`_ to modify this file.

.. _information-files: information_files.rst

.. _source-code-repository: https://www.gitlab.com/resif/obsinfo

.. _JSONref: <https://tools.ietf.org/id/draft-pbryan-zyp-json-ref-03.html>

