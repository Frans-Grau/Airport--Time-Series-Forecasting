### Imports
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, page_container

### Initialize
app = dash.Dash(__name__,use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

### Style 
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H1("Menu", className="display-4"),
        html.Hr(),
        html.P(
            "Choose an option", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page['name'],className='ns-2')
                        # dbc.Button(page['name'], href = page['relative_path'],className='me-1'),
                    ],
                    href = page['path'],
                    active = 'exact',
                )
                for page in dash.page_registry.values()
            ],
            
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# content = dash.page_container
content = html.Div(id="page-content", style=CONTENT_STYLE)

### Initialize
app.layout = html.Div([dcc.Location(id="url", pathname ='/'), sidebar, content])

### Callbacks
@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname"))
def render_page_content(pathname):
    if pathname.startswith("/"):
        return page_container
    else:
        return html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ],
            className="p-3 bg-light rounded-3",
        )

### Run the app
if __name__ == "__main__":
    app.run_server(debug=True)