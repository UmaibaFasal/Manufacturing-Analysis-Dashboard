from Main import get_data1, get_data2, get_data3, get_data4, get_data5, get_data6, get_data7, get_data8, get_data9  
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
#Fetch Data
df1 = get_data1()
df2 = get_data2()   
df3 = get_data3()
df4 = get_data4()
df5 = get_data5()
df6 = get_data6()
df7 = get_data7()
df8 = get_data8()
df9 = get_data9()
#Connect to mySQL
username = "root"
password = quote_plus("hAmd@2021")
host = "localhost"
port = "3306"  # MySQL default port
database = "Manufacturing_Analytics"
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")
#Load DataFrame into MySQL
table_name1 = "production_orders"
df1.to_sql(table_name1, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name1}' in database '{database}'.")
table_name2 = "quality_defects"
df2.to_sql(table_name2, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name2}' in database '{database}'.")
table_name3 = "downtime_log"
df3.to_sql(table_name3, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name3}' in database '{database}'.")
table_name4 = "employees_shifts"
df4.to_sql(table_name4, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name4}' in database '{database}'.")
table_name5 ="inventory_materials"
df5.to_sql(table_name5, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name5}' in database '{database}'.")
table_name6 = "machines_equipment"
df6.to_sql(table_name6, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name6}' in database '{database}'.")
table_name7 = "dim_products"
df7.to_sql(table_name7, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name7}' in database '{database}'.") 
table_name8 = "dim_employees"
df8.to_sql(table_name8, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name8}' in database '{database}'.")
table_name9 = "dim_date"    
df9.to_sql(table_name9, engine, if_exists="replace", index=False)
print(f"Data successfully loaded into table '{table_name9}' in database '{database}'.")