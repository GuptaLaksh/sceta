import math
from IPython.display import display, HTML

rows = []

def initialize(rationumholder):
    def ratio(sc1, sc2, ct1, ct2):
        sc_ratio = (round(sc1/sc2, 3))
        sc_ratio_err = round(sc_ratio*(math.sqrt((1/sc1)+(1/sc2))), 3)

        ct_ratio = round(ct1/ct2, 3)
        ct_ratio_err = round(ct_ratio*(math.sqrt(2)/10), 3)

        if sc_ratio > ct_ratio:
            exc_def = (1 - (ct_ratio/sc_ratio))*100
            note = "Population A is in excess by "
        else:
            exc_def = (1 - (sc_ratio/ct_ratio))*100
            note = "Population B is in excess by "

        return sc_ratio, sc_ratio_err, ct_ratio, ct_ratio_err, exc_def, note

    html_table = """
    <table border="1" style="border-collapse: collapse; width: 100%;">
        <tr>
            <th style="text-align: center;">Pop A</th>
            <th style="text-align: center;">Pop B</th>
            <th style="text-align: center;">Star Count</th>
            <th style="text-align: center;">Crossing Time</th>
            <th style="text-align: center;">Note</th>
        </tr>
    """

    for i in range(len(rationumholder)):
        scr, sce, ctr, cte, exc_def, note = ratio(*rationumholder[i])
        exc_def = round(exc_def, 2)
        
        pop_a_str = f"{rationumholder[i][0]}, {rationumholder[i][2]}"
        pop_b_str = f"{rationumholder[i][1]}, {round(rationumholder[i][3], 3)}"
        star_count_str = f"{scr:.3f} &plusmn; {sce:.3f}"
        crossing_time_str = f"{ctr:.3f} &plusmn; {cte:.3f}"
        note_str = f"{note}{exc_def}%"
        
        html_table += f"""
        <tr>
            <td style="text-align: right;">{pop_a_str}</td>
            <td style="text-align: right;">{pop_b_str}</td>
            <td style="text-align: center;">{star_count_str}</td>
            <td style="text-align: center;">{crossing_time_str}</td>
            <td style="text-align: left;">{note_str}</td>
        </tr>
        """

    html_table += "</table>"

    display(HTML(html_table))

    # return locals()
