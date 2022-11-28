import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px


ecom_sales = pd.read_csv('/Users/pbo_a/Documents/Python/datasets/data.csv', encoding= 'unicode_escape')
ecom_sales["InvoiceDate"] = ecom_sales["InvoiceDate"].str[:9]

for_lineplot = ecom_sales.groupby(['InvoiceDate','Country'])['UnitPrice'].agg('sum').reset_index(name='Total Sales ($)')

line_graph = px.line(
  # Set the appropriate DataFrame and title
  data_frame=for_lineplot, title='Total Sales by Country and Month', 
  # Set the x and y arguments
  x='InvoiceDate', y='Total Sales ($)',
  # Ensure a separate line per country
  color="Country")

for_barplot = ecom_sales.groupby(['Country'])['UnitPrice'].agg('sum').reset_index(name='Total Sales ($)')
max_country = for_barplot.sort_values(by='Total Sales ($)', ascending=False).loc[0]['Country']

bar_graph = px.bar(data_frame=for_barplot,
    x="Total Sales ($)", y='Country',
    orientation="h", title="Total Sales by Country")

# Create the Dash app
app = dash.Dash(__name__)

# Set up the layout with a single graph

app.layout = html.Div(
    children = [
        # add a H1
        html.H1("Sales by Country & Over Time"),
        # Add both graphs
        html.Div(dcc.Graph(id="line_graph", figure=line_graph)),
        html.Div(dcc.Graph(id="bar_graph", figure=bar_graph)),
        # Add the H3
        html.H3(f'The largest country by sales was {max_country}')
    ]
)

# Set the app to run in development mode
if __name__ == '__main__':
    app.run_server(debug=True)