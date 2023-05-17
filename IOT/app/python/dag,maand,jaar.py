from bokeh.layouts import column
from bokeh.plotting import figure, output_file, save, show
from bokeh.models import FactorRange, Button
from bokeh.io import show
from bokeh.models import CustomJS, DatePicker




# create a new plot with a title and axis labels
p = figure(
    title="verbruik in kWh", 
    x_axis_label="x", 
    y_axis_label="y",
    max_width=500,
    height=250,)

output_file(filename="jaar_bar_graph.html", title="verbruik in kWh per jaar")


factors = [
    ("Q1", "jan"), ("Q1", "feb"), ("Q1", "mar"),
    ("Q2", "apr"), ("Q2", "may"), ("Q2", "jun"),
    ("Q3", "jul"), ("Q3", "aug"), ("Q3", "sep"),
    ("Q4", "oct"), ("Q4", "nov"), ("Q4", "dec"),
]

p = figure(x_range=FactorRange(*factors), height=350,
           toolbar_location=None, tools="")

x = [ 100, 120, 160, 90, 112, 89, 120, 130, 140, 154, 120, 160 ]
p.vbar(x=factors, top=x, width=0.9, alpha=0.5)

p.line(x=["Q1", "Q2", "Q3", "Q4"], y=[126, 97, 130, 144], color="red", line_width=2)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None


#  style the headline
p.title.text_font_size = "25px"
p.title.align = "right"
p.title.background_fill_color = "orange"
p.title.text_color = "white"


# Display the plot and buttons
p.toolbar.logo = None
p.toolbar_location = None
save(p)
# show the results