import os
import openmdao.api as om
import my_utils
from openlego.core.problem import LEGOProblem

file_dir = os.path.dirname(__file__)

## Construct Optimization problem from CMDOWS file and models in knowledge base.
prob = LEGOProblem(cmdows_path=os.path.join(file_dir, 'CMDOWS/Freidberg Opt Benchmark CPE_math.xml'),
                   kb_path = os.path.join(file_dir, 'KB'),
                   data_folder = os.path.join(file_dir, 'output_files'),
                   base_xml_file=os.path.join(file_dir, 'output-opt.xml'))

## Store graphical representation of optimization problem for inspection
prob.store_model_view(open_in_browser=False)

## Initialize problem with initial values
prob.initialize_from_xml('Freidberg_example/KB/Freidberg-base-v5.xml')

## Check if the analytic partial derivatives correspond with finite difference derivatives
# prob.check_partials(show_only_incorrect=True, compact_print=True)

# Set problem recording options
prob.recording_options['record_derivatives'] = True

## Run model once, or run the driver to execute optimization
# prob.run_model        
prob.run_driver()

## Collect optimization results for problem
prob.collect_results() # prints main results to command line

## Process results
# cr = om.CaseReader(prob.case_reader_path)
# source = 'driver'
# filename = file_dir+'/output_files/test'

# my_utils.write_csv(cr,source,filename)


