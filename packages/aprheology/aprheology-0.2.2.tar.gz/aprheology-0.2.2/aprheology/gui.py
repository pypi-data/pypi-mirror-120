# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Kevin De Bruycker
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import aprheology
import PySimpleGUI as sg
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')


def GUI():
    plot_size = (5, 4.5)
    max_exponentials = 5
    sg.theme('Dark Grey 7')

    InputParameters = [
        [
            sg.Text("Experiment:"),
        ],
        [
            sg.Radio('Stress relaxation', 'ExperimentType', pad=(5, 0), disabled=True, key="-StressRelaxation-"),
        ],
        [
            sg.Radio('Frequency sweep', 'ExperimentType', pad=(5, 0), disabled=True, key="-FrequencySweep-"),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Text("Read temperature from:"),
        ],
        [
            sg.Radio('Additional column in table', 'get_T_from', pad=(5, 0), default=True, disabled=True, key="-T_from_datacolumns_names_last-"),
        ],
        [
            sg.Radio('Last number in curve header', 'get_T_from', pad=(5, 0), disabled=True, key="-T_from_curve_header_last_number-"),
        ],
        [
            sg.Text("Temperature unit:"),
            sg.DropDown(['°C', 'K'], default_value='°C', disabled=True, size=(4, 1), key="-T_unit-"),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Text('Discard first'),
            sg.Spin([i for i in range(0, 101)], initial_value=0, pad=(0, 3), size=(3,1), disabled=True, key='-datapoints_discarded-'),
            sg.Text('data points'),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Button('Open file', disabled=True, key='-OpenFile-')
        ],
    ]

    ParameterColumn1 = [
        [
            sg.Frame("Input parameters:", InputParameters, key="-InputParameters-")
        ],
    ]

    RelaxationTimeSelection = [
        [
            sg.Radio('Single Maxwell', 'tau_mode', pad=(5, 0), enable_events=True, default=True, disabled=True, key="-TauModeSingle-"),
        ],
        [
            sg.Radio('Generalised Maxwell', 'tau_mode', pad=(5, 0), enable_events=True, disabled=True, key="-TauModeGeneral-"),
        ],

    ]

    TemperatureSelection = [
        [
            sg.Listbox(values=[], disabled=True, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                       size=(13, 3), no_scrollbar=True, key="-Temperatures-"),
        ],
        [
            sg.Button('Update', disabled=True, key='-UpdateTemperatures-')
        ],
    ]

    ParameterColumn2 = [
        [
            sg.Frame("Relaxation time:", RelaxationTimeSelection, key="-RelaxationTimeSelection-")
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Frame("Temperatures:", TemperatureSelection, key="-TemperatureSelection-")
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Checkbox("Normalise G(t)", pad=(5, 0), enable_events=True, default=True, disabled=True,
                        key="-normalise_relax_mod-"),
        ],
    ]

    InputColumn = [
        [
            sg.Text("File:"),
            sg.InputText(size=(41, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse(file_types=(("CSV/Text file", ["*.csv", "*.txt"]), ("All files", "*.*"), )),
        ],
        [
            sg.Column(ParameterColumn1, vertical_alignment='top'),
            sg.Column(ParameterColumn2, vertical_alignment='top'),
        ],
    ]

    DataPlotColumn = [
        [
            sg.Canvas(size=[dim * 100 for dim in plot_size], key='-DataPlot-')
        ],
        [
            sg.Button('Open as interactive plot', disabled=True, key='-OpenDataPlot-'),
            sg.Save('Save CSV', disabled=True, key='-QuickSaveDataPlotCSV-'),
            sg.Save('Save XLSX', disabled=True, key='-QuickSaveDataPlotXLSX-'),
            sg.InputText(size=(35, 1), enable_events=True, visible=False, key="-SaveDataPlotAs-"),
            sg.FileSaveAs('Save raw plot data as...', disabled=True, file_types=(("CSV file", "*.csv"), ("Excel file", "*.xlsx"),), key='-SaveDataPlot-', ),
            # sg.Button('Save raw plot data as...', disabled=True, key='-SaveDataPlot-'),
        ],
    ]

    ArrheniusColumn = [
        [
            sg.Canvas(size=[dim * 100 for dim in plot_size], key='-ArrheniusPlot-')
        ],
        [
            sg.Button('Open as interactive plot', disabled=True, key='-OpenArrheniusPlot-'),
            sg.Save('Save CSV', disabled=True, key='-QuickSaveArrheniusPlotCSV-'),
            sg.Save('Save XLSX', disabled=True, key='-QuickSaveArrheniusPlotXLSX-'),
            sg.InputText(size=(35, 1), enable_events=True, visible=False, key="-SaveArrheniusPlotAs-"),
            sg.FileSaveAs('Save raw plot data as...', disabled=True, file_types=(("CSV file", "*.csv"), ("Excel file", "*.xlsx"),),
                          key='-SaveArrheniusPlot-', ),
            # sg.Button('Save raw plot data as...', disabled=True, key='-SaveArrheniusPlot-'),
        ],
    ]

    OverviewTab = [
        [
            sg.Column(DataPlotColumn),
            sg.VSeperator(),
            sg.Column(ArrheniusColumn),
        ],
    ]

    CurveByCurveParams = [
        [
            sg.Text("Select temperature:"),
        ],
        [
            sg.Listbox(values=[], enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(13, 3),
                       no_scrollbar=True, key="-CurveByCurve_temperature-"),
        ],
        [
            sg.Checkbox("Analyse curve", pad=(5, 0), enable_events=True, default=True, disabled=True, key="-CurveByCurve_visible-"),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Text("Analysis method:"),
        ],
        [
            sg.Radio('Fit exponentials', 'AdvancedAnalysis', pad=(5, 0), disabled=True, default=True, enable_events=True,
                     key="-FitExponentials-"),
        ],
        [
            sg.Text('  ', pad=(5, 0)),
            sg.Text('Exponentials: '),
            sg.Spin([i for i in range(1, max_exponentials + 1)], initial_value=1, pad=((0, 10), 3), size=(3, 1), enable_events=True, disabled=True,
                    key='-number_exponentials-'),
        ],
        [
            sg.Radio('Intersect with 1/e', 'AdvancedAnalysis', pad=(5, 0), disabled=True, enable_events=True,
                     key="-eIntersect-"),
        ],
    ]

    Weights = [
        [
            sg.Text("Weights:"),
        ],
        [
            sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(19, max_exponentials), disabled=True,
                       no_scrollbar=True, key="-AdvancedResults_weights-"),
        ],
    ]

    RelaxationTimes = [
        [
            sg.Text("Relaxation times:"),
        ],
        [
            sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(19, max_exponentials), disabled=True,
                       no_scrollbar=True, key="-AdvancedResults_times-"),
        ],
    ]

    AdvancedResults = [
        [
            sg.Column(Weights, vertical_alignment='top'),
            sg.Column(RelaxationTimes, vertical_alignment='top')
        ],
    ]

    AdvancedParameterColumn = [
        [
            sg.Frame("Curve-by-curve:", CurveByCurveParams, key="-CurveByCurve-"),
            sg.Frame("Results:", AdvancedResults, key="-AdvancedResults-", vertical_alignment='top'),
        ],
        [
            sg.Text('Use relaxation time', tooltip='To assemble the Arrhenius plot. Applies to exponential fits only.'),
            sg.Spin([i for i in range(1, max_exponentials + 1)], initial_value=1, pad=(0, 3), size=(3, 1),
                    enable_events=True, key='-time_idx-', tooltip='To assemble the Arrhenius plot. Applies to exponential fits only.'),
            sg.Text('(high to low)', tooltip='To assemble the Arrhenius plot. Applies to exponential fits only.'),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Button('Apply', key='-CurveByCurve_apply-')
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Save('Save Maxwell data', key='-QuickSaveMaxwellData-'),
            sg.InputText(size=(35, 1), enable_events=True, visible=False, key="-SaveMaxwellDataAs-"),
            sg.FileSaveAs('Save Maxwell data as...',
                          file_types=(("Excel file", "*.xlsx"),),
                          key='-SaveMaxwellData-', ),
        ],
    ]

    GeneralisedMaxwellColumn = [
        [
            sg.Canvas(size=[dim * 100 for dim in plot_size], key='-GeneralisedMaxwellPlot-')
        ],
        [
            sg.Button('Open as interactive plot', disabled=True, key='-OpenMaxwellPlot-'),
            # sg.Save('Save CSV', disabled=True, key='-QuickSaveMaxwellPlotCSV-'),
            # sg.Save('Save XLSX', disabled=True, key='-QuickSaveMaxwellPlotXLSX-'),
            # sg.InputText(size=(35, 1), enable_events=True, visible=False, key="-SaveMaxwellPlotAs-"),
            # sg.FileSaveAs('Save raw plot data as...', disabled=True,
            #               file_types=(("CSV file", "*.csv"), ("Excel file", "*.xlsx"),),
            #               key='-SaveMaxwellPlot-', ),
        ],
    ]

    AdvancedTab = [
        [
            sg.Column(AdvancedParameterColumn, size=(plot_size[0] * 102, plot_size[1] * 100)),
            sg.VSeperator(),
            sg.Column(GeneralisedMaxwellColumn),
        ],
    ]

    Tabs = [
        [
            sg.Tab('Overview', OverviewTab, key="-OverviewTab-"),
            sg.Tab('Advanced', AdvancedTab, key="-AdvancedTab-", visible=False),
        ],
    ]

    layout = [
        [
            sg.Column(InputColumn),
            sg.TabGroup(Tabs)
            # sg.VSeperator(),
            # sg.Column(DataPlotColumn),
            # sg.VSeperator(),
            # sg.Column(ArrheniusColumn),
        ],
    ]

    window = sg.Window("Anton Paar Rheology v" + aprheology.__version__, layout)
    window.Finalize()

    def draw_plot(canvas, plot):
        for child in canvas.winfo_children():
            child.destroy()
        if plot:
            figure_canvas_agg = FigureCanvasTkAgg(plot, canvas)
            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

    def update_overview_plots(experiment):
        draw_plot(window['-DataPlot-'].TKCanvas, experiment.plot(plot_size=plot_size, return_plot=True))
        draw_plot(window['-ArrheniusPlot-'].TKCanvas, experiment.analyse_arrhenius(plot_size=plot_size, show_plot=False, return_plot=True))

    def update_GM_plot(experiment, values):
        if experiment.get_evaluate_flag(values['-CurveByCurve_temperature-'][0]):
            if values['-FitExponentials-']:
                draw_plot(window['-GeneralisedMaxwellPlot-'].TKCanvas,
                          experiment.fit_GM(exponentials=values['-number_exponentials-'],
                                            curve_temp=values['-CurveByCurve_temperature-'][0],
                                            plot_size=plot_size,
                                            return_plot=True))
            if values['-eIntersect-']:
                draw_plot(window['-GeneralisedMaxwellPlot-'].TKCanvas,
                          experiment.plot_SM(temperature=values['-CurveByCurve_temperature-'][0],
                                             plot_size=plot_size,
                                             return_plot=True))
        else:
            draw_plot(window['-GeneralisedMaxwellPlot-'].TKCanvas, None)

    def get_updated_advancedresults(experiment, values):
        if experiment.get_evaluate_flag(values['-CurveByCurve_temperature-'][0]):
            if values['-FitExponentials-']:
                experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_mode_GM'] = True
                weights = list(u'{:.3f} \u00B1 {:.3f}'.format(round(weight, 3), round(weight_err, 3)) for weight, weight_err, time, time_err in experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_GM'])
                times = list(u'{:.3f} \u00B1 {:.3f}'.format(round(time, 3), round(time_err, 3)) for weight, weight_err, time, time_err in experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_GM'])
                # return list(round(elem, 3) for elem in experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_GM'][:,2]), list(round(elem, 3) for elem in experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_GM'][:,2])
                return weights, times
            if values['-eIntersect-']:
                experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_mode_GM'] = False
                return [], [str(round(experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_SM'], 3))]
        return [], []

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-FILE-":
            if not values["-FILE-"]:
                continue
            try:
                window["-T_unit-"].update(aprheology.RelaxationExperiment(values["-FILE-"], None).T_unit)
            except:
                pass
            window["-StressRelaxation-"].update(disabled=False)
            window["-FrequencySweep-"].update(disabled=False)
            window["-T_from_datacolumns_names_last-"].update(disabled=False)
            window["-T_from_curve_header_last_number-"].update(disabled=False)
            window["-T_unit-"].update(disabled=False)
            # window["-tau_mode_interpolate-"].update(disabled=False)
            # window["-tau_mode_closest-"].update(disabled=False)
            # window["-datapoints_discarded-"].update(disabled=False)
            # Gives an error that a wrong state is passed... Do it manually without update:
            window["-datapoints_discarded-"].TKSpinBox['state'] = 'normal'
            window["-OpenFile-"].update(disabled=False)
        if event == "-OpenFile-":
            if values['-T_from_datacolumns_names_last-']:
                get_T_from = 'datacolumns_names_last'
            elif values['-T_from_curve_header_last_number-']:
                get_T_from = 'curve_header_last_number'
            else:
                sg.popup_error('Something went wrong')
                continue
            # if values['-tau_mode_interpolate-']:
            #     tau_mode = 'interpolate_highest'
            # elif values['-tau_mode_closest-']:
            #     tau_mode = 'closest_highest'
            # else:
            #     sg.popup_error('Something went wrong')
            #     continue
            datapoints_discarded = int(values['-datapoints_discarded-']) if values['-datapoints_discarded-'] != 0 else None
            if values['-StressRelaxation-']:
                try:
                    experiment = aprheology.StressRelaxation(filename=values["-FILE-"],
                                                             get_T_from=get_T_from,
                                                             T_unit=values["-T_unit-"],
                                                             datapoints_discarded=datapoints_discarded)
                except:
                    sg.popup_error('Something went wrong, check the input file.')
                    continue
            elif values['-FrequencySweep-']:
                try:
                    experiment = aprheology.FrequencySweep(filename=values["-FILE-"],
                                                           get_T_from=get_T_from,
                                                           T_unit=values["-T_unit-"],
                                                           datapoints_discarded=datapoints_discarded)
                except:
                    sg.popup_error('Something went wrong, check the input file.')
                    continue
            else:
                sg.popup_error('No experiment type selected.')
                continue
            update_overview_plots(experiment)
            window["-normalise_relax_mod-"].update(disabled=False)
            window["-TauModeSingle-"].update(disabled=False)
            window["-TauModeGeneral-"].update(disabled=False)
            window["-Temperatures-"].update(disabled=False)
            temperatures = [curve['T'] for curve in experiment.curves]
            window["-Temperatures-"].update(values=temperatures)
            window["-Temperatures-"].SetValue(temperatures)
            window["-Temperatures-"].set_size(size=(None, len(temperatures)))
            window["-UpdateTemperatures-"].update(disabled=False)
            window['-OpenDataPlot-'].update(disabled=False)
            window['-OpenArrheniusPlot-'].update(disabled=False)
            window['-QuickSaveDataPlotCSV-'].update(disabled=False)
            window['-QuickSaveDataPlotXLSX-'].update(disabled=False)
            window['-SaveDataPlot-'].update(disabled=False)
            window['-QuickSaveArrheniusPlotCSV-'].update(disabled=False)
            window['-QuickSaveArrheniusPlotXLSX-'].update(disabled=False)
            window['-SaveArrheniusPlot-'].update(disabled=False)
            window['-TauModeSingle-'].update(value=True)
            window['-AdvancedTab-'].update(visible=False)
            window["-Temperatures-"].update(disabled=False)
            window["-UpdateTemperatures-"].update(disabled=False)
            window["-CurveByCurve_temperature-"].update(values=temperatures)
            window["-CurveByCurve_temperature-"].set_size(size=(None, len(temperatures)))
        if event == "-normalise_relax_mod-":
            try:
                experiment.normalised_relax_mod = values["-normalise_relax_mod-"]
                update_overview_plots(experiment)
            except:
                pass
        if event == '-TauModeSingle-':
            for curve in experiment.curves:
                curve['tau'] = curve['tau_SM']
                curve['tau_mode_GM'] = False
            update_overview_plots(experiment)
            window['-AdvancedTab-'].update(visible=False)
            window["-Temperatures-"].update(disabled=False)
            window["-UpdateTemperatures-"].update(disabled=False)
        if event == '-TauModeGeneral-':
            window['-AdvancedTab-'].update(visible=True)
            window["-Temperatures-"].update(disabled=True)
            window["-UpdateTemperatures-"].update(disabled=True)
        if event == '-UpdateTemperatures-':
            experiment.set_evaluated_T(T_list=values["-Temperatures-"])
            update_overview_plots(experiment)
        if event == '-OpenDataPlot-':
            experiment.plot(return_plot=False)
        if event == '-OpenArrheniusPlot-':
            experiment.analyse_arrhenius(show_plot=True, return_plot=False)
        if event == '-QuickSaveDataPlotCSV-':
            try:
                experiment.export_plot_data(excel=False)
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-QuickSaveArrheniusPlotCSV-':
            try:
                experiment.export_arrhenius_data(excel=False)
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-QuickSaveDataPlotXLSX-':
            try:
                experiment.export_plot_data(excel=True)
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-QuickSaveArrheniusPlotXLSX-':
            try:
                experiment.export_arrhenius_data(excel=True)
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-SaveDataPlotAs-':
            extension = re.sub('\A.*\.([^.]*)\Z', '\\1', values['-SaveDataPlotAs-'])
            try:
                experiment.export_plot_data(filename=values['-SaveDataPlotAs-'], excel=(extension == 'xlsx'))
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-SaveArrheniusPlotAs-':
            extension = re.sub('\A.*\.([^.]*)\Z', '\\1', values['-SaveArrheniusPlotAs-'])
            try:
                experiment.export_arrhenius_data(filename=values['-SaveArrheniusPlotAs-'], excel=(extension == 'xlsx'))
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == '-CurveByCurve_temperature-':
            evaluate_flag = experiment.get_evaluate_flag(values['-CurveByCurve_temperature-'][0])
            window["-CurveByCurve_visible-"].update(disabled=False,
                                                    value=evaluate_flag)
            window["-FitExponentials-"].update(disabled=not evaluate_flag)
            window["-eIntersect-"].update(disabled=not evaluate_flag)
            try:
                if experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_mode_GM']:
                    window["-FitExponentials-"].update(value = True)
                    values["-FitExponentials-"] = True
                    values["-eIntersect-"] = False
                else:
                    window["-eIntersect-"].update(value=True)
                    values["-FitExponentials-"] = False
                    values["-eIntersect-"] = True
                number_exponentials = len(experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_GM'])
                window["-number_exponentials-"].update(disabled=not evaluate_flag or not values['-FitExponentials-'],
                                                       value=number_exponentials)
                values["-number_exponentials-"] = number_exponentials
            except:
                window["-FitExponentials-"].update(value=True)
                values["-FitExponentials-"] = True
                values["-eIntersect-"] = False
                window["-number_exponentials-"].update(disabled=not evaluate_flag or not values['-FitExponentials-'])
                # experiment.curves[experiment.get_curve_idx(values['-CurveByCurve_temperature-'][0])]['tau_mode_GM'] = True
            window["-AdvancedResults_weights-"].update(disabled=not evaluate_flag)
            window["-AdvancedResults_times-"].update(disabled=not evaluate_flag)
            window["-OpenMaxwellPlot-"].update(disabled=not evaluate_flag)
            update_GM_plot(experiment, values)
            weights, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
        if event == '-CurveByCurve_visible-':
            window["-FitExponentials-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-number_exponentials-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-eIntersect-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-AdvancedResults_weights-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-AdvancedResults_times-"].update(disabled=not values['-CurveByCurve_visible-'])
            window["-OpenMaxwellPlot-"].update(disabled=not values['-CurveByCurve_visible-'])
            experiment.set_evaluate_flag(values['-CurveByCurve_temperature-'][0], values['-CurveByCurve_visible-'])
            update_GM_plot(experiment, values)
            weights, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
        if event == "-FitExponentials-":
            window["-number_exponentials-"].update(disabled=False)
            update_GM_plot(experiment, values)
            weights, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
        if event == "-eIntersect-":
            window["-number_exponentials-"].update(disabled=True)
            update_GM_plot(experiment, values)
            weights, times = get_updated_advancedresults(experiment, values)
            window["-AdvancedResults_weights-"].update(values=weights)
            window["-AdvancedResults_times-"].update(values=times)
        if event == "-number_exponentials-":
            try:
                update_GM_plot(experiment, values)
                weights, times = get_updated_advancedresults(experiment, values)
                window["-AdvancedResults_weights-"].update(values=weights)
                window["-AdvancedResults_times-"].update(values=times)
            except:
                sg.popup_error('Select a temperature first')
        # if event == "-time_idx-":
        #     get_updated_relaxation_times(experiment, values)
        if event == "-CurveByCurve_apply-":
            experiment.set_arrhenius_times(values['-time_idx-'] - 1)
            update_overview_plots(experiment)
        if event == "-OpenMaxwellPlot-":
            if values['-FitExponentials-']:
                experiment.fit_GM(exponentials=values['-number_exponentials-'],
                                  curve_temp=values['-CurveByCurve_temperature-'][0],
                                  return_plot=False)
            if values['-eIntersect-']:
                experiment.plot_SM(temperature=values['-CurveByCurve_temperature-'][0],
                                   return_plot=False)
        if event == "-QuickSaveMaxwellData-":
            try:
                experiment.export_maxwell_data()
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")
        if event == "-SaveMaxwellDataAs-":
            try:
                experiment.export_maxwell_data(filename=values['-SaveMaxwellDataAs-'])
            except:
                sg.popup_error("Failed to save.\nCheck that the file isn't opened in another program.")




    window.close()