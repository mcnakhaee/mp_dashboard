from shiny import App, ui, render
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

# Create some sample data
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Score": [85, 90, 78, 92]
})


# Function to generate plot as base64 image
def plot_to_base64():
    fig, ax = plt.subplots()
    ax.plot(df["Name"], df["Score"], marker='o', color='blue')
    ax.set_title("Scores of Individuals")

    # Convert plot to PNG image
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return f"data:image/png;base64,{img_base64}"


# Define UI
app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav("Overview", ui.h3("Welcome to the Overview Tab"), ui.p("This is the overview of the app")),
        ui.nav("Plot", ui.output_image("plot_img")),
        ui.nav("Table", ui.output_table("table"))
    )
)


# Define server logic
def server(input, output, session):
    @output
    @render.image
    def plot_img():
        return plot_to_base64()

    @output
    @render.table
    def table():
        return df


# Create app
app = App(app_ui, server)

# Run the app
app.run()