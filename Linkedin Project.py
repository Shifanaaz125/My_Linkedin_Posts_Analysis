#!/usr/bin/env python
# coding: utf-8

# # Project Summary: LinkedIn Post Analytics
# 

# ### Objective: *To analyze LinkedIn post engagement and reach by consolidating data from multiple Excel sheets into a single dataset for comprehensive analysis.*

# ##### Data Source: LinkedIn posts data downloaded as 89 separate Excel sheets.
# ##### Task: Merge all 89 Excel sheets into a single consolidated sheet for easier analysis.
# ##### Tools: Python for data merging and Excel for final data review.
# ##### Outcome: A unified dataset that facilitates the analysis of post performance, engagement metrics, and reach, helping to identify which types of posts resonate best with the audience.
# 

# # Methodolgy

# ### Steps Taken:
# **Downloaded Data: Collected 92 different Excel sheets containing data for individual LinkedIn posts.**
# 
# **Python Code: Utilized Python to merge all Excel files into a single consolidated sheet.**
# 
# **Excel: Preperocess the data to analys it.**
# 
# **Analysis: Plan to use the unified dataset to analyze engagement patterns and optimize post strategies.**

# In[2]:


import pandas as pd
import glob

# Specify the path to the folder containing Excel files using a raw string
path = r'C:\Users\Shifa\OneDrive\Resume\Linkedin post Analysis\*.xlsx'
files = glob.glob(path)

# Initialize an empty list to hold dataframes
df_list = []

# Loop through each file and append to the list
for file in files:
    df = pd.read_excel(file)
    df_list.append(df)

# Concatenate all dataframes
combined_df = pd.concat(df_list, ignore_index=True)


# Export to Excel
combined_df.to_excel('consolidated_data.xlsx', index=False)


# In[2]:


combined_df.head(20)


# In[11]:


df = pd.read_excel(r'C:\Users\Shifa\OneDrive\Resume\Linkedin post Analysis\consolidated_data.xlsx')


# In[12]:


df.shape


# In[13]:


print(df)

print('dimensions:')
print(df.shape)

print('Information:')
df.info()


# ### Data Restructure and Saving file in local Machine ###
# 

# In[6]:


import pandas as pd

# Load the CSV file
file_path = r'C:\Users\Shifa\OneDrive\Resume\Linkedin post Analysis\consolidated_data.csv'
data = pd.read_csv(file_path)

# Step 1: Restructure Data
# Extract the Post URL (assuming it starts at the first column)
# and separate it into its own column.
# Assumption: We want to drop any duplicate header rows.

# Filter out rows where Post URL is empty or NaN
data_cleaned = data.dropna(subset=['Post URL'])

# Now, reset the index and ensure that all post metrics align with their post URLs
# Assuming each row represents a post with its metrics, we can fix the order
data_cleaned.reset_index(drop=True, inplace=True)

# Step 2: Export the cleaned data
output_path = r'C:\Users\Shifa\OneDrive\Resume\Linkedin post Analysis\consolidated_data.csv'
data_cleaned.to_csv(output_path, index=False)

print("Data restructuring complete. Cleaned CSV saved at:", output_path)


# In[7]:


data_cleaned.head


# In[14]:


# Save file to the current working directory
save_path = r'consolidated_linkedin_data.xlsx'

# Export the reshaped data to Excel
combined_df.to_excel(save_path, index=False)

print(f"Data reshaping and consolidation complete and saved as '{save_path}' in the current directory")


# In[27]:


import pandas as pd

# Load the data
file_path = r'C:\Users\Shifa\OneDrive\Resume\Linkedin post Analysis\consolidated_data.xlsx'
df = pd.read_excel(file_path)

# Print the column names to inspect
print(df.columns)


# In[28]:


print(combined_df.shape)  # (rows, columns)


# In[29]:


print(combined_df.head(100))  # First 5 rows
print(combined_df.tail(100))  # Last 5 rows


# In[5]:


import pandas as pd

df= pd.read_excel(r'C:\Users\Shifa\OneDrive\Resume\Linkedin post Analysis\consolidated_data.xlsx')

df_transposed = df.T

df_transposed.to_excel("transposed_file.xlsx")


# In[6]:


df_transposed.head(20)


# In[7]:


import pandas as pd 

# Load the original Excel file
df = pd.read_excel(r'C:\Users\Shifa\OneDrive\Resume\Linkedin post Analysis\consolidated_data.xlsx')

# Transpose the DataFrame
df_transposed = df.T

# Save the transposed DataFrame to a specific location
df_transposed.to_excel(r'C:\Users\Shifa\OneDrive\Resume\Linkedin post Analysis\transposed_file.xlsx', index=True)


# In[8]:


print(df_transposed.shape)  # (rows, columns)


# In[ ]:




