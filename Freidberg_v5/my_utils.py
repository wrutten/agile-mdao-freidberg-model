import matplotlib.pyplot as plt
import numpy as np
import os.path

## Plot values at every iteration to show convergence history.
def plot_opt_hist(cr, base_filename, show = False):
    # Get driver cases (do not recurse to system/solver cases)
    driver_cases = cr.get_cases('driver', recurse=False)

    # Plot the path the parameters took to convergence
    obj_VIPE_values = []
    dv_a_values = []
    dv_b_values = []
    dv_c_values = []
    dv_R0_values = []
    con_PW_values = []
    con_sigma_values = []
    con_gammafrac_values = []
    con_CPE_values = []
    QOI_PE_values = []
    QOI_residuals = []

    for case in driver_cases:
        obj_VIPE_values.append(case['/dataSchema/reactor/other/VIPE'])

        dv_a_values.append(case['/dataSchema/reactor/geometry/a'])
        dv_b_values.append(case['/dataSchema/reactor/geometry/b'])
        dv_c_values.append(case['/dataSchema/reactor/geometry/c'])
        dv_R0_values.append(case['/dataSchema/reactor/geometry/R0'])

        # Normalise constraint values
        PW_norm = case['/dataSchema/reactor/plasma/PW']/4-1
        sigma_norm = case['/dataSchema/reactor/coils/sigma']/300-1
        gammafrac_norm = case['/dataSchema/reactor/blanket/gammafrac']/0.01-1
        CPE_norm = case['/dataSchema/reactor/other/CPE'][0]/1000-1

        con_PW_values.append(PW_norm)
        con_sigma_values.append(sigma_norm)
        con_gammafrac_values.append(gammafrac_norm)
        con_CPE_values.append(CPE_norm)

        res = np.sqrt(PW_norm**2+sigma_norm**2+gammafrac_norm**2+CPE_norm**2)
        QOI_residuals.append(res)


    fig, (axs) = plt.subplots(2, 2)
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)


    axs[0,0].plot(np.arange(len(obj_VIPE_values)), np.array(obj_VIPE_values))
    axs[0,0].set(xlabel='Iterations', ylabel='value', title='Objective')
    # axs[0,0].set_yscale('log')
    axs[0,0].grid()

    axs[0,1].plot(np.arange(len(dv_a_values)), np.array(dv_a_values), label='a')
    axs[0,1].plot(np.arange(len(dv_b_values)), np.array(dv_b_values), label='b')
    axs[0,1].plot(np.arange(len(dv_c_values)), np.array(dv_c_values), label='c')
    axs[0,1].plot(np.arange(len(dv_R0_values)), np.array(dv_R0_values), label='R0')
    axs[0,1].set(xlabel='Iteration', ylabel='value', title='Design Variables')
    axs[0,1].grid()
    axs[0,1].legend(fontsize='small')

    axs[1,0].plot(np.arange(len(QOI_residuals)), np.array(QOI_residuals), label='Total constraint residual')
    axs[1,0].set_yscale('log')
    axs[1,0].set(xlabel='Iteration', ylabel='value', title='Quantities of Interest')
    axs[1,0].grid()
    axs[1,0].legend(fontsize='small')

    axs[1,1].plot(np.arange(len(con_PW_values)), np.array(con_PW_values), label='PW')
    axs[1,1].plot(np.arange(len(con_gammafrac_values)), np.array(con_gammafrac_values), label='gammafrac')
    axs[1,1].plot(np.arange(len(con_sigma_values)), np.array(con_sigma_values), label='sigma')
    axs[1,1].plot(np.arange(len(con_CPE_values)), np.array(con_CPE_values), label='CPE')
    axs[1,1].set(xlabel='Iteration', ylabel='Normalised value', title='Constraints')
    axs[1,1].grid()
    axs[1,1].legend(fontsize='small')

    plt.tight_layout()
    plt.savefig(base_filename+'.png',bbox_inches='tight',dpi=100)
    plt.show()

## Plot optimizer derivative values
def plot_opt_deriv(cr, base_filename, show = False):

    driver_cases = cr.get_cases('driver', recurse=False)

    # Plot the path the parameters took to convergence
    obj_VIPE_values = []
    dv_a_values = []
    dv_b_values = []
    dv_c_values = []
    dv_R0_values = []
    con_PW_values = []
    con_sigma_values = []
    con_gammafrac_values = []
    QOI_PE_values = []

    for case in driver_cases:
            obj_VIPE_values.append(case['/dataSchema/reactor/other/VIPE'])

            dv_a_values.append(case['/dataSchema/reactor/geometry/a'])
            dv_b_values.append(case['/dataSchema/reactor/geometry/b'])
            dv_c_values.append(case['/dataSchema/reactor/geometry/c'])
            dv_R0_values.append(case['/dataSchema/reactor/geometry/R0'])

            con_PW_values.append(case['/dataSchema/reactor/plasma/PW']/4)
            con_sigma_values.append(case['/dataSchema/reactor/coils/sigma']/300)
            con_gammafrac_values.append(case['/dataSchema/reactor/blanket/gammafrac']/0.01)

            QOI_PE_values.append(case['/dataSchema/reactor/other/PE'][0])

    # plt.tight_layout()
    # plt.savefig(base_filename+'.png',bbox_inches='tight',dpi=100)

    # if show == True:
    #     plt.show()

# Plot a scan for Design Of Experiment (DOE) drivers
def plot_DOE(cr):

    # Get driver cases (do not recurse to system/solver cases)
    driver_cases = cr.get_cases('driver', recurse=False)

    # Plot the path the parameters took to convergence
    obj_VIPE_values = []
    dv_a_values = []
    dv_b_values = []
    dv_c_values = []
    dv_R0_values = []
    con_PW_values = []
    con_sigma_values = []
    con_gammafrac_values = []
    QOI_PE_values = []

    # TODO: automatically select all objs, dvs, cons, qois for the plots. Automatically scale them.

    for case in driver_cases:
        obj_VIPE_values.append(case['/dataSchema/reactor/other/VIPE'])

        dv_a_values.append(case['/dataSchema/reactor/geometry/a'])
        dv_b_values.append(case['/dataSchema/reactor/geometry/b'])
        dv_c_values.append(case['/dataSchema/reactor/geometry/c'])
        dv_R0_values.append(case['/dataSchema/reactor/geometry/R0'])

        con_PW_values.append(case['/dataSchema/reactor/plasma/PW']/4)
        con_sigma_values.append(case['/dataSchema/reactor/coils/sigma']/300)
        con_gammafrac_values.append(case['/dataSchema/reactor/blanket/gammafrac']/0.01)

        QOI_PE_values.append(case['/dataSchema/reactor/other/PE'][0])


    fig, (axs) = plt.subplots(2, 2)
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)

    axs[0,0].scatter(np.array(dv_a_values), np.array(obj_VIPE_values))
    # axs[0,0].scatter(np.array(dv_b_values), np.array(obj_VIPE_values))
    # axs[0,0].scatter(np.array(dv_c_values), np.array(obj_VIPE_values))
    # axs[0,0].scatter(np.array(dv_R0_values), np.array(obj_VIPE_values))

    axs[0,0].set(xlabel='Design param. value', ylabel='VIPE', title='Objective')
    axs[0,0].grid()

    # axs[0,1].plot(np.arange(len(dv_a_values)), np.array(dv_a_values), label='a')
    # axs[0,1].plot(np.arange(len(dv_b_values)), np.array(dv_b_values), label='b')
    # axs[0,1].plot(np.arange(len(dv_c_values)), np.array(dv_c_values), label='c')
    # axs[0,1].plot(np.arange(len(dv_R0_values)), np.array(dv_R0_values), label='R0')
    axs[0,1].set(xlabel='Iterations', ylabel='value', title='Design Variables')
    axs[0,1].grid()
    axs[0,1].legend()

    # axs[1,0].plot(np.arange(len(QOI_PE_values)), np.array(QOI_PE_values), label='PE')
    # axs[1,0].set(xlabel='Iterations', ylabel='value', title='Quantities of Interest')
    axs[1,0].grid()
    axs[1,0].legend()

    # axs[1,1].plot(np.arange(len(con_PW_values)), np.array(con_PW_values), label='PW')
    # axs[1,1].plot(np.arange(len(con_gammafrac_values)), np.array(con_gammafrac_values), label='gammafrac')
    # axs[1,1].plot(np.arange(len(con_sigma_values)), np.array(con_sigma_values), label='sigma')
    axs[1,1].set(xlabel='Iterations', ylabel='Normalised value', title='Constraints')
    axs[1,1].grid()
    axs[1,1].legend()

    plt.show()

# Write case reader data to a csv file to analyse in other applications.
def write_csv(cr, source, base_filename):
    """
        Write data file to be imported in the Mimer knowledge discovery tool. (https://assar.his.se/mimer/html/)


    Parameters
    ----------
    cr : CaseReader Object.
        Contains the data points to be formatted and written to '<filename>_PLOT.DAT'
    source : str
        Data source to collect cases from. Options: 'solver', 'driver', 'problem', 'system'
    filename : str
        Path to the output file.

    Returns
    -------
    <filename_PLOT.csv> : .csv file
        Data file containing reformatted output data.
    """  

    # # Prevent accidentally overwriting files
    # file_exists = os.path.exists(filename)
    # if file_exists:
    #     filename = base_filename + '(new)' + '_PLOT.csv'
    # else:
    filename = base_filename + '_PLOT.csv'


    # Get vars to print # TODO: extract from case metadata?
    cr_vars = cr.list_source_vars(source,out_stream=None)['outputs']
    selected_vars = cr_vars # TODO: Potentially filter vars to print to output file v

    # Format header row
    name = dict()
    header_row = ''
    for var in selected_vars:
        name[var] = var.split('/')[-1]
        header_row += name[var] + ';'
    header_row += "\n"
    with open(filename, "w") as plot_dat:
        plot_dat.write(header_row)

    # Format data rows
    driver_cases = cr.get_cases(source, recurse=False)
    data_rows = ''
    for case in driver_cases:
        for var in selected_vars:
            value = case.outputs[var][0]
            data_rows += str(value) + ';'
        data_rows += "\n"

    # Write data rows
    with open(filename, "a") as plot_dat:
        plot_dat.write(data_rows)






