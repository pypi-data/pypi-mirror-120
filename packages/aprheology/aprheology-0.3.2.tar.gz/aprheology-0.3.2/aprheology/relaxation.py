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

import pandas as pd
import numpy as np
import re
import math
import sys
from operator import itemgetter, attrgetter
from scipy import interpolate, constants
from scipy.optimize import curve_fit
from scipy.special import gamma
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib as mpl
import itertools
# import aprheology

# fit_curve models: 'single', 'stretched single', 'generalised liquid', 'stretched generalised liquid'

def SM(t, tau):
    return np.exp(-t / tau)

def GM_1(t, a1, tau1):
    return a1 * np.exp(-t / tau1)

def GM_2(t, a1, tau1, a2, tau2):
    return a1 * np.exp(-t / tau1) + a2 * np.exp(-t / tau2)

def GM_3(t, a1, tau1, a2, tau2, a3, tau3):
    return a1 * np.exp(-t / tau1) + a2 * np.exp(-t / tau2) + a3 * np.exp(-t / tau3)

def GM_4(t, a1, tau1, a2, tau2, a3, tau3, a4, tau4):
    return a1 * np.exp(-t / tau1) + a2 * np.exp(-t / tau2) + a3 * np.exp(-t / tau3) + a4 * np.exp(-t / tau4)

def GM_5(t, a1, tau1, a2, tau2, a3, tau3, a4, tau4, a5, tau5):
    return a1 * np.exp(-t / tau1) + a2 * np.exp(-t / tau2) + a3 * np.exp(-t / tau3) + a4 * np.exp(-t / tau4) + a5 * np.exp(-t / tau5)

def SSM(t, b, tau):
    return np.exp(-(t / tau) ** b)

def SGM_1(t, a1, b1, tau1):
    return a1 * np.exp(-(t / tau1) ** b1)

def SGM_2(t, a1, b1, tau1, a2, b2, tau2):
    return a1 * np.exp(-(t / tau1) ** b1) + a2 * np.exp(-(t / tau2) ** b2)

def SGM_3(t, a1, b1, tau1, a2, b2, tau2, a3, b3, tau3):
    return a1 * np.exp(-(t / tau1) ** b1) + a2 * np.exp(-(t / tau2) ** b2) + a3 * np.exp(-(t / tau3) ** b3)

def SGM_4(t, a1, b1, tau1, a2, b2, tau2, a3, b3, tau3, a4, b4, tau4):
    return a1 * np.exp(-(t / tau1) ** b1) + a2 * np.exp(-(t / tau2) ** b2) + a3 * np.exp(-(t / tau3) ** b3) + a4 * np.exp(-(t / tau4) ** b4)

def SGM_5(t, a1, b1, tau1, a2, b2, tau2, a3, b3, tau3, a4, b4, tau4, a5, b5, tau5):
    return a1 * np.exp(-(t / tau1) ** b1) + a2 * np.exp(-(t / tau2) ** b2) + a3 * np.exp(-(t / tau3) ** b3) + a4 * np.exp(-(t / tau4) ** b4) + a5 * np.exp(-(t / tau5) ** b5)


GM_functions = [GM_1, GM_2, GM_3, GM_4, GM_5, ]
SGM_functions = [SGM_1, SGM_2, SGM_3, SGM_4, SGM_5, ]


class RelaxationExperiment:
    def __init__(self,
                 filename: str,
                 datacolumns_names: list = None,
                 get_T_from: str = 'datacolumns_names_last',
                 T_unit=None,
                 ):

        if get_T_from != 'datacolumns_names_last' and get_T_from != 'curve_header_last_number':
            sys.exit('At the moment no other methods available to extract temperature apart from default')

        file = open(filename, 'r').read()
        self.filename = re.sub("\A(.*)\.([^.]*)\Z", "\\1", filename)
        # self.extension = re.sub("\A(.*)\.([^.]*)\Z", "\\2", filename)
        # basename = re.sub(re.sub("/", "", originals_dir) + "\\\\", "", re.sub("\A(.*)\.([^.]*)\Z", "\\1", filename))
        file_curves = re.split('Result:', re.sub('\s*\n\s*', '@@@', re.sub('\0', '', file)))
        file_header = file_curves.pop(0)
        self.project = re.sub('^.*Project:\t([^@]*)@@@.*$', '\\1', file_header)
        self.test_title = re.sub('^.*Test:\t([^@]*)@@@.*$', '\\1', file_header)

        self.datacolumns_names = datacolumns_names
        try: # Will raise error if no curves are actually detected in the file
            self.units = re.split('\t', re.sub('[\[\]]', '', re.sub('^.*Interval data:\t[^@]*@@@([^@]*)@@@.*$', '\\1', file_curves[0])))
        except:
            self.units = None

        if datacolumns_names is not None:
            curves = []
            for idx, curve in enumerate(file_curves):
                columns = re.split('\t', re.sub('^.*Interval data:\t([^@]*)@@@.*$', '\\1', curve))
                # data = [[float(number) for number in re.split('\t', line)] for line in re.split('@@@', re.sub(',', '.', re.sub('^.*Interval data:\t[^@]*@@@[^@]*@@@(.*)(@@@)+$', '\\1', curve)))]
                # data = pd.DataFrame(data, columns=columns)[retainedColumns]
                data = [re.split('\t', line) for line in
                        re.split('@@@', re.sub(',', '.', re.sub('^.*Interval data:\t[^@]*@@@[^@]*@@@(.*)(@@@)+$', '\\1', curve)))]
                data = pd.DataFrame(data, columns=columns)[datacolumns_names].apply(pd.to_numeric, errors='coerce')
                data.dropna(axis=0, how='any', inplace=True)
                if get_T_from == 'datacolumns_names_last':
                    temperature = round(data[datacolumns_names[-1]].mean())
                    data.drop(columns=[datacolumns_names[-1]], inplace=True)
                elif get_T_from == 'curve_header_last_number':
                    temperature = int(re.sub('^[^@]*\D(\d+)[^@]*@@@.*$', '\\1', curve))
                data.reset_index(drop=True, inplace=True)
                curves.append({'data': data,
                               'T': temperature,
                               'evaluate': True,
                               })
            self.curves = sorted(curves, key=itemgetter('T'), reverse=True)
        else:
            self.curves = None
            print('Parameter datacolumns_names not passed to RelaxationExperiment, curves not read.')
        if T_unit is not None:
            self.T_unit = T_unit
        else:
            if '°C' in self.units:
                self.T_unit = '°C'
            else:
                sys.exit('Not sure what the temperature unit is, please provide T_unit.')

    def set_evaluated_T(self, T_min: float = None, T_max: float = None, T_range=None, T_list=None):
        if T_min == T_max == T_range == T_list is None:
            return
        if T_list is not None:
            for curve in self.curves:
                curve['evaluate'] = True if curve['T'] in T_list else False
            if hasattr(self, 'plot_data'):
                delattr(self, 'plot_data')
            return
        if T_range is not None:
            T_min = min(T_range)
            T_max = max(T_range)
        if T_min is None or T_max is None:
            sys.exit('Could not resolve the temperatures to be evaluated. Check parameters T_min, T_max, T_range or T_list.')
        else:
            for curve in self.curves:
                curve['evaluate'] = True if T_min <= curve['T'] <= T_max else False
            if hasattr(self, 'plot_data'):
                delattr(self, 'plot_data')
            return

    def set_evaluate_flag(self, temperature, evaluate = True):
        for curve in self.curves:
            if curve['T'] == temperature:
                curve['evaluate'] = evaluate
        if hasattr(self, 'plot_data'):
            delattr(self, 'plot_data')

    def get_evaluate_flag(self, temperature):
        for curve in self.curves:
            if curve['T'] == temperature:
                return curve['evaluate']

    def get_curve_idx(self, temperature):
        try:
            return [idx for idx, curve in enumerate(self.curves) if curve['T'] == temperature][0]
        except:
            return None

    def get_plot_data(self):
        if hasattr(self, 'normalised_relax_mod'):
            normalise = self.normalised_relax_mod
        else:
            normalise = False
        self.plot_data = pd.DataFrame(columns=[[],[]])
        for curve in self.curves:
            if curve['evaluate']:
                tmp = curve['data'].copy(deep=True)
                if normalise:
                    for column in tmp.columns[1:]:
                        tmp[column] /= tmp[column].max()
                tmp.columns = [np.full(len(tmp.columns), curve['T']), list(tmp.columns)]
                self.plot_data = self.plot_data.join(tmp, how='outer')
        return self.plot_data

    def export_plot_data(self, filename=None, excel=False):
        # if not hasattr(self, 'plot_data'):
        self.get_plot_data()
        if excel:
            if filename is not None:
                self.plot_data.to_excel(filename)
            else:
                self.plot_data.to_excel(self.filename + '_relaxationplot.xlsx')
        else:
            if filename is not None:
                self.plot_data.to_csv(filename, index=False)
            else:
                self.plot_data.to_csv(self.filename + '_relaxationplot.csv', index=False)

    @staticmethod
    def get_Ea(T, tau, T_unit='°C', show_plot=False, return_plot=False, plot_size: list = None, plot_dpi: float = None, return_plot_data=False):
        '''

        :param T:
        :param tau:
        :param T_unit:
        :param return_plot_data:
        :type T: list or np.ndarray
        :type tau: list or np.ndarray
        :type T_unit: str
        :type return_plot_data: bool
        :return: [Ea, std.err., R2, [ndarray(1/T), ndarray(ln(tau)), ndarray(predicted ln(tau))]]
        :rtype: list
        '''

        if type(T) == list:
            T = np.array(T)
        if T.size:
            # Only perform all calculations when a non-empty dataset is passed. Else return None values and an empty graph
            ln_tau = np.array([math.log(elem) for elem in tau])

            if T_unit == '°C':
                T = T + 273.15
            elif T_unit == 'K':
                pass
            else:
                sys.exit('Invalid temperature unit passed to determineEa.')
            T_inv = 1 / T
            # sklearn method does not allow to calculate std err on the linear regression
            # statsmodels method
            X = sm.add_constant(T_inv, prepend=False)
            olsResult = sm.OLS(ln_tau, X).fit()
            slope = list(zip(olsResult.params, olsResult.bse))[0]
            # intercept = list(zip(olsResult.params, olsResult.bse))[1]
            R2 = olsResult.rsquared
            ln_tau_pred = olsResult.predict()

            if show_plot or return_plot:
                fig_Ea = plt.figure(figsize=plot_size, dpi=plot_dpi)
                ax = fig_Ea.add_subplot(111)
                ax.scatter(1000 * T_inv, ln_tau)
                ax.plot(1000 * T_inv, ln_tau_pred, 'r--')
                plt.title('Arrhenius plot')
                plt.xlabel(r'1000/T (K$^{-1}$)')
                plt.ylabel(r'ln($\tau$)')
                plt.text((3 * (1000 * T_inv).min() + (1000 * T_inv).max()) * .25,
                         (ln_tau_pred.min() + 3 * ln_tau_pred.max()) * .25,
                         r'$\mathregular{E_a}$ = ' + str(round(slope[0] * constants.R / 1000, 2)) + r' $\pm$ ' + str(
                             round(slope[1] * constants.R / 1000, 2)) + r' kJ$\,$mol$^{-1}$' + '\n' + r'R$^2$ = ' + str(
                             round(R2, 4)),
                         horizontalalignment='center', verticalalignment='bottom', )
                if show_plot:
                    plt.show()

            plt.close()
            results = [elem * constants.R for elem in slope] + [R2]
            if return_plot_data:
                results.append([T_inv, ln_tau, ln_tau_pred])
            if return_plot:
                results.append(fig_Ea)

            return results
        else:
            if show_plot or return_plot:
                fig_Ea = plt.figure(figsize=plot_size, dpi=plot_dpi)
                ax = fig_Ea.add_subplot(111)
                # ax.scatter(1000 * T_inv, ln_tau)
                # ax.plot(1000 * T_inv, ln_tau_pred, 'r--')
                plt.title('Arrhenius plot')
                plt.xlabel(r'1000/T (K$^{-1}$)')
                plt.ylabel(r'ln($\tau$)')
                # plt.text((3 * (1000 * T_inv).min() + (1000 * T_inv).max()) * .25,
                #          (ln_tau_pred.min() + 3 * ln_tau_pred.max()) * .25,
                #          r'$\mathregular{E_a}$ = ' + str(round(slope[0] * constants.R / 1000, 2)) + r' $\pm$ ' + str(
                #              round(slope[1] * constants.R / 1000, 2)) + r' kJ$\,$mol$^{-1}$' + '\n' + r'R$^2$ = ' + str(
                #              round(R2, 4)),
                #          horizontalalignment='center', verticalalignment='bottom', )
                if show_plot:
                    plt.show()

            plt.close()
            results = [None, None, None]
            if return_plot_data:
                results.append([None, None, None])
            if return_plot:
                results.append(fig_Ea)

            return results

    def analyse_arrhenius(self, show_plot=True, return_plot=False, plot_size: list = None, plot_dpi: float = None):
        self.arrhenius = pd.DataFrame([[curve['T'], curve['tau']] for curve in self.curves if curve['evaluate']], columns=['T', 'tau']).dropna(axis=0, how='any')
        # self.arrhenius = self.arrhenius.dropna(axis=0, how='any', inplace=True)
        self.arrhenius.reset_index(drop=True, inplace=True)

        tmp = self.get_Ea(T=self.arrhenius['T'].to_numpy(),
                          tau=self.arrhenius['tau'].to_numpy(),
                          T_unit=self.T_unit,
                          show_plot=show_plot,
                          return_plot=return_plot,
                          plot_size=plot_size,
                          plot_dpi=plot_dpi,
                          return_plot_data=True)

        self.Ea = tmp[0:3]
        self.arrhenius = self.arrhenius.join(pd.DataFrame(tmp[3], index=['T_inv', 'ln_tau', 'ln_tau_pred']).T)
        if return_plot:
            self.arrhenius_plot = tmp[-1]
            return self.arrhenius_plot
        else:
            self.arrhenius_plot = None

    def export_arrhenius_data(self, filename=None, excel=False):
        if not hasattr(self, 'Ea'):
            self.analyse_arrhenius(show_plot=False)
        if excel:
            if filename is not None:
                self.arrhenius.to_excel(filename, index=False)
            else:
                self.arrhenius.to_excel(self.filename + '_arrheniusplot.xlsx', index=False)
        else:
            if filename is not None:
                self.arrhenius.to_csv(filename, index=False)
            else:
                self.arrhenius.to_csv(self.filename + '_arrheniusplot.csv', index=False)

class StressRelaxation(RelaxationExperiment):
    '''
    @staticmethod
    def get_tau_SM(time, normRelaxMod):
        # Gives the highest time value where normRelaxMod passes the 1/e threshold.
        if type(time) == list:
            time = np.array(time)
        if type(normRelaxMod) == list:
            normRelaxMod = np.array(normRelaxMod)
        e = np.full(len(time), 1 / math.e)
        intersections = np.argwhere(np.diff(np.sign(normRelaxMod - e))).flatten()
        if len(intersections) == 0:
            return None
        f = interpolate.interp1d(normRelaxMod[intersections[-1]:intersections[-1] + 2],
                                 time[intersections[-1]:intersections[-1] + 2])
        return float(f(1 / math.e))

    @staticmethod
    def get_tau_GM(time, relaxMod, exponentials, return_relaxMod_pred=False):
        if type(time) == list:
            time = np.array(time)
        if type(relaxMod) == list:
            relaxMod = np.array(relaxMod)
        popt, pcov = curve_fit(f=GM_functions[exponentials - 1], xdata=time, ydata=relaxMod, bounds=(0, np.inf))
        perr = np.sqrt(np.diag(pcov))
        params = np.concatenate((popt, perr)).reshape(2, -1).T.flatten().reshape(-1, 4)
        if return_relaxMod_pred:
            return [params[params[:, 2].argsort()[::-1]],
                    GM_functions[exponentials - 1](time, *params[:, [0, 2]].flatten())]
        else:
            return params[params[:, 2].argsort()[::-1]]
    '''

    @staticmethod
    def get_tau_intersect(time, normRelaxMod, intersect_value=None):
        # Gives the highest time value where normRelaxMod passes a certain intersect_value, by default 1/e.
        if type(time) == list:
            time = np.array(time)
        if type(normRelaxMod) == list:
            normRelaxMod = np.array(normRelaxMod)
        if intersect_value is None:
            intersect_value = 1 / math.e
        intersect = np.full(len(time), intersect_value)
        intersections = np.argwhere(np.diff(np.sign(normRelaxMod - intersect))).flatten()
        if len(intersections) == 0:
            return None
        f = interpolate.interp1d(normRelaxMod[intersections[-1]:intersections[-1] + 2],
                                 time[intersections[-1]:intersections[-1] + 2])
        return float(f(intersect_value))

    @staticmethod
    def get_tau_fit(time, relaxMod, model, exponentials: int = 1, tau_guess: float = None, return_relaxMod_pred=False):
        if type(time) == list:
            time = np.array(time)
        if type(relaxMod) == list:
            relaxMod = np.array(relaxMod)
        if model == 'single':
            function = SM
            bounds = (0, np.inf)
            p0 = None if tau_guess is None else [tau_guess]
        elif model == 'stretched single':
            function = SSM
            bounds = (0, (1, np.inf))
            p0 = None if tau_guess is None else [1, tau_guess]
        elif model == 'generalised liquid':
            function = GM_functions[exponentials - 1]
            bounds = (0, np.inf)
            p0 = None if tau_guess is None else list(np.full([exponentials, 2], [1 / exponentials, tau_guess]).flatten())
        elif model == 'stretched generalised liquid':
            function = SGM_functions[exponentials - 1]
            bounds = (0, tuple(np.full([exponentials, 3], [np.inf, 1, np.inf]).flatten()))
            p0 = None if tau_guess is None else list(np.full([exponentials, 3], [1 / exponentials, 1, tau_guess]).flatten())
        else:
            sys.exit('Please provide a valid model to get_tau_fit.')
        # params_opt, params_cov = curve_fit(f=function, xdata=time, ydata=relaxMod, bounds=bounds)
        # params_opt, params_cov = curve_fit(f=function, xdata=time, ydata=relaxMod, bounds=bounds, p0=p0)
        # params_opt, params_cov = curve_fit(f=function, xdata=time, ydata=relaxMod, p0=[0.5, 1, 216, 0.5, 1, 216], bounds=(0, (np.inf, 1.0, np.inf, np.inf, 1.0, np.inf)))
        try:
            params_opt, params_cov = curve_fit(f=function, xdata=time, ydata=relaxMod, bounds=bounds, p0=p0)
        except:
            if model == 'stretched generalised liquid':
                function = GM_functions[exponentials - 1]
                bounds = (0, np.inf)
                p0 = None if tau_guess is None else list(np.full([exponentials, 2], [1 / exponentials, tau_guess]).flatten())
                params_opt, params_cov = curve_fit(f=function, xdata=time, ydata=relaxMod, bounds=bounds, p0=p0)
                params_opt = params_opt.reshape(-1, 2)
                function = SGM_functions[exponentials - 1]
                bounds = (0, tuple(np.full([exponentials, 3], [np.inf, 1, np.inf]).flatten()))
                p0 = np.concatenate((params_opt.T[0], np.full(len(params_opt), 1), params_opt.T[1])).reshape((3,-1)).T.flatten()
                params_opt, params_cov = curve_fit(f=function, xdata=time, ydata=relaxMod, bounds=bounds, p0=p0)
        params_err = np.sqrt(np.diag(params_cov))
        relaxMod_pred = function(time, *params_opt)

        if model == 'single':
            params = np.concatenate((params_opt, params_err)).reshape(2, -1).T.flatten().reshape(-1, 2)
        elif model == 'stretched single':
            params = np.concatenate((params_opt, params_err)).reshape(2, -1).T.flatten().reshape(-1, 4)
            params[:, 3] = np.sqrt((params[:, 3] / params[:, 2]) ** 2 + (params[:, 1] / params[:, 0]) ** 2)
            params[:, 2] = params[:, 2] / params[:, 0] * gamma(1 / params[:, 0])
            params[:, 3] *= params[:, 2]
        elif model == 'generalised liquid':
            params = np.concatenate((params_opt, params_err)).reshape(2, -1).T.flatten().reshape(-1, 4)
            params = params[params[:, 2].argsort()[::-1]]
        elif model == 'stretched generalised liquid':
            params = np.concatenate((params_opt, params_err)).reshape(2, -1).T.flatten().reshape(-1, 6)
            params[:, 5] = np.sqrt((params[:, 5] / params[:, 4]) ** 2 + (params[:, 3] / params[:, 2]) ** 2)
            params[:, 4] = params[:, 4] / params[:, 2] * gamma(1 / params[:, 2])
            params[:, 5] *= params[:, 4]
            params = params[params[:, 4].argsort()[::-1]]

        if return_relaxMod_pred:
            return [params,
                    relaxMod_pred]
        else:
            return params

    def __init__(self,
                 filename: str,
                 datacolumns_names=None,
                 get_T_from: str = 'datacolumns_names_last',
                 T_unit=None,
                 T_range=None,
                 datapoints_discarded=None,
                 normalise_relax_mod=True,
                 ):

        if datacolumns_names is None:
            if get_T_from == 'datacolumns_names_last':
                datacolumns_names = ['Time', 'Relaxation Modulus', 'Temperature']
            else:
                datacolumns_names = ['Time', 'Relaxation Modulus']

        super().__init__(filename, datacolumns_names, get_T_from, T_unit)
        self.set_evaluated_T(T_range=T_range)

        if datapoints_discarded is not None:
            if type(datapoints_discarded) == int:
                datapoints_discarded = np.full(len(self.curves), datapoints_discarded)
            elif len(datapoints_discarded) != len(self.curves):
                sys.exit('The length of the list of datapoints that should be discarded (' + str(
                    len(datapoints_discarded)) + ') is different from the number of curves to be analysed (' + str(
                    len(self.curves)) + ').')

        for idx, curve in enumerate(self.curves):
            if datapoints_discarded is not None:
                curve['data'].drop(range(0, datapoints_discarded[idx]), inplace=True) # detele certain parts from range, meant to calculate tau
                curve['data'].reset_index(drop=True, inplace=True)
            self.normalised_relax_mod = True if normalise_relax_mod else False
            # curve['relaxMod_max'] = curve['data'][datacolumns_names[1]].max()
            # curve['data'][datacolumns_names[1]] /= curve['data'][datacolumns_names[1]].max()  # normalisation
            curve['tau_intersect'] = self.get_tau_intersect(curve['data'][datacolumns_names[0]].to_numpy(),
                                                            (curve['data'][datacolumns_names[1]] /
                                                            curve['data'][datacolumns_names[1]].max()).to_numpy())
            curve['tau_mode_fit'] = False
            curve['tau'] = curve['tau_intersect']

    def plot(self, plot_size: list = None, plot_dpi: float = None, return_plot=False):
        # if not hasattr(self, 'plot_data'):
        self.get_plot_data()

        fig_relax = plt.figure(figsize=plot_size, dpi=plot_dpi)
        ax = fig_relax.add_subplot(111)
        for temp in np.flip(np.unique([col[0] for col in self.plot_data])):
            ax.plot(self.plot_data[temp, self.datacolumns_names[0]],
                    self.plot_data[temp, self.datacolumns_names[1]],
                    label=str(temp) + '$\,$' + self.T_unit)
        if self.normalised_relax_mod:
            tmp_array = np.array([self.plot_data[x, self.datacolumns_names[0]] for x in np.unique([col[0] for col in self.plot_data])])
            x_range = np.arange(np.nanmin(tmp_array), np.nanmax(tmp_array), (np.nanmax(tmp_array) - np.nanmin(tmp_array)) / 10)
            ax.plot(x_range, np.full(len(x_range), 1 / math.e), '--', color='grey')
            plt.ylim(-0.05, 1.05)
            plt.ylabel(r'Normalised relaxation modulus')
        else:
            plt.ylabel(r'Relaxation modulus (Pa)')
        ax.set_xscale('log')
        ax.legend()
        plt.title('Stress relaxation')
        plt.xlabel(r'Time (s)')
        if return_plot:
            plt.close()
            return fig_relax
        else:
            plt.show()

    def plot_SM(self, temperature, plot_size: list = None, plot_dpi: float = None, return_plot=False):
        curve_idx = self.get_curve_idx(temperature)
        fig_SM = plt.figure(figsize=plot_size, dpi=plot_dpi)
        ax = fig_SM.add_subplot(111)
        ax.scatter(self.curves[curve_idx]['data'][self.datacolumns_names[0]],
                   self.curves[curve_idx]['data'][self.datacolumns_names[1]] /
                   self.curves[curve_idx]['data'][self.datacolumns_names[1]].max(),
                   s=10)
        ax.plot(self.curves[curve_idx]['data'][self.datacolumns_names[0]],
                SM(self.curves[curve_idx]['data'][self.datacolumns_names[0]].to_numpy(),
                   self.curves[curve_idx]['tau_intersect']),
                'r-')
        plt.ylim(-0.05, 1.05)
        plt.ylabel(r'Normalised relaxation modulus')
        ax.set_xscale('log')
        # ax.legend()
        plt.title(r'Single Maxwell (intersect with $e^{-1}$)')
        plt.xlabel(r'Time (s)')
        if return_plot:
            plt.close()
            return fig_SM
        else:
            plt.show()

    # def fit_GM(self, exponentials: int, curve_idx=None, curve_temp=None, return_plot=False, plot_size: list = None, plot_dpi: float = None):
    #     if curve_idx is None and curve_temp is None or curve_idx is not None and curve_temp is not None:
    #         sys.exit('Please pass an either index or a temperature to the function fit_GM.')
    #     if curve_idx is None and curve_temp is not None:
    #         curve_idx = self.get_curve_idx(curve_temp)
    #         if curve_idx is None:
    #             sys.exit('Invalid temperature passed to fit_GM.')
    #     self.curves[curve_idx]['tau_GM'], self.curves[curve_idx]['relaxMod_GM'] = \
    #         self.get_tau_GM(self.curves[curve_idx]['data'][self.datacolumns_names[0]].to_numpy(),
    #                         (self.curves[curve_idx]['data'][self.datacolumns_names[1]] /
    #                          self.curves[curve_idx]['data'][self.datacolumns_names[1]].max()).to_numpy(),
    #                         exponentials=exponentials,
    #                         return_relaxMod_pred=True)
    #     self.curves[curve_idx]['tau_mode_GM'] = True
    #
    #     fig_GM = plt.figure(figsize=plot_size, dpi=plot_dpi)
    #     ax = fig_GM.add_subplot(111)
    #     ax.scatter(self.curves[curve_idx]['data'][self.datacolumns_names[0]],
    #                self.curves[curve_idx]['data'][self.datacolumns_names[1]] /
    #                self.curves[curve_idx]['data'][self.datacolumns_names[1]].max(),
    #                s=10)
    #     ax.plot(self.curves[curve_idx]['data'][self.datacolumns_names[0]],
    #             self.curves[curve_idx]['relaxMod_GM'],
    #             'r-')
    #     ax.set_xscale('log')
    #     plt.title('Generalised Maxwell fit')
    #     plt.xlabel(r'Time (s)')
    #     # if self.normalised_relax_mod:
    #     plt.ylim(-0.05, 1.05)
    #     plt.ylabel(r'Normalised relaxation modulus')
    #     # else:
    #     #     plt.ylabel(r'Relaxation modulus (Pa)')
    #
    #     if return_plot:
    #         plt.close()
    #         return fig_GM
    #     else:
    #         plt.show()

    def fit_curve(self, model: str = None, exponentials: int = 1, curve_idx=None, curve_temp=None, return_plot=False, plot_size: list = None, plot_dpi: float = None):
        if curve_idx is None and curve_temp is None or curve_idx is not None and curve_temp is not None:
            sys.exit('Please pass an either index or a temperature to the function fit_curve.')
        if curve_idx is None and curve_temp is not None:
            curve_idx = self.get_curve_idx(curve_temp)
            if curve_idx is None:
                sys.exit('Invalid temperature passed to fit_curve.')
        if model is None:
            try:
                model = self.curves[curve_idx]['tau_fit_model']
            except:
                sys.exit('Please pass a model to fit_curve.')
        self.curves[curve_idx]['tau_fit'], self.curves[curve_idx]['relaxMod_fit'] = \
            self.get_tau_fit(self.curves[curve_idx]['data'][self.datacolumns_names[0]].to_numpy(),
                             (self.curves[curve_idx]['data'][self.datacolumns_names[1]] /
                             self.curves[curve_idx]['data'][self.datacolumns_names[1]].max()).to_numpy(),
                             model=model,
                             exponentials=exponentials,
                             tau_guess=self.curves[curve_idx]['tau_intersect'],
                             return_relaxMod_pred=True)
        self.curves[curve_idx]['tau_fit_model'] = model
        self.curves[curve_idx]['tau_mode_fit'] = True

        fig_fit = plt.figure(figsize=plot_size, dpi=plot_dpi)
        ax = fig_fit.add_subplot(111)
        ax.scatter(self.curves[curve_idx]['data'][self.datacolumns_names[0]],
                   self.curves[curve_idx]['data'][self.datacolumns_names[1]] /
                   self.curves[curve_idx]['data'][self.datacolumns_names[1]].max(),
                   s=10)
        ax.plot(self.curves[curve_idx]['data'][self.datacolumns_names[0]],
                self.curves[curve_idx]['relaxMod_fit'],
                'r-')
        ax.set_xscale('log')
        title = 'Curve fit '
        if model == 'single':
            title += '(single Maxwell)'
        elif model == 'stretched single':
            title += '(stretched single Maxwell)'
        elif model == 'generalised liquid':
            title += '(generalised Maxwell, {} elements)'.format(exponentials)
        elif model == 'stretched generalised liquid':
            title += '(stretched gen. Maxwell, {} elements)'.format(exponentials)
        plt.title(title)
        plt.xlabel(r'Time (s)')
        # if self.normalised_relax_mod:
        plt.ylim(-0.05, 1.05)
        plt.ylabel(r'Normalised relaxation modulus')
        # else:
        #     plt.ylabel(r'Relaxation modulus (Pa)')

        if return_plot:
            plt.close()
            return fig_fit
        else:
            plt.show()

    def set_arrhenius_times(self, fitted_time_index=0):
        for curve in self.curves:
            if curve['tau_mode_fit']:
                try:
                    curve['tau'] = curve['tau_fit'][fitted_time_index, -2]
                except:
                    curve['tau'] = None
            else:
                curve['tau'] = curve['tau_intersect']

    def get_maxwell_data(self):
        maxwell_data_tau = pd.DataFrame(columns=[[], []])
        maxwell_data_fit = pd.DataFrame(columns=[[], []])
        for curve in self.curves:
            if curve['evaluate']:
                fit = curve['data'].copy(deep=True)
                fit[self.datacolumns_names[1]] /= fit[self.datacolumns_names[1]].max()
                if curve['tau_mode_fit']:
                    if curve['tau_fit_model'] == 'single':
                        model = 'single Maxwell'
                        tau = pd.DataFrame(curve['tau_fit'], columns=[np.full(2, curve['T']),
                                                                      ['tau', 'tau_error']])
                    elif curve['tau_fit_model'] == 'stretched single':
                        model = 'stretched single Maxwell'
                        tau = pd.DataFrame(curve['tau_fit'], columns=[np.full(4, curve['T']),
                                                                      ['stretch', 'stretch_error',
                                                                       'tau', 'tau_error']])
                    elif curve['tau_fit_model'] == 'generalised liquid':
                        model = 'generalised Maxwell, {} elements'.format(len(curve['tau_fit']))
                        tau = pd.DataFrame(curve['tau_fit'], columns=[np.full(4, curve['T']),
                                                                      ['weight', 'weight_error',
                                                                       'tau', 'tau_error']])
                    elif curve['tau_fit_model'] == 'stretched generalised liquid':
                        model = 'stretched gen. Maxwell, {} elements'.format(len(curve['tau_fit']))
                        tau = pd.DataFrame(curve['tau_fit'], columns=[np.full(6, curve['T']),
                                                                      ['weight', 'weight_error',
                                                                       'stretch', 'stretch_error',
                                                                       'tau', 'tau_error']])
                    fit['Model fit ({})'.format(model)] = curve['relaxMod_fit']
                    if curve['tau_fit_model'] == 'generalised liquid':
                        for idx, t in enumerate(curve['tau_fit'][::-1, -2]):
                            fit['Element ' + str(idx + 1)] = SM(fit.Time.to_numpy(), t)
                    elif curve['tau_fit_model'] == 'stretched generalised liquid':
                        for idx, [b, t] in enumerate(curve['tau_fit'][::-1, [2, -2]]):
                            # t = t * b / math.gamma(1 / b)
                            fit['Element ' + str(idx + 1)] = SSM(fit.Time.to_numpy(), b, t * b / math.gamma(1 / b))
                else:
                    tau = pd.DataFrame([[curve['tau_intersect']]], columns=[[curve['T']], ['tau']])
                    fit['Single Maxwell'] = SM(fit.Time.to_numpy(), curve['tau_intersect'])
                maxwell_data_tau = maxwell_data_tau.join(tau, how='outer')
                fit.columns = [np.full(len(fit.columns), curve['T']), list(fit.columns)]
                maxwell_data_fit = maxwell_data_fit.join(fit, how='outer')

        self.maxwell_data = {'tau': maxwell_data_tau,
                             'fit': maxwell_data_fit}
        return self.maxwell_data

    def export_maxwell_data(self, filename=None):
        # if not hasattr(self, 'maxwell_data'):
        self.get_maxwell_data()
        if filename is None:
            filename = self.filename + '_maxwelldata.xlsx'
        with pd.ExcelWriter(filename) as excel:
            self.maxwell_data['tau'].to_excel(excel, sheet_name='Relaxation times')
            for temperature in sorted(self.maxwell_data['fit'].columns.levels[0], reverse=True):
                self.maxwell_data['fit'][temperature].to_excel(excel, sheet_name='Curve at ' + str(temperature) + self.T_unit, index=False)
            # excel.close()


class FrequencySweep(RelaxationExperiment):
    @staticmethod
    def get_tau(ang_freq, g_storage, g_loss):
        # Gives the time value where normRelaxMod passes the 1/e threshold. More specifically the last timepoint before
        # it drops below 1/e (or multiple in case of noisy data), which is not necessarily the timepoint closest to the
        # intersection
        if type(ang_freq) == list:
            ang_freq = np.array(ang_freq)
        if type(g_storage) == list:
            g_storage = np.array(g_storage)
        if type(g_loss) == list:
            g_loss = np.array(g_loss)
        g_diff = g_storage - g_loss
        intersections = np.argwhere(np.diff(np.sign(g_diff))).flatten()
        if len(intersections) == 0:
            return None

        tau_inv = []
        for intersection in intersections:
            f = interpolate.interp1d(g_diff[intersection:intersection + 2],
                                     ang_freq[intersection:intersection + 2])
            tau_inv.append(float(f(0)))

        return (1 / np.array(tau_inv)).max()

    def __init__(self,
                 filename: str,
                 datacolumns_names=None,
                 get_T_from: str = 'datacolumns_names_last',
                 T_unit=None,
                 T_range=None,
                 datapoints_discarded=None,
                 ):

        if datacolumns_names is None:
            if get_T_from == 'datacolumns_names_last':
                datacolumns_names = ['Angular Frequency', 'Storage Modulus', 'Loss Modulus', 'Temperature']
            else:
                datacolumns_names = ['Angular Frequency', 'Storage Modulus', 'Loss Modulus']

        super().__init__(filename, datacolumns_names, get_T_from, T_unit)
        self.set_evaluated_T(T_range=T_range)

        if datapoints_discarded is not None:
            if type(datapoints_discarded) == int:
                datapoints_discarded = np.full(len(self.curves), datapoints_discarded)
            elif len(datapoints_discarded) != len(self.curves):
                sys.exit('The length of the list of datapoints that should be discarded (' + str(
                    len(datapoints_discarded)) + ') is different from the number of curves to be analysed (' + str(
                    len(self.curves)) + ').')

        #check that the angular frequency is in rad/s, otherwise recalculation is needed
        if 'rad/s' not in self.units and 'Hz' in self.units:
            print('Assuming the frequency is given in Hz, please export as rad/s next time.')
            for curve in self.curves:
                curve['data'][datacolumns_names[0]] *= 2 * constants.pi

        for idx, curve in enumerate(self.curves):
            if datapoints_discarded is not None:
                curve['data'].drop(range(0, datapoints_discarded[idx]), inplace=True) # detele certain parts from range, meant to calculate tau
                curve['data'].reset_index(drop=True, inplace=True)
            # curve['data'][datacolumns_names[1]] /= curve['data'][datacolumns_names[1]].max()  # no normalisation
            curve['tau'] = self.get_tau(curve['data'][datacolumns_names[0]].to_numpy(),
                                        curve['data'][datacolumns_names[1]].to_numpy(),
                                        curve['data'][datacolumns_names[2]].to_numpy())

    def plot(self, plot_size: list = None, plot_dpi: float = None, return_plot=False):
        # if not hasattr(self, 'plot_data'):
        self.get_plot_data()

        mpl_default = mpl.rcParams['axes.prop_cycle']
        mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=itertools.chain(
            *zip([color['color'] for color in mpl_default], [color['color'] for color in mpl_default])))

        fig_relax = plt.figure(figsize=plot_size, dpi=plot_dpi)
        ax = fig_relax.add_subplot(111)
        for temp in np.flip(np.unique([col[0] for col in self.plot_data])):
            ax.plot(self.plot_data[temp, self.datacolumns_names[0]], self.plot_data[temp, self.datacolumns_names[1]],
                    '-', label=str(temp) + "$\,$°C (G')")
            ax.plot(self.plot_data[temp, self.datacolumns_names[0]], self.plot_data[temp, self.datacolumns_names[2]],
                    '--', label=str(temp) + '$\,$°C (G")')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        plt.title('Frequency sweep')
        plt.xlabel(r'Frequency (rad$\cdot$s$^{-1}$)')
        plt.ylabel(r'Modulus (Pa)')
        mpl.rcParams['axes.prop_cycle'] = mpl_default
        if return_plot:
            plt.close()
            return fig_relax
        else:
            plt.show()
