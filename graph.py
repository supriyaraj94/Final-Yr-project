import plotly.plotly as py
import plotly.graph_objs as go
import sys
a = long( sys.argv[1] )
b = long( sys.argv[2] )
c = long( sys.argv[3] )
d = long( sys.argv[4] )
l = [a,b]
m = [c,d]

N = 500

# Create a trace
def plotit(l,m):
    trace0 = go.Scatter(
        x = l,
        y = [5,5],
        name = 'Genome pair',
        mode = 'markers',
        marker = dict(
            size = 10,
            color = 'rgba(152, 0, 0, .8)',
            line = dict(
                width = 2,
                color = 'rgb(0, 0, 0)'
            )
        )
    )

    trace1 = go.Scatter(
        x = m,
        y = [5,5],
        name = 'Prime factors',
        mode = 'markers',
        marker = dict(
            size = 10,
            color = 'rgba(255, 182, 193, .9)',
            line = dict(
                width = 2,
            )
        )
    )

    data = [trace0, trace1]

    layout = dict(title = 'Styled Scatter',
                yaxis = dict(zeroline = False),
                xaxis = dict(zeroline = False)
                )

    fig = dict(data=data, layout=layout)
    py.image.save_as(fig, filename='a-simple-plot.png')
plotit(l,m)

