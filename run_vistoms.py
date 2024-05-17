import sys, os
from kadmos.vistoms.vistoms import run_vistoms

""""
This script runs vistoms from the kadmos repository as installed in your environment.
Code is directly copied from vistoms.py if __name__ == '__main__': 
"""

# Get system arguments
args = sys.argv
# Check if folder is given in args
if '-folder' in args:
    folder = os.path.join(args[args.index('-folder') + 1],'')
    assert isinstance(folder, string_types), 'Folder should be a string.'
else:
    folder = None
# Check if open_vistoms is given in args
if '-open' in args:
    open_vistoms = args[args.index('-open') + 1]
    assert open_vistoms.lower() in ['y', 'yes', 'n', 'no']
    if open_vistoms.lower() in ['y', 'yes']:
        open_vistoms = True
    elif open_vistoms.lower() in ['n', 'no']:
        open_vistoms = False
    else:
        raise IOError('Please provide valid argument for -open, either y or n.')
else:
    open_vistoms = True  # default is to open
# Check if write_log is given in args
if '-write_log' in args:
    write_log = args[args.index('-write_log') + 1]
    assert write_log.lower() in ['y', 'yes', 'n', 'no']
    if write_log.lower() in ['y', 'yes']:
        write_log = True
    elif write_log.lower() in ['n', 'no']:
        write_log = False
    else:
        raise IOError('Please provide valid argument for -open, either y or n.')
else:
    write_log = True
# Now run the Python VISTOMS method that you have in app.py
run_vistoms(folder=folder, write_log=write_log, open_vistoms=open_vistoms)