import numpy as np
import Enorms
import Tools
import BestTransform
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

### @Author Tomasz Szczepanski
###
### Creates a dashboard that visualizes the e-norms method.
###
### Allowes users to select a plateau from datasets and returns statistical analysis from the selected sets.

coords = []
lines = []
plots = []
s_result = ""

def draw(s_title, b_lat, a_measurements_clean, fig, ax):
    global coords, lines, plots, s_result
    coords = []
    lines = []
    plots = []
    s_result = ""

    a_set_historical = a_measurements_clean
    a_set_historical.sort()

    bt = BestTransform.BestTransform(a_set_historical)
    a_set_historical_transformed = bt.getBestTransformedSet()

    e = Enorms.Enorms(a_set_historical_transformed, 13)

    fig.suptitle("e-norms dashboard", fontsize=16, fontweight='bold')
    fig.set_size_inches(12, 8)
    s_headline = "historical e-norms"
    ax.set_title(s_headline)

    i_max_delta = 0
    i_offset = round(len(a_set_historical_transformed)*0.1)
    i = i_offset
    while i < len(a_set_historical_transformed)-i_offset:
        if i_max_delta < e.get_deltas()[i]:
            i_max_delta = e.get_deltas()[i]
        i += 1
    i_scale_average = (((a_set_historical_transformed[len(a_set_historical_transformed)-1]*1.1)-(a_set_historical_transformed[0]*0.9))*0.30)/i_max_delta
    i_max_average = 0
    i_offset = round(len(a_set_historical_transformed)*0.1)
    i = i_offset
    while i < len(a_set_historical_transformed)-i_offset:
        if i_max_average < e.get_deltas_moving_average()[i]:
            i_max_average = e.get_deltas_moving_average()[i]
        i += 1
    i_scale_deltas_average = (((a_set_historical_transformed[len(a_set_historical_transformed)-1]*1.1)-(a_set_historical_transformed[0]*0.9))*0.10)/i_max_average
    l_hist, = ax.plot(a_set_historical_transformed, color="#4567c6", linewidth=2.0)
    l_hist_av, = ax.plot(e.get_training_moving_average(), visible=False, color="#4567c6", linewidth=2.0)
    l_d, = ax.plot(np.add(np.multiply(e.get_deltas(), i_scale_average), a_set_historical_transformed[0]*0.9), alpha=0.7, color="red")
    l_d_av, = ax.plot(np.add(np.multiply(e.get_deltas_moving_average(), i_scale_deltas_average), a_set_historical_transformed[0]*0.9), alpha=0.9, color="#0DFFDA")
    xp = np.linspace(0, len(a_set_historical_transformed), len(a_set_historical_transformed)*2)
    l_p3, = ax.plot(xp, e.get_p3()(xp), alpha=0.9, visible=False, color="orange")

    ax.set_ylim(a_set_historical_transformed[0]*0.9, (2*a_set_historical_transformed[int(len(a_set_historical_transformed)/2)] - a_set_historical_transformed[0])*1.1)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    a_lines = [(l_hist, "hist. data + avg."), (l_d, "derivatives"), (l_d_av, "d. average"), (l_p3, "p3"), (l_hist, ""), (l_hist, "blind mode")]
    a_line_colors = [l[0].get_color() for l in a_lines]

    # Make checkbuttons with all plotted lines with correct visibility
    rax = fig.add_axes([0.01, 0.4, 0.14, 0.20])
    check = CheckButtons(
        ax=rax,
        labels=[l[1] for l in a_lines],
        actives=[l[0].get_visible() for l in a_lines]
    )
    [rec.set_facecolor(a_line_colors[i]) for i, rec in enumerate(check.rectangles)]
    check.rectangles[4].set_visible(False)
    check.lines[4][0].set_visible(False)
    check.lines[4][1].set_visible(False)

    def callback(label):
        for l in a_lines:
            if label == l[1]:
                if label == "hist. data + avg.":
                    b_visible = l[0].get_visible()
                    l[0].set_visible(not b_visible)
                    l_hist_av.set_visible(b_visible)
                elif label == "blind mode":
                    b_scramble = ax.get_xaxis().get_visible()
                    s_headline = "historical e-norms"
                    if b_scramble:
                        ax.get_xaxis().set_visible(False)
                        ax.get_yaxis().set_visible(False)
                    else:
                        s_headline += " - " + s_title
                        ax.get_xaxis().set_visible(True)
                        ax.get_yaxis().set_visible(True)
                    ax.set_title(s_headline)
                elif label == "":
                    check.lines[4][0].set_visible(False)
                    check.lines[4][1].set_visible(False)
                else:
                    l[0].set_visible(not l[0].get_visible())
        plt.draw()

    check.on_clicked(callback)

    def onclick(event, coord_preset=None):
        global coords, lines, plots, s_result, rf_controll
        if coord_preset is not None or event.inaxes in [ax]:
            ix, iy = None, None
            if coord_preset is not None:
                ix, iy = coord_preset, 0
            else:
                ix, iy = event.xdata, event.ydata
            if not ix is None and not iy is None and ix >= 0 and ix < len(a_set_historical_transformed):
                coords.append(round(ix))
                if len(coords) == 1:
                    if len(lines) == 2:
                        lines[0].set_visible(False)
                        lines[1].set_visible(False)
                        plots[0].set_visible(False)
                    lines = []
                    plots = []
                    lines.append(ax.axvline(x=coords[0], color="black", linewidth=1.0, linestyle="--"))
                if len(coords) == 2:
                    lines.append(ax.axvline(x=coords[1], color="black", linewidth=1.0, linestyle="--"))
                    coords.sort()
                    a_set_plateau = a_set_historical[coords[0]:coords[1]]
                    if len(a_set_plateau) > 1:
                        u, sd, t_rf, i_median, q1, q3, iqr = Tools.get_statistics(a_set_historical_transformed[coords[0]:coords[1]])
                        
                        # mean +/- 2 * sd calcullated from the transformed data and then re-transformet to original data
                        rf2sd = bt.getReverseTransformValCompute(t_rf[1]) if b_lat else bt.getReverseTransformValCompute(t_rf[0]) 
                        rf2sd_percent = len(a_set_historical) - Tools.get_n_less_than_from_set(a_set_historical, rf2sd) if b_lat else Tools.get_n_less_than_from_set(a_set_historical, rf2sd)
                        rf2sd_percent = rf2sd_percent/len(a_set_historical)*100
                        rf25sd = bt.getReverseTransformValCompute(u+2.5*sd) if b_lat else bt.getReverseTransformValCompute(u-2.5*sd)
                        rf25sd_percent = len(a_set_historical) - Tools.get_n_less_than_from_set(a_set_historical, rf25sd) if b_lat else Tools.get_n_less_than_from_set(a_set_historical, rf25sd)
                        rf25sd_percent = rf25sd_percent/len(a_set_historical)*100
                        rf3sd = bt.getReverseTransformValCompute(u+3*sd) if b_lat else bt.getReverseTransformValCompute(u-3*sd)
                        rf3sd_percent = len(a_set_historical) - Tools.get_n_less_than_from_set(a_set_historical, rf3sd) if b_lat else Tools.get_n_less_than_from_set(a_set_historical, rf3sd)
                        rf3sd_percent = rf3sd_percent/len(a_set_historical)*100
                        
                        s_result = str(u)+","+str(sd)+","+str(i_median)+","+str(iqr)+","+str(len(a_set_plateau))+","+bt.getBestTransformedSetLabel()+","+str(rf2sd)+","+str(rf2sd_percent)+","+str(rf25sd)+","+str(rf25sd_percent)+","+str(rf3sd)+","+str(rf3sd_percent)+","+str(coords[0])+","+str(coords[1])
                        
                        s_pathology_enorms = "pathology "+("above " if b_lat else "below ")+"{:.2f}".format(rf2sd)
                        ax.set_xlabel(s_pathology_enorms)
                    line, = ax.plot(coords, [a_set_historical_transformed[coords[0]], a_set_historical_transformed[coords[1]]], 'ko-', color='#61FF0D')
                    plots.append(line)

                    coords = []
                plt.draw()

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    plt.subplots_adjust(left=0.200, bottom=0.073, right=0.988, top=0.908, wspace=0.345, hspace=0.267)

    plt.show()
    
    if s_result == "":
        s_result = ",,,,,,,,,,,,,,"
    
    return s_result
