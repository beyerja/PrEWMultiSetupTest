""" Functions that creat summary plots for one setup.
"""

import matplotlib.pyplot as plt
import numpy as np

# Local modules
import Analysis.CovMatrixCalc as CMC
import IO.SysHelp as IOSH
import Plotting.ParSymbolMapping as PPSM

def plot_parameter(ax, res_summary, p):
  """ Create the summary plot for the single parameter of index p.
  """
  p_avg = res_summary.par_avg[p]
  p_min = res_summary.par_min[p]
  p_max = res_summary.par_max[p]
  
  p_unc_clc = res_summary.unc_vec_calc[p] # Calculated uncerainty
  p_unc_fit = res_summary.unc_vec_avg[p] # Uncertainty average from fits
  
  # x-axis minimum and maximum
  x_min = p_min - 0.1*(p_avg-p_min)
  x_max = p_max + 0.1*(p_max-p_avg)
  
  # Create a histogram for this parameter
  h_entries, h_edges, _ = ax.hist(res_summary.par_vals.T[p], range=(x_min,x_max), bins=10, histtype='step', color='black', label="Fit results")
  ax.set_xlabel("Fit result")
  ax.set_ylabel("#Fits")
  
  # Plot poissonian errorbars
  bin_centers = 0.5 * (h_edges[:-1] + h_edges[1:])
  ax.errorbar(bin_centers, h_entries, yerr=np.sqrt(h_entries), color='black', fmt='none')
  
  # Plot mean, standard deviation and average uncertainty
  y_lims = ax.get_ylim() # Keep y-axis limits constant
  ax.plot([p_avg,p_avg], [0,y_lims[1]],color='red', label="Mean of fits")
  ax.plot([p_avg-p_unc_clc,p_avg-p_unc_clc], [0,y_lims[1]],color='green', label="Calc. unc.")
  ax.plot([p_avg+p_unc_clc,p_avg+p_unc_clc], [0,y_lims[1]],color='green')
  ax.plot([p_avg-p_unc_fit,p_avg-p_unc_fit], [0,y_lims[1]],color='magenta', label="Avg. fit unc.")
  ax.plot([p_avg+p_unc_fit,p_avg+p_unc_fit], [0,y_lims[1]],color='magenta')
  ax.set_ylim(y_lims) # Keep y-axis limits constant
  
  # Add legend
  ax.legend(title=res_summary.par_names[p])
  
def plot_parameters(res_summary, output_dir, extensions=["pdf","png"]):
  """ Create the summary plots for the all individual parameters.
  """
  n_pars = len(res_summary.par_names)
    
  for p in range(n_pars):
    fig, ax = plt.subplots(figsize=(8, 6.5),tight_layout=True)
    plot_parameter(ax,res_summary,p)
    for ext in extensions:
      IOSH.create_dir("{}/{}".format(output_dir,ext))
      fig.savefig("{}/{}/hist_{}.{}".format(output_dir,ext,res_summary.par_names[p],ext))
    plt.close(fig)
    
def plot_cor_matrix(cor_matrix, par_names, h_name, output_dir, write_values,
                    extensions=["pdf","png"]):
  """ Plot the correlation matrix of a single setup run.
  """
  # First remove parameters that were not used
  cor_matrix, par_mask = CMC.clean_cor_mat(cor_matrix)
  par_names = par_names[par_mask]
  
  # Create figure for plots and adjust height and width
  n_pars = len(par_names)
  fig, ax = plt.subplots(figsize=np.array([8, 6.5])+0.45 * n_pars)

  # Plot a 2D color plot (sharp, no interpolations, using PRGn color map)
  im_cor = ax.imshow(cor_matrix,interpolation='none',cmap='PRGn')
  cb_cor = fig.colorbar(im_cor, ax=ax) # Show what the colors mean
  im_cor.set_clim(-1, 1); # Correlations are between -1 and +1
  
  # Write the values on the plot if requested
  if write_values:
    h_name += "_wValues"
    w_ax = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).width * fig.dpi
    value_fs = w_ax/n_pars/4
    for (j,i),label in np.ndenumerate(np.around(cor_matrix,decimals=1)):
      ax.text(i,j,label,ha='center',va='center',fontsize=value_fs)

  # We want to show all ticks...
  ax.set_xticks(np.arange(n_pars))
  ax.set_yticks(np.arange(n_pars))
  # ... and label them with the respective list entries
  par_symbols = PPSM.names_to_symbols(par_names)
  ax.set_xticklabels(par_symbols)
  ax.set_yticklabels(par_symbols)

  # Rotate the tick labels and set their alignment.
  plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
           rotation_mode="anchor")
  plt.setp(ax.get_yticklabels(), rotation=22.5)

  ax.set_title("Average correlation matrix")
  fig.tight_layout()
  for ext in extensions:
    IOSH.create_dir("{}/{}".format(output_dir,ext))
    fig.savefig("{}/{}/{}.{}".format(output_dir,ext,h_name,ext))
  plt.close(fig)

def plot_cor_matrix_avg(res_summary, output_dir, write_values=False, 
                        extensions=["pdf","png"]):
  """ Plot the correlation matrix of a single setup run, calculated by averaging
      over the correlation matrices of all fits.
  """
  plot_cor_matrix(res_summary.cor_mat_avg, res_summary.par_names, 
                  "hist_cor_avg", output_dir, write_values, extensions)
    
def plot_cor_matrix_calc(res_summary, output_dir, write_values=False,
                         extensions=["pdf","png"]):
  """ Plot the correlation matrix of a single setup run, calculated from the
      final fit result points.
  """
  plot_cor_matrix(res_summary.cor_mat_calc, res_summary.par_names, 
                  "hist_cor_calc", output_dir, write_values, extensions)

def plot_nll_ndf(res_summary, output_dir, extensions=["pdf","png"]):
  """ Plot the negative log likelihood (/ degrees of freedom) for a single setup 
      run.
  """
  ndf = res_summary.ndf
  norm_nlls = res_summary.nll/ndf
  norm_nll_avg = np.average(norm_nlls)
  nll_min = np.amin(norm_nlls) # Smallest chi^2/ndof found
  nll_max = np.amax(norm_nlls) # Largest chi^2/ndof found

  # x-axis minimum and maximum
  x_min = nll_min - 0.1*(norm_nll_avg-nll_min) 
  x_max = nll_max + 0.1*(nll_max-norm_nll_avg)

  # Plot histogram of all found chi^2 values
  fig, ax = plt.subplots(figsize=(7.5, 5),tight_layout=True)
  hist = ax.hist(norm_nlls, range=(x_min,x_max), bins=15, histtype='step', color='black', label="results")
  ax.set_xlabel(r"$-2*\log(L)/$ndf")
  ax.set_ylabel("#Fits")
  ax.set_ylim([0,1.1*np.amax(hist[0])])

  # Plot errorbars
  bin_centers = 0.5 * (hist[1][:-1] + hist[1][1:])
  ax.errorbar(bin_centers, hist[0], yerr=np.sqrt(hist[0]), color='black', fmt='none')

  # Plot mean chi^2 of all toy fits
  y_lims = ax.get_ylim()
  ax.plot([norm_nll_avg,norm_nll_avg], [0,y_lims[1]],color='red', label="result mean")
  ax.set_ylim(y_lims)

  # Draw legend
  ndof_str = r"$ndf$ = " + str(ndf)
  ax.legend(title=ndof_str)

  for ext in extensions:
    IOSH.create_dir("{}/{}".format(output_dir,ext))
    fig.savefig("{}/{}/hist_nll_ndf.{}".format(output_dir,ext,ext))
  plt.close(fig)
  
def plot_cov_status(res_summary, output_dir, extensions=["pdf","png"]):
  """ Plot the covariance matrix status of a single setup run.
  """
  # Plot the status histogram
  fig, ax = plt.subplots(figsize=(7.5, 7),tight_layout=True)
  hist = ax.hist(res_summary.cov_status, range=(-1.5,3.5), bins=5, histtype='step', color='black')
  ax.set_title("Cov. matr. calc. status")
  ax.set_ylabel("#Fits")
  ax.set_yscale('log') # Log scale to see when individuals go wrong
  ax.set_ylim(0.9, 1.2*np.amax(hist[0]))

  # x axis labels with possible outcomes
  ax_labels = ["PrEW output failure", "not calculated", "approximated", "made pos def", "accurate"]
  ax.set_xticks(np.arange(-1, len(ax_labels)-1))
  ax.set_xticklabels(ax_labels)

  # Rotate the tick labels and set their alignment.
  plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

  for ext in extensions:
    IOSH.create_dir("{}/{}".format(output_dir,ext))
    fig.savefig("{}/{}/hist_cov_status.{}".format(output_dir,ext,ext))
  plt.close(fig)
  
def plot_min_status(res_summary, output_dir, extensions=["pdf","png"]):
  """ Plot the minimizer status of a single setup run.
  """
  fig, ax = plt.subplots(figsize=(9, 7),tight_layout=True)
  hist = ax.hist(res_summary.min_status, range=(-1.5,6.5), bins=8, histtype='step', color='black')
  ax.set_title("Minimizer status")
  ax.set_ylabel("#Fits")
  ax.set_yscale('log')
  ax.set_ylim(0.9, 1.2*np.amax(hist[0]))

  # Write x-axis labels that tell problem exactly (corresponding to value from -1 to 6)
  min_stat_ax_labels = ["PrEW output failure", "All good", "Cov-matr. made pos. def.", "Hesse not valid", "EDM above max", "Call limit reached", "Cov-matr. not pos. def.", "UNEXPECTED"]
  ax.set_xticks(np.arange(-1, len(min_stat_ax_labels)-1))
  ax.set_xticklabels(min_stat_ax_labels)

  # Rotate the tick labels and set their alignment.
  plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

  for ext in extensions:
    IOSH.create_dir("{}/{}".format(output_dir,ext))
    fig.savefig("{}/{}/hist_min_status.{}".format(output_dir,ext,ext))
  plt.close(fig)
  
def plot_fit_calls(res_summary, output_dir, extensions=["pdf","png"]):
  """ Plot the number of calls and iterations that the fit made.
  """
  # Create the figure with the histograms
  fig, ax = plt.subplots(figsize=(7, 5),tight_layout=True)
  hist_calls = ax.hist(res_summary.fct_calls, bins=15, histtype='step', color='blue', label="#FctCalls")
  hist_iters = ax.hist(res_summary.n_iters, bins=15, histtype='step', color='red', label="#Iterations")
  ax.set_xlabel("N")
  ax.set_ylabel("#Fits")
  ax.set_ylim([0, 1.2*np.amax([np.amax(hist_calls[0]),np.amax(hist_iters[0])])])

  # Add a legend 
  ax.legend()

  for ext in extensions:
    IOSH.create_dir("{}/{}".format(output_dir,ext))
    fig.savefig("{}/{}/hist_n_stats.{}".format(output_dir,ext,ext))
  plt.close(fig)
  
def plot_res_summary(res_summary, output_dir, extensions=["pdf","png"]):
  """ Create all summary and check plots for the given result summary.
  """
  plot_parameters(res_summary, output_dir, extensions)
  plot_cor_matrix_avg(res_summary, output_dir, extensions=extensions)
  plot_cor_matrix_avg(res_summary, output_dir, write_values=True, extensions=extensions)
  plot_cor_matrix_calc(res_summary, output_dir, extensions=extensions)
  plot_nll_ndf(res_summary, output_dir, extensions)
  plot_cov_status(res_summary, output_dir, extensions)
  plot_min_status(res_summary, output_dir, extensions)
  plot_fit_calls(res_summary, output_dir, extensions)
  