from openlego.core.problem import LEGOProblem

#the code below should work according to the demonstration found here: https://www.agile-project.eu/2018/11/30/demo-of-the-collaborative-mdo-tools/. Unfortunately, it does not work and needs debugging.

prob = LEGOProblem(cmdows_path='Freidberg v4/CMDOWS/Freidberg_MDPG.xml',
                   kb_path = 'database',
                   data_folder = 'output_files',
                   base_xml_file='output-opt.xml')


prob.store_model_view(open_in_browser=True)

prob.initialize_from_xml('Freidberg-base-v4.xml')

prob.run_driver()

prob.collect_results()