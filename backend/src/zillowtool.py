import configparser
import connection
import csvreader
import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt

config = configparser.ConfigParser()
config.read('./backend/config/config.cfg')

psql = connection.Connection(config, config["VALUES"]["CreateTables"])

# csvreader.csvreader(config, psql)

temp_df = psql.readdata("OH", "Cincinnati")

g = sb.FacetGrid(temp_df, col_wrap=4, height=4, col='type', sharex=True, sharey=False) 
g.map(sb.lineplot, "date", "value")    
g.set_titles("{col_name}")
g.set_axis_labels("date", "value")
g.add_legend()

plt.show()