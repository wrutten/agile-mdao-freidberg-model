import os
import openmdao.api as om
import my_utils
from openlego.core.problem import LEGOProblem

file_dir = os.path.dirname(__file__)

## Construct Optimization problem from CMDOWS file and models in knowledge base.
prob = LEGOProblem(cmdows_path=os.path.join(file_dir, 'CMDOWS/example.xml'),
                   kb_path = os.path.join(file_dir, 'KB'),
                   data_folder = os.path.join(file_dir, 'example_output'),
                   base_xml_file=os.path.join(file_dir, 'example_output-opt.xml'))


## Initialize problem with initial values
prob.initialize_from_xml('AGILE_example/KB/EXAMPLE-base.xml')

## Run model once
prob.run_model        