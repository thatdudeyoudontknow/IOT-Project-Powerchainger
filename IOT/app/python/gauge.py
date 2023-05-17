import plotly.graph_objects as go
import plotly.express as px

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 1.2, 
    title = {'text': "verbruik in kWh", 'font': {'size': 24}},
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {
        'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "green"},
        'bar': {'color': "green"},
        'bgcolor': "rgba(0, 0, 0, 0)",
        'borderwidth': 2,
        'bordercolor': "gray",
        }))

fig.update_layout(paper_bgcolor = "rgba(0, 0, 0, 0)", font = {'color': "darkblue", 'family': "Arial"})

fig.write_html("gauge.html")
# fig.show()

