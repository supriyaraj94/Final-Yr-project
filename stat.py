import plotly.plotly as py
import plotly.graph_objs as go
py.sign_in('shibani', 'k0l604lvym')

y1 = [0.00809502601624,
0.0180449485779,
0.340131282806,
1.25386190414,
243.087193012]
x1 = ['5','6','7','8','9']
# Create a simple chart..
trace = go.Bar(x = x1, y = y1)
data = [trace]
layout = go.Layout(title='Time vs no_of_digits', width=800, height=640)
fig = go.Figure(data=data, layout=layout)
py.image.save_as(fig, filename='sieve.png')
