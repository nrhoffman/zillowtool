import pandas as pd
import re

def csvreader(config, psql):
    url_list = {}
    urls = config['FILES']
    for url in urls:
        raw_df = pd.read_csv(config['VALUES']['ZillowUrl'] + config['FILES'][url])
        df_rows = len(raw_df.index)
        date_columns = [col for col in raw_df.columns if re.match(r'^\d{4}-\d{2}-\d{2}$', col)]
        for region, group in raw_df.groupby("RegionName"):
            count = psql.getrowcount(url)
            print("Row {} of {}.".format(count, df_rows))
            for date in date_columns:
                if group["RegionType"].iloc[0] == "msa":
                    city, state = region.split(", ")
                    region_date = region + "_" + date
                    psql.insertdata(url, region_date, city, state, date, str(group[date].values[0]))
    return url_list