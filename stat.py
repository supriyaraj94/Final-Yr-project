import plotly.plotly as py
import plotly.graph_objs as go
py.sign_in('shibani', 'k0l604lvym')

y1 = [57.0287401676,
111.396743059,
80.9745569229,
48.0354728699,
39.3146169186,
29.3861558437]
x1 = [1,2,3,4,5,6]
# Create a simple chart..
trace = go.Bar(x = x1, y = y1)
data = [trace]
layout = go.Layout(title='4 Bits', width=800, height=640)
fig = go.Figure(data=data, layout=layout)
py.image.save_as(fig, filename='twenty_bits.png')
