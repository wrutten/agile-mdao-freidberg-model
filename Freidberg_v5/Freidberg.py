import os
import openmdao.api as om
from openlego.utils import my_utils

from openlego.core.problem import LEGOProblem

file_dir = os.path.dirname(__file__)

prob = LEGOProblem(cmdows_path='Freidberg_v5/CMDOWS/Freidberg Opt Benchmark CPE fix bR0.xml',
                   kb_path = os.path.join(file_dir, 'KB'),
                   data_folder = 'Freidberg_v5/output_files',
                   base_xml_file='Freidberg_v5/output-opt.xml')


prob.store_model_view(open_in_browser=False)

prob.initialize_from_xml('Freidberg_v5/KB/Freidberg-base-v5.xml')
# prob.check_partials(show_only_incorrect=True, compact_print=True)

prob.recording_options['record_derivatives'] = True

prob.run_model        
prob.run_driver()

# Process results
prob.collect_results() # prints main results to command line

# cr = om.CaseReader(prob.case_reader_path)
# source = 'driver'
# filename = file_dir+'/output_files/test'

# my_utils.write_csv(cr,source,filename)


