import pandas as pd
import numpy as np
from datetime import datetime
def get_data1():
    df = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Dim_Date", usecols=["Date", "Month", "Month_Name"])
    df1 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Production_Orders")
    df1["Start_Date"] = pd.to_datetime(df1["Start_DateTime"]).dt.date
    df1["End_DateTime"] = pd.to_datetime(df1["End_DateTime"]).dt.date
    df1["Start_DateTime"] = pd.to_datetime(df1["Start_DateTime"])
    df1["End_DateTime"] = pd.to_datetime(df1["End_DateTime"])
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df1["Production_Variance"] = (df1["Qty_Planned"] - df1["Qty_Produced"]).clip(lower=0)
    df1["Plan_Attainment_Rate"] = round((df1["Qty_Produced"] / df1["Qty_Planned"]) * 100 ,2)
    df1["Production_Duration"] = (df1["End_DateTime"] - df1["Start_DateTime"]).dt.total_seconds() / 3600
    df1["Under_Over_Produced_Flag"] = df1.apply(lambda row: "Under" if row["Production_Variance"] > 0 else ("Over" if row["Production_Variance"] < 0 else "On Target"), axis=1)
    df1["Target_Met_Flag"] = df1["Under_Over_Produced_Flag"].apply(lambda x: "No" if x == "Under" else "Yes")
    df1["Planned_Cost"] = df1["Unit_Cost_GBP"] * df1["Qty_Planned"]
    df1["Cost_Variance"] = df1["Planned_Cost"] - df1["Total_Cost_GBP"]
    Shift_Duration_Mapping = {
        "Shift A" : 8,
        "Shift B" : 8,  
        "Shift C" : 8
    } 
    df1["Shift_Duration"] = df1["Shift"].map(Shift_Duration_Mapping)
    df1["Shift_Utilization%"] = ((df1["Duration_hrs"] / df1["Shift_Duration"]) * 100).clip(upper=100)
    merged = pd.merge(df1, df, left_on="Start_Date", right_on="Date", how="left")
    df1["Current_Month"] = merged["Month"]
    df1["Month_Name"] = merged["Month_Name"].str[:3]
    return df1
def get_data2():
    df = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Dim_Products", usecols=["Standard_Cost_GBP", "Product_ID"])
    df2 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Quality_Defects")
    df3 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Dim_Date", usecols=["Date", "Month", "Month_Name"])
    df3["Date"] = pd.to_datetime(df3["Date"]).dt.date
    df2["Inspection_Date"] = pd.to_datetime(df2["Inspection_Date"]).dt.date
    merged = pd.merge(df2, df, on="Product_ID", how="left")
    merged1 = pd.merge(df2, df3, left_on="Inspection_Date", right_on="Date", how="left")
    df2["Inspection_Type"] = df2["Linked_Order_ID"].apply(lambda x: "Routine Inspection" if x is None else "Rejection Inspection")
    df2["Pass_Rate"] = round((df2["Units_Passed"] / df2["Units_Inspected"])*100, 2)
    df2["Scrap_Rate"] = round((df2["Scrapped"] / df2["Units_Inspected"])*100, 2)
    df2["Quality_Rating"] = round((df2["Units_Defective"] / df2["Units_Inspected"])*100, 2)
    df2["Rework_Units"] = df2["Units_Defective"] - df2["Scrapped"]
    df2["Rework_Rate"] = round((df2["Rework_Units"] / df2["Units_Defective"])*100, 2)   
    df2["Rework_Flag"] = df2["Rework_Required"].apply(lambda x: "Yes" if x=='Yes' else "No")
    df2["Defect_Cost"] = df2["Units_Defective"] * merged["Standard_Cost_GBP"]
    df2["Scrap_Cost"] = df2["Scrapped"] * merged["Standard_Cost_GBP"]
    df2["Rework_Cost"] = df2["Rework_Units"] * merged["Standard_Cost_GBP"]
    df2["Current_Month"] = merged1["Month"]
    df2["Month_Name"] = merged1["Month_Name"].str[:3]
    df2 = df2.rename(columns={"Defect_Rate_%": "Defect_Rate"})
    return df2
def get_data3():
    df3 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Downtime_Log")
    df = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Machines_Equipment", usecols=["Machine_ID", "Production_Line", "Capacity_hrs_day"])
    df1 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Dim_Date", usecols=["Date", "Month", "Month_Name"])
    merged = pd.merge(df3, df, on=["Machine_ID", "Production_Line"], how="left")
    merged1 = pd.merge(df3, df1, left_on="Date", right_on="Date", how="left")
    df3["Current_Month"] = merged1["Month"]
    df3["Month_Name"] = merged1["Month_Name"].str[:3]
    df3["Capacity_hrs_day"] = merged["Capacity_hrs_day"]
    df3["Used_Time_hrs"] = df3["Capacity_hrs_day"] - df3["Duration_hrs"]
    df3["Downtime_Rate"] = ((df3["Duration_hrs"] / df3["Capacity_hrs_day"])*100).clip(upper=100)
    df3["Planned_unplanned_Flag"] = df3["Downtime_Type"].apply(lambda x: "Planned" if x == "Planned Maintenance" else "Unplanned")
    df3["Cost_GBP_per_hr"] = round(df3["Cost_GBP"]/df3["Duration_hrs"], 2)
    df3["Unresolved_Cost_GBP"] = df3.apply(lambda row: row["Cost_GBP"] if row["Resolved"] == "No" else 0, axis=1)
    df3["Unplanned_Cost_GBP"] = df3.apply(lambda row: row["Cost_GBP"] if row["Planned_unplanned_Flag"] == "Unplanned" else 0, axis=1)
    return df3
def get_data4():
    df4 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Employees_Shifts")
    df = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Dim_Date", usecols=["Date", "Month", "Month_Name"])
    merged = pd.merge(df4, df, left_on="Date", right_on="Date", how="left")
    df4["Current_Month"] = merged["Month"]
    df4["Month_Name"] = merged["Month_Name"].str[:3]
    df4["Regular_Hours"] = df4["Hours_Worked"] - df4["Overtime_hrs"]
    df4["Overtime_Flag"] = df4["Overtime_hrs"].apply(lambda x: "Yes" if x > 0 else "No")
    df4["Overtime_Rate"] = df4.apply(lambda row: (row["Overtime_hrs"]/row["Regular_Hours"]) if row["Overtime_Flag"] == "Yes" else 0, axis=1)
    df4["Units_Produced_per_hr"] = df4["Units_Produced"] / df4["Regular_Hours"]
    df4["Planned_Units"] = np.ceil((df4["Units_Produced"]/df4["Productivity_%"])*100)
    df4["Shift_Type"] = df4["Shift"].apply(lambda x: "Day Shift" if x in ["Shift A", "Shift B"] else "Night Shift")
    df4["Shift_Efficiency"] = (df4["Units_Produced"] / df4["Planned_Units"])*100
    df4["Machine_Productivity_Rate"] = round(df4["Units_Produced"] / df4["Regular_Hours"], 2)
    return df4
def get_data5():
    df5 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Inventory_Materials")
    df = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Dim_Date", usecols=["Date", "Month", "Month_Name"])
    merged = pd.merge(df5, df, on=["Date"], how="left") 
    df5["Current_Month"] = merged["Month"]
    df5["Month_Name"] = merged["Month_Name"].str[:3]
    df5["Stock_Gap"] = df5.apply(lambda row: row["Reorder_Level"] - row["Qty_In_Stock"] if row["Reorder_Level"] - row["Qty_In_Stock"] > 0 else 0, axis=1)
    df5["Stock_Surplus"] = df5.apply(lambda row: row["Qty_In_Stock"] - row["Reorder_Level"] if row["Qty_In_Stock"] - row["Reorder_Level"] > 0 else 0, axis=1)
    df5["Reorder_Quantity"] = df5["Stock_Gap"].clip(lower=0)
    df5["Reorder_Rating"] = round((df5["Stock_Gap"] / df5["Reorder_Level"]) * df5["Lead_Time_days"], 2)
    df5["Stock_Value_GBP"] = df5["Qty_In_Stock"] * df5["Unit_Cost_GBP"]
    def rating_label(score):
        if score <= 0:   
            return "No action"
        elif score <= 5:  
            return "Watch"
        elif score <= 15: 
            return "Reorder soon"
        elif score <= 30: 
            return "Reorder now"
        else:          
            return "Critical - escalate"
    df5["Reorder_Priority"] = df5["Reorder_Rating"].apply(rating_label)
    df5["Reorder_Cost_GBP"] = df5["Reorder_Quantity"] * df5["Unit_Cost_GBP"]
    df5["Stock_Coverage_Pcnt"] = (df5["Qty_In_Stock"] / df5["Reorder_Level"])*100
    df5["Stockout_Risk"] = df5["Stock_Coverage_Pcnt"].apply(lambda x: "Stockout" if x==0 else "High" if x < 200  else ("Medium" if x <500 else "Low"))
    return df5
def get_data6():
    df6 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Machines_Equipment")
    df = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Dim_Date", usecols=["Date", "Month", "Month_Name"])
    current_day = '26-11-2024'
    current_day = pd.to_datetime(current_day, dayfirst=True)
    merged = pd.merge(df6, df, left_on="Last_Maintenance", right_on="Date", how="left")
    df6["Current_Month"] = merged["Month"]
    df6["Month_Name"] = merged["Month_Name"].str[:3]
    df6["Install_Date"] = pd.to_datetime(df6["Install_Date"])
    df6["Last_Maintenance"] = pd.to_datetime(df6["Last_Maintenance"])
    df6["Next_Maintenance"] = pd.to_datetime(df6["Next_Maintenance"])
    df6["Machine_Age_years"] = (current_day - df6["Install_Date"]).dt.days / 365
    df6["Machine_Age_years"] = df6["Machine_Age_years"].round(2)
    df6["Days_Since_Maintenance"] = (current_day- df6["Last_Maintenance"]).dt.days
    df6["Days_Until_Next_Maintenance"] = ((df6["Next_Maintenance"] - current_day).dt.days)
    df6["Maintenance_Interval_days"] = ((df6["Next_Maintenance"] - df6["Last_Maintenance"]).dt.days)
    df6["Maintenance_Overdue_Flag"] = df6["Days_Until_Next_Maintenance"].apply(lambda x: "Yes" if x < 0 else "No")
    df6["Maintenance_Overdue_Days"] = df6["Days_Until_Next_Maintenance"].apply(lambda x: abs(x) if x < 0 else 0)
    df6["Maintenance_Urgency"] = df6.apply(lambda row: "Critical - Overdue" if row["Days_Until_Next_Maintenance"] < 0 else ("Due Soon" if row["Days_Until_Next_Maintenance"] <= 15 else "Not Due"), axis=1)
    df6["Expected_Activity_hrs"] = df6["OEE_Target_%"] * df6["Capacity_hrs_day"] / 100
    df6["Estimated_Downtime"] = df6["Capacity_hrs_day"] - df6["Expected_Activity_hrs"]
    df6["Estimated_Downtime_Rate"] = (df6["Estimated_Downtime"] / df6["Capacity_hrs_day"])*100
    df6["Machine_Efficiency"] = (df6["Expected_Activity_hrs"] / df6["Capacity_hrs_day"])*100
    df6["Asset_Value_per_capacity"] = df6["Asset_Value_GBP"] / df6["Capacity_hrs_day"]
    return df6
def get_data7():
    df7 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Dim_Products")
    return df7
def get_data8():
    df8 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Dim_Employees")
    df8["Join_Date"] = pd.to_datetime(df8["Join_Date"])
    return df8
def get_data9():
    df9 = pd.read_excel("Manufacturing_Dataset.xlsx", sheet_name="Dim_Date")
    df9["Date"] = pd.to_datetime(df9["Date"])
    return df9