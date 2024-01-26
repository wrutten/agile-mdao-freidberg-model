from openlego.core.problem import LEGOProblem

#the code below should work according to the demonstration found here: https://www.agile-project.eu/2018/11/30/demo-of-the-collaborative-mdo-tools/. Unfortunately, it does not work and needs debugging.

prob = LEGOProblem(cmdows_path='Freidberg v4/CMDOWS/Freidberg_MDPG.xml',
                   kb_path = 'Freidberg v4/database',
                   data_folder = 'Freidberg v4/output_files',
                   base_xml_file='Freidberg v4/output-opt.xml')


prob.store_model_view(open_in_browser=False)

prob.initialize_from_xml('Freidberg v4/Freidberg-base-v4.xml')

# print(prob.driver._problem)
# prob.run_model        
prob.run_driver()

# prob.collect_results()