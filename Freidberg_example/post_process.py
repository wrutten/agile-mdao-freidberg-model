import my_utils
import openmdao.api as om
import os

cr_filename = "Freidberg_example/output_files/case_reader_Freidberg Opt Benchmark CPE fix b_20250305_14412535.sql"
filename = cr_filename.split('.')[0] # remove .sql extention

cr = om.CaseReader(cr_filename)
source = 'driver'

# Write Mimer data file
my_utils.write_csv(cr,source,filename)

# Save optimization history plot
my_utils.plot_opt_hist(cr,filename)

# # Plot optimizer details
my_utils.plot_opt_deriv(cr,filename)
