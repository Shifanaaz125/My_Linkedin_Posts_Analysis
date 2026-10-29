#!/usr/bin/env python
# coding: utf-8

# In[460]:


from pathlib import Path


# In[461]:


raw_folder = Path(r"C:\Users\Shifa\OneDrive\Resume\Linkedin post Analysis")

print(raw_folder)


# In[462]:


excel_files = list(raw_folder.glob("*.xlsx"))

print(f"Excel files found: {len(excel_files)}")


# In[463]:


#Step 1 — Create a basic file inventory


# In[464]:


file_inventory = []

for file in excel_files:
    file_inventory.append({
        "file_name": file.name,
        "file_size_kb": round(file.stat().st_size / 1024, 2)
    })

file_inventory[:10]


# In[465]:


raw_excel_files = [
    file for file in excel_files
    if file.name.startswith("PostAnalytics_")
]

print(f"Potential raw LinkedIn files: {len(raw_excel_files)}")
print(f"Other Excel files: {len(excel_files) - len(raw_excel_files)}")


# In[466]:


#Step 2 — Let's inspect the 42 "other" files


# In[467]:


other_excel_files = [
    file for file in excel_files
    if not file.name.startswith("PostAnalytics_")
]

for file in other_excel_files:
    print(file.name)


# In[468]:


#Step 3 — Inspect the first PostAnalytics filename


# In[469]:


print(raw_excel_files[0])


# In[470]:


#Step 4 — Inspect the workbook's sheets


# In[471]:


import pandas as pd

sample_post_file = raw_excel_files[0]

excel_file = pd.ExcelFile(sample_post_file)

print("File:", sample_post_file.name)
print("Sheets:", excel_file.sheet_names)


# In[472]:


single_post_files = [
    file for file in excel_files
    if file.name.startswith("SinglePostAnalytics_")
]

print(f"SinglePostAnalytics files: {len(single_post_files)}")
print(single_post_files[0])


# In[473]:


# Inspect its sheets


# In[474]:


sample_single_file = single_post_files[0]

single_excel_file = pd.ExcelFile(sample_single_file)

print("File:", sample_single_file.name)
print("Sheets:", single_excel_file.sheet_names)


# In[475]:


# Step 5 — Now we inspect the actual data structure


# In[476]:


post_df = pd.read_excel(
    sample_post_file,
    sheet_name="PERFORMANCE"
)

print("Shape:", post_df.shape)
print("\nColumns:")
print(post_df.columns.tolist())


# In[477]:


#Step 6 — Read the SinglePostAnalytics sheet


# In[478]:


single_df = pd.read_excel(
    sample_single_file,
    sheet_name="Post analytics"
)

print("Shape:", single_df.shape)
print("\nColumns:")
print(single_df.columns.tolist())


# In[479]:


#Step 7 — Inspect the complete PostAnalytics raw data


# In[480]:


print(post_df.to_string(index=False))


# In[481]:



#Step 8 — Inspect the complete SinglePostAnalytics structure


# In[482]:




print(single_df.to_string(index=False))


# In[483]:


#Step 9 — Let's extract the Post URLs from the filenames/data


# In[484]:


post_url_from_post = post_df.iloc[0, 1]

print(post_url_from_post)


# In[485]:


#Step 10 — Let's inspect the structure precisely


# In[486]:


print("Columns:")
print(post_df.columns.tolist())

print("\nIndex:")
print(post_df.index.tolist())

print("\nFirst 3 rows:")
print(post_df.head(3))


# In[487]:


#Step 11 — Extract the actual Post URL correctly


# In[488]:


post_url = post_df.columns[1]

print(post_url)


# In[489]:


#Step 12 — Let's confirm the same behavior in SinglePostAnalytics


# In[490]:



print("Columns:")
print(single_df.columns.tolist())

print("\nFirst 3 rows:")
print(single_df.head(3))


# In[491]:


#Step 13 — Extract the Post URL from the SinglePostAnalytics file


# In[492]:


single_post_url = single_df.columns[1]

print(single_post_url)


# In[493]:


#Step 14 — Let's inspect the filenames against the URLs


# In[494]:



file_name = sample_post_file.stem

print("Filename:")
print(file_name)

print("\nURL:")
print(post_url)


# In[495]:


#Step 15 — Check the SinglePostAnalytics filename ID


# In[496]:


single_file_name = sample_single_file.stem

print("Filename:")
print(single_file_name)

print("\nURL:")
print(single_post_url)


# In[497]:


for file in raw_excel_files[:10]:
    print(file.name)


# In[498]:


#Step 16 — Let's quantify the duplicate candidates


# In[499]:


copy_files = [
    file for file in raw_excel_files
    if " - Copy" in file.stem
]

print(f"Potential copy files: {len(copy_files)}")


# In[500]:


#Step 17 - classify the raw files


# In[501]:


file_inventory_df = pd.DataFrame([
    {
        "file_name": file.name,
        "file_size_kb": round(file.stat().st_size / 1024, 2),
        "source_type": (
            "PostAnalytics"
            if file.name.startswith("PostAnalytics_")
            else "SinglePostAnalytics"
            if file.name.startswith("SinglePostAnalytics_")
            else "Other"
        ),
        "is_copy_candidate": " - Copy" in file.stem
    }
    for file in excel_files
])

print(file_inventory_df["source_type"].value_counts())
print()
print(file_inventory_df["is_copy_candidate"].value_counts())


# In[502]:


import hashlib

def calculate_file_hash(file_path):
    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


file_inventory_df["file_hash"] = [
    calculate_file_hash(file)
    for file in excel_files
]

print("Hash calculation completed.")
print("Unique file hashes:", file_inventory_df["file_hash"].nunique())
print("Total Excel files:", len(file_inventory_df))


# In[503]:


#Show the exact duplicate groups


# In[504]:


duplicate_hashes = (
    file_inventory_df
    .groupby("file_hash")
    .filter(lambda group: len(group) > 1)
    .sort_values("file_hash")
)

print(
    duplicate_hashes[
        ["file_name", "source_type", "is_copy_candidate", "file_hash"]
    ].to_string(index=False)
)


# In[505]:


copy_candidates_df = file_inventory_df[
    file_inventory_df["is_copy_candidate"]
].copy()

copy_candidates_df["hash_duplicate"] = copy_candidates_df[
    "file_hash"
].duplicated(keep=False)

copy_exceptions = copy_candidates_df[
    ~copy_candidates_df["hash_duplicate"]
]

print("Copy candidates:", len(copy_candidates_df))
print("Exact duplicate copy files:", 
      copy_candidates_df["hash_duplicate"].sum())
print("Non-identical copy candidates:", len(copy_exceptions))

print("\nNon-identical copy candidates:")
print(
    copy_exceptions[
        ["file_name", "source_type", "file_size_kb", "file_hash"]
    ].to_string(index=False)
)


# In[506]:


copy_hash_counts = (
    file_inventory_df
    .groupby("file_hash")
    .size()
    .rename("files_with_same_hash")
)

copy_candidates_df = file_inventory_df[
    file_inventory_df["is_copy_candidate"]
].copy()

copy_candidates_df = copy_candidates_df.merge(
    copy_hash_counts,
    left_on="file_hash",
    right_index=True
)

true_copy_exceptions = copy_candidates_df[
    copy_candidates_df["files_with_same_hash"] == 1
]

print("Copy candidates:", len(copy_candidates_df))
print(
    "Copy candidates with matching file hash:",
    (copy_candidates_df["files_with_same_hash"] > 1).sum()
)
print(
    "Copy candidates with no matching file hash:",
    len(true_copy_exceptions)
)

print("\nPotential exceptions:")
print(
    true_copy_exceptions[
        ["file_name", "source_type", "file_size_kb", "file_hash"]
    ].to_string(index=False)
)


# In[507]:


original_6974 = raw_folder / "PostAnalytics_ShifaNaaz_6974940149876965376.xlsx"
copy_6974 = raw_folder / "PostAnalytics_ShifaNaaz_6974940149876965376 - Copy.xlsx"

original_df = pd.read_excel(
    original_6974,
    sheet_name="PERFORMANCE"
)

copy_df = pd.read_excel(
    copy_6974,
    sheet_name="PERFORMANCE"
)

print("ORIGINAL")
print("Shape:", original_df.shape)
print("Columns:", original_df.columns.tolist())
print()

print("COPY")
print("Shape:", copy_df.shape)
print("Columns:", copy_df.columns.tolist())


# In[508]:


#Next step — compare the actual data


# In[509]:


print("Are the dataframes identical?")
print(original_df.equals(copy_df))

print("\nORIGINAL DATA")
print(original_df.to_string(index=False))

print("\nCOPY DATA")
print(copy_df.to_string(index=False))


# In[510]:


print("ORIGINAL DTYPES")
print(original_df.dtypes)

print("\nCOPY DTYPES")
print(copy_df.dtypes)

print("\nCOLUMN NAMES IDENTICAL?")
print(original_df.columns.equals(copy_df.columns))

print("\nINDEX IDENTICAL?")
print(original_df.index.equals(copy_df.index))

print("\nSHAPE IDENTICAL?")
print(original_df.shape == copy_df.shape)


# In[511]:


differences = original_df.ne(copy_df)

print("Number of different cells:", differences.sum().sum())

print("\nDifferent cells:")

for row_idx, col_idx in zip(*differences.to_numpy().nonzero()):
    col_name = original_df.columns[col_idx]

    print(f"\nRow: {row_idx}")
    print(f"Column: {col_name}")
    print("Original:", repr(original_df.iloc[row_idx, col_idx]))
    print("Copy:    ", repr(copy_df.iloc[row_idx, col_idx]))


# In[512]:


original_7089 = raw_folder / "PostAnalytics_ShifaNaaz_7089201422558240769.xlsx"
copy_7089 = raw_folder / "PostAnalytics_ShifaNaaz_7089201422558240769 - Copy.xlsx"

original_7089_df = pd.read_excel(
    original_7089,
    sheet_name="PERFORMANCE"
)

copy_7089_df = pd.read_excel(
    copy_7089,
    sheet_name="PERFORMANCE"
)

print("ORIGINAL")
print("Shape:", original_7089_df.shape)
print("Columns:", original_7089_df.columns.tolist())

print("\nCOPY")
print("Shape:", copy_7089_df.shape)
print("Columns:", copy_7089_df.columns.tolist())


# In[513]:


print("===== ORIGINAL =====")
print(original_7089_df.to_string(index=False))

print("\n\n===== COPY =====")
print(copy_7089_df.to_string(index=False))


# In[514]:


print("ORIGINAL FILE")
print("Name:", original_7089.name)
print("Modified:", original_7089.stat().st_mtime)

print("\nCOPY FILE")
print("Name:", copy_7089.name)
print("Modified:", copy_7089.stat().st_mtime)


# In[515]:


from datetime import datetime

print("Original modified:")
print(datetime.fromtimestamp(original_7089.stat().st_mtime))

print("\nCopy modified:")
print(datetime.fromtimestamp(copy_7089.stat().st_mtime))


# In[516]:


structure_inventory = []

for file in raw_excel_files:
    try:
        excel_file = pd.ExcelFile(file)

        structure_inventory.append({
            "file_name": file.name,
            "sheet_count": len(excel_file.sheet_names),
            "sheet_names": " | ".join(excel_file.sheet_names),
            "status": "Readable"
        })

    except Exception as e:
        structure_inventory.append({
            "file_name": file.name,
            "sheet_count": None,
            "sheet_names": None,
            "status": f"Error: {type(e).__name__}"
        })

structure_inventory_df = pd.DataFrame(structure_inventory)

print("Files profiled:", len(structure_inventory_df))
print("\nStatus:")
print(structure_inventory_df["status"].value_counts())

print("\nSheet count:")
print(structure_inventory_df["sheet_count"].value_counts().sort_index())


# In[517]:


sheet_structure_summary = (
    structure_inventory_df
    .groupby(["sheet_count", "sheet_names"])
    .size()
    .reset_index(name="file_count")
    .sort_values(
        ["sheet_count", "file_count"],
        ascending=[True, False]
    )
)

print(sheet_structure_summary.to_string(index=False))


# In[518]:


two_sheet_files = [
    file for file in raw_excel_files
    if (
        structure_inventory_df.loc[
            structure_inventory_df["file_name"] == file.name,
            "sheet_count"
        ].iloc[0] == 2
    )
]

sample_two_sheet_file = two_sheet_files[0]

print("Sample file:")
print(sample_two_sheet_file.name)

print("\nSheets:")
print(pd.ExcelFile(sample_two_sheet_file).sheet_names)


# In[519]:


demographics_df = pd.read_excel(
    sample_two_sheet_file,
    sheet_name="TOP DEMOGRAPHICS"
)

print("Shape:", demographics_df.shape)

print("\nColumns:")
print(demographics_df.columns.tolist())

print("\nData:")
print(demographics_df.to_string(index=False))


# In[520]:


#Next step: inspect the PERFORMANCE sheet from this same workbook


# In[521]:


performance_two_sheet_df = pd.read_excel(
    sample_two_sheet_file,
    sheet_name="PERFORMANCE"
)

print("Shape:", performance_two_sheet_df.shape)

print("\nColumns:")
print(performance_two_sheet_df.columns.tolist())

print("\nData:")
print(performance_two_sheet_df.to_string(index=False))


# In[522]:


one_sheet_files = [
    file for file in raw_excel_files
    if (
        structure_inventory_df.loc[
            structure_inventory_df["file_name"] == file.name,
            "sheet_count"
        ].iloc[0] == 1
    )
]

print("One-sheet files:", len(one_sheet_files))

sample_one_sheet_file = one_sheet_files[0]

print("\nSample file:")
print(sample_one_sheet_file.name)

print("\nSheets:")
print(pd.ExcelFile(sample_one_sheet_file).sheet_names)


# In[523]:


#Next step — profile the row labels across all 69 files


# In[524]:


performance_schema = []

for file in one_sheet_files:
    try:
        df = pd.read_excel(
            file,
            sheet_name="PERFORMANCE"
        )

        row_labels = (
            df.iloc[:, 0]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        performance_schema.append({
            "file_name": file.name,
            "row_labels": row_labels
        })

    except Exception as e:
        performance_schema.append({
            "file_name": file.name,
            "row_labels": [],
            "status": f"Error: {type(e).__name__}"
        })

performance_schema_df = pd.DataFrame(performance_schema)

print("Files profiled:", len(performance_schema_df))

print("\nFirst 5 file structures:")
for _, row in performance_schema_df.head().iterrows():
    print("\n", row["file_name"])
    print(row["row_labels"])


# In[525]:


from collections import Counter

all_performance_fields = []

for labels in performance_schema_df["row_labels"]:
    all_performance_fields.extend(labels)

field_frequency = (
    pd.Series(Counter(all_performance_fields))
    .sort_values(ascending=False)
)

print("Unique performance fields:", len(field_frequency))

print("\nField frequency across 69 files:")
print(field_frequency.to_string())


# In[526]:


two_sheet_demographic_schema = []

for file in two_sheet_files:
    try:
        df = pd.read_excel(
            file,
            sheet_name="TOP DEMOGRAPHICS"
        )

        two_sheet_demographic_schema.append({
            "file_name": file.name,
            "columns": df.columns.tolist(),
            "row_count": len(df),
            "categories": (
                df["Category"]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()
            )
        })

    except Exception as e:
        two_sheet_demographic_schema.append({
            "file_name": file.name,
            "columns": [],
            "row_count": None,
            "categories": [],
            "status": f"Error: {type(e).__name__}"
        })

two_sheet_demographic_schema_df = pd.DataFrame(
    two_sheet_demographic_schema
)

print("Files profiled:", len(two_sheet_demographic_schema_df))

print("\nFirst 5 demographic structures:")

for _, row in two_sheet_demographic_schema_df.head().iterrows():
    print("\n", row["file_name"])
    print("Columns:", row["columns"])
    print("Rows:", row["row_count"])
    print("Categories:", row["categories"])


# In[527]:


#Next: quantify the demographic variations


# In[528]:


category_pattern_counts = (
    two_sheet_demographic_schema_df
    .assign(
        category_pattern=two_sheet_demographic_schema_df["categories"]
        .apply(lambda x: " | ".join(sorted(x)))
    )
    ["category_pattern"]
    .value_counts()
)

print("Unique category patterns:", len(category_pattern_counts))

print("\nCategory pattern frequency:")
print(category_pattern_counts.to_string())


# In[529]:


single_schema = []

for file in single_post_files:
    try:
        df = pd.read_excel(
            file,
            sheet_name="Post analytics"
        )

        row_labels = (
            df.iloc[:, 0]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        single_schema.append({
            "file_name": file.name,
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": df.columns.tolist(),
            "row_labels": row_labels
        })

    except Exception as e:
        single_schema.append({
            "file_name": file.name,
            "row_count": None,
            "column_count": None,
            "columns": [],
            "row_labels": [],
            "status": f"Error: {type(e).__name__}"
        })

single_schema_df = pd.DataFrame(single_schema)

print("Files profiled:", len(single_schema_df))

print("\nFirst 5 SinglePostAnalytics structures:")

for _, row in single_schema_df.head().iterrows():
    print("\n", row["file_name"])
    print("Rows:", row["row_count"])
    print("Columns:", row["columns"])
    print("Row labels:", row["row_labels"])


# In[530]:


#Next — verify SinglePostAnalytics schema consistency


# In[531]:


single_field_frequency = (
    pd.Series(
        [
            label
            for labels in single_schema_df["row_labels"]
            for label in labels
        ]
    )
    .value_counts()
)

print("Unique SinglePostAnalytics row labels:",
      len(single_field_frequency))

print("\nField frequency across 40 files:")
print(single_field_frequency.to_string())


# In[532]:


single_pattern_counts = (
    single_schema_df
    .assign(
        row_pattern=single_schema_df["row_labels"]
        .apply(lambda x: " | ".join(x))
    )
    ["row_pattern"]
    .value_counts()
)

print("Unique SinglePostAnalytics row patterns:",
      len(single_pattern_counts))

print("\nPattern frequency:")
print(single_pattern_counts.to_string())


# In[533]:


sample_single = pd.read_excel(
    single_post_files[0],
    sheet_name="Post analytics"
)

print("Sample file:")
print(single_post_files[0].name)

print("\nData types:")
print(sample_single.dtypes)

print("\nRaw data:")
print(sample_single.to_string(index=False))


# In[534]:


def extract_post_url(df):
    """
    Extract the LinkedIn Post URL from the second column header.
    """

    if len(df.columns) < 2:
        raise ValueError("Expected at least two columns in the LinkedIn export.")

    post_url = str(df.columns[1]).strip()

    if not post_url.startswith("http"):
        raise ValueError("Second column header does not contain a valid URL.")

    return post_url


# Test on our sample SinglePostAnalytics file
sample_url = extract_post_url(sample_single)

print("Extracted Post URL:")
print(sample_url)


# In[535]:


print("Field → Raw Value → Python Data Type")
print("-" * 60)

for field in ["Post Date", "Post Publish Time", "Impressions", "Reactions", "Comments", "Reposts"]:
    
    matches = sample_single[
        sample_single.iloc[:, 0].astype(str).str.strip() == field
    ]
    
    if not matches.empty:
        value = matches.iloc[0, 1]
        print(f"{field:25} → {repr(value):15} → {type(value).__name__}")
    else:
        print(f"{field:25} → NOT FOUND")


# In[536]:


def get_field_value(df, field_names):
    """
    Return the value associated with the first matching field name.
    """

    if isinstance(field_names, str):
        field_names = [field_names]

    field_column = df.iloc[:, 0].astype(str).str.strip()

    for field_name in field_names:
        matches = df[field_column == field_name]

        if not matches.empty:
            return matches.iloc[0, 1]

    return None


# Test the helper
print("Impressions:", repr(get_field_value(sample_single, "Impressions")))
print("Comments:", repr(get_field_value(sample_single, ["Comments", "Comment"])))
print("Reposts:", repr(get_field_value(sample_single, ["Reposts", "Repost"])))


# In[537]:


def extract_single_post_core(df):
    """
    Extract core post-level metrics from a SinglePostAnalytics export.
    """

    return {
        "post_url": extract_post_url(df),
        "post_date": get_field_value(df, "Post Date"),
        "publish_time": get_field_value(df, "Post Publish Time"),
        "impressions": get_field_value(df, "Impressions"),
        "reactions": get_field_value(df, "Reactions"),
        "comments": get_field_value(df, ["Comments", "Comment"]),
        "reposts": get_field_value(df, ["Reposts", "Repost"])
    }


# Test on the sample file
sample_core = extract_single_post_core(sample_single)

print(sample_core)


# In[538]:


video_files = []

for row in single_schema:
    if "Video views" in row["row_labels"]:
        video_files.append(row["file_name"])

print("SinglePostAnalytics files containing video metrics:", len(video_files))

print("\nFiles:")
for file_name in video_files:
    print(file_name)


# In[539]:


sample_video_file = raw_folder / video_files[0]

video_df = pd.read_excel(
    sample_video_file,
    sheet_name="Post analytics"
)

print("File:")
print(sample_video_file.name)

print("\nShape:")
print(video_df.shape)

print("\nRaw data:")
print(video_df.to_string(index=False))


# In[540]:


print("Video metric values and data types")
print("-" * 50)

for field in [
    "Video views",
    "Watch time",
    "Average watch time"
]:
    
    value = get_field_value(video_df, field)
    
    print(
        f"{field:20} → "
        f"{repr(value):10} → "
        f"{type(value).__name__}"
    )


# In[541]:


optional_fields = [
    "Premium custom button engagements",
    "Members reached",
    "Video views",
    "Watch time",
    "Average watch time"
]

optional_summary = []

for field in optional_fields:
    file_count = sum(
        field in labels
        for labels in single_schema_df["row_labels"]
    )

    optional_summary.append({
        "field": field,
        "files_containing_field": file_count,
        "files_missing_field": len(single_schema_df) - file_count
    })

optional_summary_df = pd.DataFrame(optional_summary)

print(optional_summary_df.to_string(index=False))


# In[542]:


sample_post = pd.read_excel(
    sample_post_file,
    sheet_name="PERFORMANCE"
)

print("Sample file:")
print(sample_post_file.name)

print("\nData types:")
print(sample_post.dtypes)

print("\nRaw data:")
print(sample_post.to_string(index=False))


# In[543]:


print("Demographic values and data types")
print("-" * 60)

print("Columns:")
for column in demographics_df.columns:
    print(f"{column:12} → {demographics_df[column].dtype}")

print("\nFirst 10 rows:")
print(demographics_df.head(10).to_string(index=False))


# In[544]:


url_validation = []

for file in raw_excel_files:
    try:
        df = pd.read_excel(
            file,
            sheet_name="PERFORMANCE"
        )

        if len(df.columns) >= 2:
            candidate_url = str(df.columns[1]).strip()
        else:
            candidate_url = None

        is_valid_url = (
            candidate_url is not None
            and candidate_url.startswith("http")
        )

        url_validation.append({
            "file_name": file.name,
            "candidate_url": candidate_url,
            "valid_url": is_valid_url
        })

    except Exception as e:
        url_validation.append({
            "file_name": file.name,
            "candidate_url": None,
            "valid_url": False
        })

url_validation_df = pd.DataFrame(url_validation)

print("Total PostAnalytics files checked:", len(url_validation_df))
print("\nURL validation results:")
print(url_validation_df["valid_url"].value_counts())

print("\nFiles without a valid URL:")
print(
    url_validation_df[
        ~url_validation_df["valid_url"]
    ]["file_name"].to_string(index=False)
)


# In[545]:


def extract_postanalytics_performance(df):
    """
    Extract core performance metrics from a PostAnalytics
    PERFORMANCE sheet.
    """

    return {
        "post_url": extract_post_url(df),
        "post_date": get_field_value(df, "Post Date"),
        "publish_time": get_field_value(df, "Post Publish Time"),
        "impressions": get_field_value(df, "Impressions"),
        "unique_views": get_field_value(df, "Unique views"),
        "reactions": get_field_value(df, "Reactions"),
        "comments": get_field_value(df, ["Comments", "Comment"]),
        "reposts": get_field_value(df, ["Reposts", "Repost"])
    }


# Test on the sample PostAnalytics file
sample_post_core = extract_postanalytics_performance(sample_post)

print(sample_post_core)


# In[546]:


postanalytics_fields = []

for file in raw_excel_files:
    try:
        df = pd.read_excel(
            file,
            sheet_name="PERFORMANCE"
        )

        labels = (
            df.iloc[:, 0]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        postanalytics_fields.append({
            "file_name": file.name,
            "row_labels": labels
        })

    except Exception as e:
        postanalytics_fields.append({
            "file_name": file.name,
            "row_labels": []
        })


postanalytics_schema_df = pd.DataFrame(postanalytics_fields)

all_postanalytics_fields = [
    label
    for labels in postanalytics_schema_df["row_labels"]
    for label in labels
]

postanalytics_field_frequency = (
    pd.Series(all_postanalytics_fields)
    .value_counts()
)

print("Unique PostAnalytics fields:",
      len(postanalytics_field_frequency))

print("\nField frequency across 162 files:")
print(postanalytics_field_frequency.to_string())


# In[547]:


#Next step: build a richer PostAnalytics extractor


# In[548]:


def extract_postanalytics_optional(df):
    """
    Extract commonly available optional metrics
    from a PostAnalytics PERFORMANCE sheet.
    """

    return {
        "profile_viewers": get_field_value(
            df, "Profile viewers from this post"
        ),
        "followers_gained": get_field_value(
            df, "Followers gained from this post"
        ),
        "saves": get_field_value(
            df, "Saves"
        ),
        "sends_on_linkedin": get_field_value(
            df, "Sends on LinkedIn"
        ),
        "members_reached": get_field_value(
            df, "Members reached"
        )
    }


sample_post_optional = extract_postanalytics_optional(sample_post)

print(sample_post_optional)


# In[549]:


optional_fields = [
    "Profile viewers from this post",
    "Followers gained from this post",
    "Saves",
    "Sends on LinkedIn",
    "Members reached",
    "Views",
    "Minutes viewed",
    "Lifetime unique viewers",
    "Article views"
]

for field in optional_fields:
    value = get_field_value(sample_post, field)
    print(f"{field}: {value}")


# In[550]:


postanalytics_files = sorted(
    [
        file_path
        for file_path in raw_folder.glob("PostAnalytics_*.xlsx")
    ]
)

print(f"PostAnalytics files found: {len(postanalytics_files)}")


# In[551]:


optional_sample_file = None

for file_path in postanalytics_files:
    df = pd.read_excel(file_path, sheet_name="PERFORMANCE")
    
    fields = df.iloc[:, 0].astype(str).str.strip()

    if "Profile viewers from this post" in fields.values:
        optional_sample_file = file_path
        break

print(optional_sample_file.name if optional_sample_file else "No matching file found")


# In[552]:



optional_sample = pd.read_excel(
    optional_sample_file,
    sheet_name="PERFORMANCE"
)

print(optional_sample.to_string(index=False))


# In[553]:


sample_post_optional = extract_postanalytics_optional(optional_sample)

print(sample_post_optional)


# In[554]:


postanalytics_record = {
    **extract_postanalytics_performance(optional_sample),
    **extract_postanalytics_optional(optional_sample)
}

print(postanalytics_record)


# In[555]:


print(repr(postanalytics_record["post_url"]))


# In[556]:


print(repr(optional_sample.columns[1]))


# In[557]:


import re

def extract_post_url(df):
    """
    Extract and clean the LinkedIn Post URL from the second column header.
    """

    if len(df.columns) < 2:
        raise ValueError("Expected at least two columns in the LinkedIn export.")

    raw_url = str(df.columns[1]).strip()

    # Extract the URL from Markdown-style hyperlink if present
    match = re.search(r"https?://[^)\s]+", raw_url)

    if not match:
        raise ValueError("Second column header does not contain a valid URL.")

    return match.group(0).replace("\\:", ":")

print(extract_post_url(optional_sample))


# In[558]:


clean_url = extract_post_url(optional_sample)

print(repr(clean_url))
print("Starts with https:", clean_url.startswith("https://"))
print("Contains Markdown brackets:", "[" in clean_url or "]" in clean_url)


# In[559]:


import re

def extract_post_url(df):
    """
    Extract and clean the LinkedIn Post URL from the second column header.
    Handles both plain URLs and Markdown-style hyperlinks.
    """

    if len(df.columns) < 2:
        raise ValueError("Expected at least two columns in the LinkedIn export.")

    raw_url = str(df.columns[1]).strip()

    # Extract URL and stop before Markdown ] or )
    match = re.search(r"https?://[^\]\)\s]+", raw_url)

    if not match:
        raise ValueError("Second column header does not contain a valid URL.")

    return match.group(0).replace("\\:", ":")

print(repr(extract_post_url(optional_sample)))


# In[560]:


raw_url = str(optional_sample.columns[1])

print("RAW:")
print(raw_url)

print("\nREPR:")
print(repr(raw_url))

print("\nCHARACTERS:")
for i, char in enumerate(raw_url):
    print(i, repr(char))


# In[561]:


def extract_post_url(df):
    """
    Extract the LinkedIn Post URL from the second column header.
    """

    if len(df.columns) < 2:
        raise ValueError("Expected at least two columns in the LinkedIn export.")

    post_url = str(df.columns[1]).strip()

    if not post_url.startswith("http"):
        raise ValueError("Second column header does not contain a valid URL.")

    return post_url

clean_url = extract_post_url(optional_sample)

print("URL:", clean_url)
print("Starts with https:", clean_url.startswith("https://"))
print("Length:", len(clean_url))


# In[562]:


single_postanalytics_files = list(
    raw_folder.glob("SinglePostAnalytics_*.xlsx")
)

print("SinglePostAnalytics files:", len(single_postanalytics_files))

single_sample = pd.read_excel(
    single_postanalytics_files[0],
    sheet_name="Post analytics"
)

print("Sample file:", single_postanalytics_files[0].name)
print("Shape:", single_sample.shape)
print("Columns:", single_sample.columns.tolist())


# In[563]:


print("PostAnalytics:")
print(repr(extract_post_url(optional_sample)))

print("\nSinglePostAnalytics:")
print(repr(extract_post_url(single_sample)))


# In[564]:


print("PostAnalytics files:", len(postanalytics_files))
print("SinglePostAnalytics files:", len(single_postanalytics_files))

print("\nExpected total:", len(postanalytics_files) + len(single_postanalytics_files))


# In[565]:


url_validation_results = []

for file_path in postanalytics_files:
    try:
        df = pd.read_excel(file_path, sheet_name="PERFORMANCE")
        post_url = extract_post_url(df)

        url_validation_results.append({
            "file_name": file_path.name,
            "source_type": "PostAnalytics",
            "status": "OK",
            "post_url": post_url
        })

    except Exception as e:
        url_validation_results.append({
            "file_name": file_path.name,
            "source_type": "PostAnalytics",
            "status": "ERROR",
            "post_url": None
        })


for file_path in single_postanalytics_files:
    try:
        df = pd.read_excel(file_path, sheet_name="Post analytics")
        post_url = extract_post_url(df)

        url_validation_results.append({
            "file_name": file_path.name,
            "source_type": "SinglePostAnalytics",
            "status": "OK",
            "post_url": post_url
        })

    except Exception as e:
        url_validation_results.append({
            "file_name": file_path.name,
            "source_type": "SinglePostAnalytics",
            "status": "ERROR",
            "post_url": None
        })


url_validation_df = pd.DataFrame(url_validation_results)

print("Total files tested:", len(url_validation_df))
print("\nStatus counts:")
print(url_validation_df["status"].value_counts())

print("\nSource type counts:")
print(url_validation_df["source_type"].value_counts())


# In[566]:


print("Total source files:", len(url_validation_df))
print("Unique Post URLs:", url_validation_df["post_url"].nunique())
print("Repeated Post URLs:", (url_validation_df["post_url"].value_counts() > 1).sum())


# In[567]:


repeated_url = (
    url_validation_df["post_url"]
    .value_counts()
    .loc[lambda x: x > 1]
    .index[0]
)

print("Repeated Post URL:")
print(repeated_url)

print("\nFiles containing this URL:")
print(
    url_validation_df.loc[
        url_validation_df["post_url"] == repeated_url,
        ["file_name", "source_type"]
    ].to_string(index=False)
)


# In[568]:


repeated_files = url_validation_df.loc[
    url_validation_df["post_url"] == repeated_url,
    "file_name"
].tolist()

for file_name in repeated_files:
    df = pd.read_excel(raw_folder / file_name, sheet_name="PERFORMANCE")
    
    print("\n" + "=" * 80)
    print(file_name)
    print("=" * 80)
    print(df.iloc[:, :2].to_string(index=False))


# In[569]:


print("Type:", type(file_inventory))
print("Number of items:", len(file_inventory))

print("\nFirst item:")
print(file_inventory[0])


# In[570]:


[name for name in globals() if "hash" in name.lower() or "inventory" in name.lower()]


# In[571]:


print(file_inventory_df.columns.tolist())
print("\nShape:", file_inventory_df.shape)


# In[572]:


url_hash_summary = (
    url_validation_df
    .merge(
        file_inventory_df[["file_name", "file_hash"]],
        on="file_name",
        how="left"
    )
    .groupby("post_url")
    .agg(
        file_count=("file_name", "count"),
        unique_hashes=("file_hash", "nunique")
    )
    .query("file_count > 1")
    .reset_index()
)

print("Repeated Post URLs:", len(url_hash_summary))
print("\nUnique hash patterns among repeated URLs:")
print(url_hash_summary["unique_hashes"].value_counts().sort_index())


# In[573]:


print(
    url_hash_summary[
        url_hash_summary["unique_hashes"] > 1
    ][["post_url", "file_count", "unique_hashes"]]
    .sort_values(["unique_hashes", "file_count"], ascending=False)
    .to_string(index=False)
)


# In[574]:


test_url = "https://www.linkedin.com/feed/update/urn:li:share:7328739655212826624"

test_files = url_validation_df.loc[
    url_validation_df["post_url"] == test_url,
    "file_name"
].tolist()

for file_name in test_files:
    df = pd.read_excel(
        raw_folder / file_name,
        sheet_name="PERFORMANCE"
    )

    print("\n" + "=" * 80)
    print(file_name)
    print("=" * 80)

    fields_to_check = [
        "Post Date",
        "Post Publish Time",
        "Impressions",
        "Members reached",
        "Profile viewers from this post",
        "Followers gained from this post",
        "Reactions",
        "Comments",
        "Reposts",
        "Saves",
        "Sends on LinkedIn"
    ]

    for field in fields_to_check:
        value = get_field_value(df, field)
        print(f"{field}: {value}")


# In[575]:


print(
    url_hash_summary[
        url_hash_summary["unique_hashes"] == 1
    ]["file_count"]
    .value_counts()
    .sort_index()
)


# In[576]:


dedup_df = file_inventory_df.copy()

dedup_df["duplicate_group_size"] = (
    dedup_df.groupby("file_hash")["file_hash"]
    .transform("size")
)

dedup_df["file_duplicate_status"] = dedup_df[
    "duplicate_group_size"
].map(
    lambda x: "EXACT_FILE_DUPLICATE" if x > 1 else "UNIQUE_CONTENT"
)

print(
    dedup_df["file_duplicate_status"]
    .value_counts()
)


# In[577]:


dedup_df = file_inventory_df.copy()

dedup_df["hash_occurrence"] = (
    dedup_df.groupby("file_hash")
    .cumcount() + 1
)

dedup_df["file_duplicate_status"] = dedup_df[
    "hash_occurrence"
].map(
    lambda x: "CANONICAL_FILE" if x == 1 else "EXACT_FILE_DUPLICATE"
)

print(
    dedup_df["file_duplicate_status"]
    .value_counts()
)


# In[578]:


canonical_df = dedup_df[
    dedup_df["file_duplicate_status"] == "CANONICAL_FILE"
].copy()

print("Canonical files:", len(canonical_df))
print("\nSource type distribution:")
print(canonical_df["source_type"].value_counts())


# In[579]:


source_files_df = canonical_df[
    canonical_df["source_type"].isin(
        ["PostAnalytics", "SinglePostAnalytics"]
    )
].copy()

print("Source files for processing:", len(source_files_df))
print("\nSource type distribution:")
print(source_files_df["source_type"].value_counts())


# In[580]:


read_check = []

for _, row in source_files_df.iterrows():
    file_path = raw_folder / row["file_name"]

    try:
        if row["source_type"] == "PostAnalytics":
            sheets = pd.ExcelFile(file_path).sheet_names
        else:
            sheets = pd.ExcelFile(file_path).sheet_names

        read_check.append({
            "file_name": row["file_name"],
            "source_type": row["source_type"],
            "status": "OK",
            "sheet_count": len(sheets)
        })

    except Exception as e:
        read_check.append({
            "file_name": row["file_name"],
            "source_type": row["source_type"],
            "status": "ERROR",
            "sheet_count": None
        })

read_check_df = pd.DataFrame(read_check)

print("Files tested:", len(read_check_df))
print("\nStatus:")
print(read_check_df["status"].value_counts())

print("\nSource type:")
print(read_check_df["source_type"].value_counts())


# In[581]:


postanalytics_read_check = read_check_df[
    read_check_df["source_type"] == "PostAnalytics"
].copy()

print(
    postanalytics_read_check["sheet_count"]
    .value_counts()
    .sort_index()
)


# In[582]:


two_sheet_files = []

for _, row in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
].iterrows():

    if row["file_name"] in set(
        postanalytics_read_check.loc[
            postanalytics_read_check["sheet_count"] == 2,
            "file_name"
        ]
    ):
        two_sheet_files.append(row["file_name"])

print("Canonical two-sheet PostAnalytics files:", len(two_sheet_files))


# In[583]:


demo_sample_file = two_sheet_files[0]

demo_sample = pd.read_excel(
    raw_folder / demo_sample_file,
    sheet_name="TOP DEMOGRAPHICS"
)

print("File:", demo_sample_file)
print("Shape:", demo_sample.shape)
print("\nColumns:")
print(demo_sample.columns.tolist())

print("\nFirst 10 rows:")
print(demo_sample.head(10).to_string(index=False))


# In[584]:


def extract_demographics(df):
    """
    Extract LinkedIn demographic data in long format.
    Raw category names and percentage values are preserved.
    """

    required_columns = ["Category", "Value", "%"]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing demographic columns: {missing_columns}"
        )

    demographics = df[
        required_columns
    ].copy()

    demographics.columns = [
        "category",
        "value",
        "percentage"
    ]

    return demographics


# In[585]:


demo_result = extract_demographics(demo_sample)

print("Shape:", demo_result.shape)
print("\nColumns:")
print(demo_result.columns.tolist())

print("\nFirst 10 rows:")
print(demo_result.head(10).to_string(index=False))


# In[586]:


all_categories = []

for file_name in two_sheet_files:
    df = pd.read_excel(
        raw_folder / file_name,
        sheet_name="TOP DEMOGRAPHICS"
    )
    
    all_categories.extend(
        df["Category"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

unique_categories = sorted(set(all_categories))

print("Unique category names:", len(unique_categories))
print("\nCategory names:")
for category in unique_categories:
    print("-", category)


# In[587]:


demographic_category_map = {
    "Company": "company",
    "Companies": "company",
    "Industry": "industry",
    "Industries": "industry",
    "Job title": "job_title",
    "Job titles": "job_title",
    "Location": "location",
    "Locations": "location",
    "Company size": "company_size",
    "Seniority": "seniority"
}

print("Mappings:", len(demographic_category_map))
print(demographic_category_map)


# In[588]:


demo_standardized = demo_result.copy()

demo_standardized["category"] = (
    demo_standardized["category"]
    .map(demographic_category_map)
)

print("Shape:", demo_standardized.shape)

print("\nStandardized categories:")
print(demo_standardized["category"].unique())

print("\nFirst 10 rows:")
print(demo_standardized.head(10).to_string(index=False))


# In[589]:


def extract_demographics(df):
    """
    Extract and standardize LinkedIn demographic data
    into a long-format structure.
    """

    required_columns = ["Category", "Value", "%"]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing demographic columns: {missing_columns}"
        )

    demographics = df[required_columns].copy()

    demographics.columns = [
        "category",
        "value",
        "percentage"
    ]

    demographics["category"] = (
        demographics["category"]
        .astype(str)
        .str.strip()
        .map(demographic_category_map)
    )

    return demographics


# In[590]:


demo_test = extract_demographics(demo_sample)

print("Shape:", demo_test.shape)
print("\nCategories:")
print(demo_test["category"].unique())

print("\nData types:")
print(demo_test.dtypes)

print("\nFirst 10 rows:")
print(demo_test.head(10).to_string(index=False))


# In[591]:


demographic_check = []

for file_name in two_sheet_files:
    try:
        df = pd.read_excel(
            raw_folder / file_name,
            sheet_name="TOP DEMOGRAPHICS"
        )

        result = extract_demographics(df)

        demographic_check.append({
            "file_name": file_name,
            "status": "OK",
            "rows_extracted": len(result),
            "unexpected_categories": result["category"].isna().sum()
        })

    except Exception as e:
        demographic_check.append({
            "file_name": file_name,
            "status": "ERROR",
            "rows_extracted": None,
            "unexpected_categories": None
        })

demographic_check_df = pd.DataFrame(demographic_check)

print("Files tested:", len(demographic_check_df))

print("\nStatus:")
print(demographic_check_df["status"].value_counts())

print("\nUnexpected categories:")
print(
    demographic_check_df["unexpected_categories"]
    .value_counts(dropna=False)
)


# In[592]:


demographics_records = []

for file_name in two_sheet_files:
    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="TOP DEMOGRAPHICS"
    )

    post_url = extract_post_url(
        pd.read_excel(
            file_path,
            sheet_name="PERFORMANCE"
        )
    )

    demographics = extract_demographics(df)

    demographics.insert(
        0,
        "post_url",
        post_url
    )

    demographics_records.append(demographics)

demographics_df = pd.concat(
    demographics_records,
    ignore_index=True
)

print("Shape:", demographics_df.shape)

print("\nColumns:")
print(demographics_df.columns.tolist())

print("\nFirst 10 rows:")
print(demographics_df.head(10).to_string(index=False))


# In[593]:


print("Percentage data types:")
print(demographics_df["percentage"].map(type).value_counts())

print("\nPercentage examples:")
print(demographics_df["percentage"].head(20).tolist())


# In[594]:


string_percentages = demographics_df[
    demographics_df["percentage"].map(type) == str
]["percentage"]

print("String percentage count:", len(string_percentages))

print("\nString percentage values:")
print(string_percentages.tolist())


# In[595]:


less_than_one_df = demographics_df[
    demographics_df["percentage"] == "< 1%"
]

print("Rows with '< 1%':", len(less_than_one_df))

print("\nBy category:")
print(less_than_one_df["category"].value_counts())

print("\nSample rows:")
print(less_than_one_df.head(20).to_string(index=False))


# In[596]:


numeric_percentages = demographics_df[
    demographics_df["percentage"].map(type) != str
]["percentage"]

print("Numeric percentage count:", len(numeric_percentages))

print("\nMinimum numeric percentage:", numeric_percentages.min())
print("Maximum numeric percentage:", numeric_percentages.max())

print("\nNumeric percentages outside 0-1:")
print(
    numeric_percentages[
        (numeric_percentages < 0) |
        (numeric_percentages > 1)
    ].tolist()
)


# In[597]:


demographic_sums = (
    demographics_df[
        demographics_df["percentage"].map(type) != str
    ]
    .groupby(["post_url", "category"])["percentage"]
    .sum()
    .reset_index(name="percentage_sum")
)

print("Post-category combinations:", len(demographic_sums))

print("\nPercentage sum statistics:")
print(demographic_sums["percentage_sum"].describe())

print("\nSample sums:")
print(demographic_sums.head(20).to_string(index=False))


# In[598]:


duplicate_demo_rows = demographics_df.duplicated(
    subset=["post_url", "category", "value", "percentage"],
    keep=False
)

print("Duplicate demographic rows:", duplicate_demo_rows.sum())

print("\nDuplicate demographic groups:")
print(
    demographics_df[
        duplicate_demo_rows
    ]
    .groupby(["post_url", "category", "value", "percentage"])
    .size()
    .reset_index(name="row_count")
    .sort_values("row_count", ascending=False)
    .head(20)
    .to_string(index=False)
)


# In[599]:


repeated_post_files = (
    url_validation_df[
        url_validation_df["post_url"].isin(
            url_validation_df["post_url"]
            .value_counts()
            .loc[lambda x: x > 1]
            .index
        )
    ]
    .groupby("post_url")
    .agg(
        source_file_count=("file_name", "nunique")
    )
    .reset_index()
)

print("Repeated posts:", len(repeated_post_files))

print("\nSource-file count per repeated post:")
print(
    repeated_post_files["source_file_count"]
    .value_counts()
    .sort_index()
)

print("\nMaximum source files for one post:")
print(repeated_post_files["source_file_count"].max())


# In[600]:


print("Canonical PostAnalytics files:", len(
    source_files_df[
        source_files_df["source_type"] == "PostAnalytics"
    ]
))

print("Canonical SinglePostAnalytics files:", len(
    source_files_df[
        source_files_df["source_type"] == "SinglePostAnalytics"
    ]
))

print("\nPostAnalytics sheet counts:")
print(
    postanalytics_read_check["sheet_count"]
    .value_counts()
    .sort_index()
)


# In[601]:


postanalytics_fields = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    fields = (
        df.iloc[:, 0]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    postanalytics_fields.extend(fields)

unique_postanalytics_fields = sorted(
    set(postanalytics_fields)
)

print("Unique PERFORMANCE field names:", len(unique_postanalytics_fields))

print("\nField names:")
for field in unique_postanalytics_fields:
    print("-", field)


# In[602]:


field_frequency = (
    pd.Series(postanalytics_fields)
    .value_counts()
    .reset_index()
)

field_frequency.columns = [
    "field_name",
    "file_count"
]

print("Field frequency:")
print(
    field_frequency
    .to_string(index=False)
)


# In[603]:


impressions_missing_files = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    fields = (
        df.iloc[:, 0]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    if "Impressions" not in fields:
        impressions_missing_files.append(file_name)

print("Files without 'Impressions':", len(impressions_missing_files))

print("\nFiles:")
for file_name in impressions_missing_files:
    print("-", file_name)


# In[604]:


for file_name in impressions_missing_files:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    print("\n" + "=" * 80)
    print("FILE:", file_name)
    print("=" * 80)

    print("\nFields:")
    print(
        df.iloc[:, 0]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    print("\nRaw data:")
    print(df.to_string(index=False))


# In[605]:


alias_check = {
    "comments": ["Comments", "Comment"],
    "reposts": ["Reposts", "Repost"]
}

for metric, aliases in alias_check.items():

    missing_files = []

    for file_name in source_files_df[
        source_files_df["source_type"] == "PostAnalytics"
    ]["file_name"]:

        df = pd.read_excel(
            raw_folder / file_name,
            sheet_name="PERFORMANCE"
        )

        fields = (
            df.iloc[:, 0]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        if not any(alias in fields for alias in aliases):
            missing_files.append(file_name)

    print(f"{metric}:")
    print(f"  Files with neither alias: {len(missing_files)}")
    print()


# In[606]:


for metric, aliases in alias_check.items():

    missing_files = []

    for file_name in source_files_df[
        source_files_df["source_type"] == "PostAnalytics"
    ]["file_name"]:

        file_path = raw_folder / file_name

        df = pd.read_excel(
            file_path,
            sheet_name="PERFORMANCE"
        )

        fields = (
            df.iloc[:, 0]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        if not any(alias in fields for alias in aliases):
            missing_files.append(file_name)

    print("\n" + "=" * 80)
    print(metric.upper(), "— FILES WITHOUT METRIC")
    print("=" * 80)

    for file_name in missing_files:
        print("-", file_name)


# In[607]:


for file_name in impressions_missing_files:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    print("\n" + "=" * 80)
    print("FILE:", file_name)
    print("=" * 80)

    print("\nFields:")
    print(
        df.iloc[:, 0]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    print("\nRaw data:")
    print(df.to_string(index=False))


# In[608]:


for file_name in [
    "PostAnalytics_ShifaNaaz_7115217803229474816.xlsx",
    "PostAnalytics_ShifaNaaz_7214254321746477056 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7226972231543799808 - Copy.xlsx"
]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    print("\n" + "=" * 80)
    print("FILE:", file_name)
    print("=" * 80)

    print("\nFields:")
    print(
        df.iloc[:, 0]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    print("\nRaw data:")
    print(df.to_string(index=False))


# In[609]:


reposts_missing_files = [
    "PostAnalytics_ShifaNaaz_7089201422558240769.xlsx",
    "PostAnalytics_ShifaNaaz_7115217803229474816.xlsx",
    "PostAnalytics_ShifaNaaz_7175918502392856576 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7177703654102118402 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7186372032723333120 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7196527586137501696 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7196544386292191233 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7201963130657120261 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7214254321746477056 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7221519605909929985 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7223905460532170752 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7226972231543799808 - Copy.xlsx",
    "PostAnalytics_ShifaNaaz_7233094257358557185 - Copy.xlsx"
]

for file_name in reposts_missing_files:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    print("\n" + "=" * 80)
    print("FILE:", file_name)
    print("=" * 80)

    print("\nFields:")
    print(
        df.iloc[:, 0]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )


# In[610]:



single_core_fields = [
    "Post Date",
    "Post Publish Time",
    "Impressions",
    "Reactions",
    "Comments",
    "Comment",
    "Reposts",
    "Repost"
]

single_field_check = []

for file_name in source_files_df[
    source_files_df["source_type"] == "SinglePostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="Post analytics"
    )

    fields = set(
        df.iloc[:, 0]
        .dropna()
        .astype(str)
        .str.strip()
    )

    row = {"file_name": file_name}

    for field in single_core_fields:
        row[field] = field in fields

    single_field_check.append(row)

single_field_check_df = pd.DataFrame(single_field_check)

print("Files tested:", len(single_field_check_df))

print("\nField availability:")
print(
    single_field_check_df[
        single_core_fields
    ].sum()
)

print("\nFields missing in at least one file:")

for field in single_core_fields:
    missing_count = (
        ~single_field_check_df[field]
    ).sum()

    if missing_count > 0:
        print(
            f"- {field}: missing in {missing_count} files"
        )


# In[611]:


single_optional_fields = [
    "Profile viewers from this post",
    "Followers gained from this post",
    "Saves",
    "Sends on LinkedIn",
    "Link engagements",
    "Premium custom button engagements",
    "Members reached",
    "Video views",
    "Watch time",
    "Average watch time"
]

single_optional_check = []

for file_name in source_files_df[
    source_files_df["source_type"] == "SinglePostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="Post analytics"
    )

    fields = set(
        df.iloc[:, 0]
        .dropna()
        .astype(str)
        .str.strip()
    )

    row = {"file_name": file_name}

    for field in single_optional_fields:
        row[field] = field in fields

    single_optional_check.append(row)

single_optional_check_df = pd.DataFrame(
    single_optional_check
)

print("Files tested:", len(single_optional_check_df))

print("\nOptional field availability:")
print(
    single_optional_check_df[
        single_optional_fields
    ].sum()
)

print("\nFields missing in at least one file:")

for field in single_optional_fields:
    missing_count = (
        ~single_optional_check_df[field]
    ).sum()

    if missing_count > 0:
        print(
            f"- {field}: missing in {missing_count} files"
        )


# In[612]:


single_core_value_types = []

for file_name in source_files_df[
    source_files_df["source_type"] == "SinglePostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="Post analytics"
    )

    for field in [
        "Impressions",
        "Reactions",
        "Comments",
        "Reposts"
    ]:

        value = get_field_value(df, field)

        single_core_value_types.append({
            "file_name": file_name,
            "field": field,
            "value": value,
            "python_type": type(value).__name__
        })

single_core_value_types_df = pd.DataFrame(
    single_core_value_types
)

print("Value type distribution:")

print(
    single_core_value_types_df
    .groupby(["field", "python_type"])
    .size()
    .reset_index(name="count")
    .to_string(index=False)
)


# In[613]:


postanalytics_core_value_types = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    for field in [
        "Impressions",
        "Total Impressions",
        "Reactions",
        "Comments",
        "Comment",
        "Reposts",
        "Repost"
    ]:

        value = get_field_value(df, field)

        if value is not None:

            postanalytics_core_value_types.append({
                "file_name": file_name,
                "field": field,
                "value": value,
                "python_type": type(value).__name__
            })

postanalytics_core_value_types_df = pd.DataFrame(
    postanalytics_core_value_types
)

print("Value type distribution:")

print(
    postanalytics_core_value_types_df
    .groupby(["field", "python_type"])
    .size()
    .reset_index(name="count")
    .to_string(index=False)
)


# In[614]:


def standardize_numeric(value):
    """
    Convert a LinkedIn metric value into a numeric value.

    Missing values remain None.
    Numeric strings are converted to numbers.
    Unexpected non-numeric values raise an error.
    """

    if value is None or pd.isna(value):
        return None

    try:
        return int(float(str(value).strip()))
    except (ValueError, TypeError):
        raise ValueError(
            f"Unable to convert value to numeric: {value!r}"
        )


# In[615]:


test_values = [
    "653",
    "13",
    "0",
    565,
    None
]

for value in test_values:
    print(
        repr(value),
        "→",
        standardize_numeric(value),
        "|",
        type(standardize_numeric(value)).__name__
    )


# In[616]:


standardization_test = []

for _, row in postanalytics_core_value_types_df.iterrows():

    try:
        standardized_value = standardize_numeric(row["value"])

        standardization_test.append({
            "file_name": row["file_name"],
            "field": row["field"],
            "raw_value": row["value"],
            "standardized_value": standardized_value,
            "status": "OK"
        })

    except Exception as e:

        standardization_test.append({
            "file_name": row["file_name"],
            "field": row["field"],
            "raw_value": row["value"],
            "standardized_value": None,
            "status": "ERROR"
        })

standardization_test_df = pd.DataFrame(standardization_test)

print(
    standardization_test_df["status"]
    .value_counts()
)


# In[617]:


print(
    standardization_test_df[
        standardization_test_df["status"] == "ERROR"
    ][
        ["file_name", "field", "raw_value"]
    ].to_string(index=False)
)


# In[618]:


def standardize_numeric(value):
    """
    Convert a LinkedIn metric value into a numeric value.

    Missing values remain None.
    Numeric strings with thousands separators are supported.
    Unexpected non-numeric values raise an error.
    """

    if value is None or pd.isna(value):
        return None

    try:
        cleaned_value = str(value).strip().replace(",", "")
        return int(float(cleaned_value))
    except (ValueError, TypeError):
        raise ValueError(
            f"Unable to convert value to numeric: {value!r}"
        )


# In[619]:


standardization_test = []

for _, row in postanalytics_core_value_types_df.iterrows():

    try:
        standardized_value = standardize_numeric(row["value"])

        standardization_test.append({
            "file_name": row["file_name"],
            "field": row["field"],
            "raw_value": row["value"],
            "standardized_value": standardized_value,
            "status": "OK"
        })

    except Exception as e:

        standardization_test.append({
            "file_name": row["file_name"],
            "field": row["field"],
            "raw_value": row["value"],
            "standardized_value": None,
            "status": "ERROR"
        })

standardization_test_df = pd.DataFrame(standardization_test)

print(
    standardization_test_df["status"]
    .value_counts()
)


# In[620]:


single_core_standardization_test = []

for _, row in single_core_value_types_df.iterrows():

    try:
        standardized_value = standardize_numeric(row["value"])

        single_core_standardization_test.append({
            "file_name": row["file_name"],
            "field": row["field"],
            "raw_value": row["value"],
            "standardized_value": standardized_value,
            "status": "OK"
        })

    except Exception:
        single_core_standardization_test.append({
            "file_name": row["file_name"],
            "field": row["field"],
            "raw_value": row["value"],
            "standardized_value": None,
            "status": "ERROR"
        })

single_core_standardization_test_df = pd.DataFrame(
    single_core_standardization_test
)

print(
    single_core_standardization_test_df["status"]
    .value_counts()
)


# In[621]:


postanalytics_date_values = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(df, "Post Date")

    postanalytics_date_values.append({
        "file_name": file_name,
        "raw_post_date": value,
        "python_type": type(value).__name__
    })

postanalytics_date_values_df = pd.DataFrame(
    postanalytics_date_values
)

print(
    postanalytics_date_values_df[
        ["python_type"]
    ].value_counts()
)

print("\nSample values:")
print(
    postanalytics_date_values_df[
        ["raw_post_date", "python_type"]
    ]
    .drop_duplicates()
    .head(20)
    .to_string(index=False)
)


# In[622]:


postanalytics_publish_time_types = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        "Post Publish Time"
    )

    postanalytics_publish_time_types.append({
        "file_name": file_name,
        "raw_publish_time": value,
        "python_type": type(value).__name__
    })

postanalytics_publish_time_types_df = pd.DataFrame(
    postanalytics_publish_time_types
)

print(
    postanalytics_publish_time_types_df[
        "python_type"
    ].value_counts()
)

print("\nSample values:")
print(
    postanalytics_publish_time_types_df[
        ["raw_publish_time", "python_type"]
    ].head(20).to_string(index=False)
)


# In[623]:


postanalytics_core_types = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    for field in [
        "Impressions",
        "Total Impressions",
        "Reactions",
        "Comments",
        "Comment",
        "Reposts",
        "Repost"
    ]:

        value = get_field_value(df, field)

        if value is not None:

            postanalytics_core_types.append({
                "file_name": file_name,
                "field": field,
                "value": value,
                "python_type": type(value).__name__
            })

postanalytics_core_types_df = pd.DataFrame(
    postanalytics_core_types
)

print("Value type distribution:")

print(
    postanalytics_core_types_df
    .groupby(["field", "python_type"])
    .size()
    .reset_index(name="count")
    .to_string(index=False)
)


# In[624]:


postanalytics_date_types = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(df, "Post Date")

    postanalytics_date_types.append({
        "file_name": file_name,
        "value": value,
        "python_type": type(value).__name__
    })

postanalytics_date_types_df = pd.DataFrame(
    postanalytics_date_types
)

print("Post Date value type distribution:")

print(
    postanalytics_date_types_df
    .groupby("python_type")
    .size()
    .reset_index(name="count")
    .to_string(index=False)
)

print("\nSample values:")

print(
    postanalytics_date_types_df[
        ["value", "python_type"]
    ].head(20).to_string(index=False)
)


# In[625]:


single_post_date_types = []

for file_name in source_files_df[
    source_files_df["source_type"] == "SinglePostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="Post analytics"
    )

    value = get_field_value(df, "Post Date")

    single_post_date_types.append({
        "file_name": file_name,
        "value": value,
        "python_type": type(value).__name__
    })

single_post_date_types_df = pd.DataFrame(
    single_post_date_types
)

print("SinglePostAnalytics Post Date type distribution:")

print(
    single_post_date_types_df
    .groupby("python_type")
    .size()
    .reset_index(name="count")
    .to_string(index=False)
)

print("\nSample values:")

print(
    single_post_date_types_df[
        ["value", "python_type"]
    ].head(20).to_string(index=False)
)


# In[626]:


postanalytics_publish_time_types = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        "Post Publish Time"
    )

    postanalytics_publish_time_types.append({
        "file_name": file_name,
        "raw_publish_time": value,
        "python_type": type(value).__name__
    })

postanalytics_publish_time_types_df = pd.DataFrame(
    postanalytics_publish_time_types
)

print(
    postanalytics_publish_time_types_df[
        "python_type"
    ].value_counts()
)

print("\nSample values:")
print(
    postanalytics_publish_time_types_df[
        ["raw_publish_time", "python_type"]
    ].head(20).to_string(index=False)
)


# In[627]:


single_publish_time_types = []

for file_name in source_files_df[
    source_files_df["source_type"] == "SinglePostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(file_path)

    value = get_field_value(
        df,
        "Post Publish Time"
    )

    single_publish_time_types.append({
        "file_name": file_name,
        "raw_publish_time": value,
        "python_type": type(value).__name__
    })

single_publish_time_types_df = pd.DataFrame(
    single_publish_time_types
)

print(
    single_publish_time_types_df[
        "python_type"
    ].value_counts()
)

print("\nSample values:")
print(
    single_publish_time_types_df[
        ["raw_publish_time", "python_type"]
    ].head(20).to_string(index=False)
)


# In[628]:


postanalytics_impressions_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        ["Impressions", "Total Impressions"]
    )

    postanalytics_impressions_profile.append({
        "file_name": file_name,
        "raw_impressions": value,
        "python_type": type(value).__name__
    })

postanalytics_impressions_profile_df = pd.DataFrame(
    postanalytics_impressions_profile
)

print("Value type distribution:")
print(
    postanalytics_impressions_profile_df[
        "python_type"
    ].value_counts()
)

print("\nUnique raw values (first 30):")
print(
    postanalytics_impressions_profile_df[
        "raw_impressions"
    ].dropna().unique()[:30]
)


# In[629]:


postanalytics_reactions_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        "Reactions"
    )

    postanalytics_reactions_profile.append({
        "file_name": file_name,
        "raw_reactions": value,
        "python_type": type(value).__name__
    })

postanalytics_reactions_profile_df = pd.DataFrame(
    postanalytics_reactions_profile
)

print("Value type distribution:")
print(
    postanalytics_reactions_profile_df[
        "python_type"
    ].value_counts()
)

print("\nUnique raw values (first 30):")
print(
    postanalytics_reactions_profile_df[
        "raw_reactions"
    ].dropna().unique()[:30]
)


# In[630]:


postanalytics_comments_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        ["Comments", "Comment"]
    )

    postanalytics_comments_profile.append({
        "file_name": file_name,
        "raw_comments": value,
        "python_type": type(value).__name__
    })

postanalytics_comments_profile_df = pd.DataFrame(
    postanalytics_comments_profile
)

print("Value type distribution:")
print(
    postanalytics_comments_profile_df[
        "python_type"
    ].value_counts()
)

print("\nMissing values:")
print(
    postanalytics_comments_profile_df[
        "raw_comments"
    ].isna().sum()
)

print("\nUnique raw values:")
print(
    postanalytics_comments_profile_df[
        "raw_comments"
    ].dropna().unique()
)


# In[631]:


postanalytics_reposts_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        ["Reposts", "Repost"]
    )

    postanalytics_reposts_profile.append({
        "file_name": file_name,
        "raw_reposts": value,
        "python_type": type(value).__name__
    })

postanalytics_reposts_profile_df = pd.DataFrame(
    postanalytics_reposts_profile
)

print("Value type distribution:")
print(
    postanalytics_reposts_profile_df[
        "python_type"
    ].value_counts()
)

print("\nMissing values:")
print(
    postanalytics_reposts_profile_df[
        "raw_reposts"
    ].isna().sum()
)

print("\nUnique raw values:")
print(
    postanalytics_reposts_profile_df[
        "raw_reposts"
    ].dropna().unique()
)


# In[632]:


postanalytics_unique_views_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        "Unique views"
    )

    postanalytics_unique_views_profile.append({
        "file_name": file_name,
        "raw_unique_views": value,
        "python_type": type(value).__name__
    })

postanalytics_unique_views_profile_df = pd.DataFrame(
    postanalytics_unique_views_profile
)

print("Value type distribution:")
print(
    postanalytics_unique_views_profile_df[
        "python_type"
    ].value_counts()
)

print("\nMissing values:")
print(
    postanalytics_unique_views_profile_df[
        "raw_unique_views"
    ].isna().sum()
)

print("\nUnique raw values:")
print(
    postanalytics_unique_views_profile_df[
        "raw_unique_views"
    ].dropna().unique()
)


# In[633]:


postanalytics_profile_viewers_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        "Profile viewers from this post"
    )

    postanalytics_profile_viewers_profile.append({
        "file_name": file_name,
        "raw_profile_viewers": value,
        "python_type": type(value).__name__
    })

postanalytics_profile_viewers_profile_df = pd.DataFrame(
    postanalytics_profile_viewers_profile
)

print("Value type distribution:")
print(
    postanalytics_profile_viewers_profile_df[
        "python_type"
    ].value_counts()
)

print("\nMissing values:")
print(
    postanalytics_profile_viewers_profile_df[
        "raw_profile_viewers"
    ].isna().sum()
)

print("\nUnique raw values:")
print(
    postanalytics_profile_viewers_profile_df[
        "raw_profile_viewers"
    ].dropna().unique()
)


# In[634]:


postanalytics_followers_gained_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        "Followers gained from this post"
    )

    postanalytics_followers_gained_profile.append({
        "file_name": file_name,
        "raw_followers_gained": value,
        "python_type": type(value).__name__
    })

postanalytics_followers_gained_profile_df = pd.DataFrame(
    postanalytics_followers_gained_profile
)

print("Value type distribution:")
print(
    postanalytics_followers_gained_profile_df[
        "python_type"
    ].value_counts()
)

print("\nMissing values:")
print(
    postanalytics_followers_gained_profile_df[
        "raw_followers_gained"
    ].isna().sum()
)

print("\nUnique raw values:")
print(
    postanalytics_followers_gained_profile_df[
        "raw_followers_gained"
    ].dropna().unique()
)


# In[635]:


postanalytics_saves_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        "Saves"
    )

    postanalytics_saves_profile.append({
        "file_name": file_name,
        "raw_saves": value,
        "python_type": type(value).__name__
    })

postanalytics_saves_profile_df = pd.DataFrame(
    postanalytics_saves_profile
)

print("Value type distribution:")
print(
    postanalytics_saves_profile_df[
        "python_type"
    ].value_counts()
)

print("\nMissing values:")
print(
    postanalytics_saves_profile_df[
        "raw_saves"
    ].isna().sum()
)

print("\nUnique raw values:")
print(
    postanalytics_saves_profile_df[
        "raw_saves"
    ].dropna().unique()
)


# In[636]:


postanalytics_sends_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        "Sends on LinkedIn"
    )

    postanalytics_sends_profile.append({
        "file_name": file_name,
        "raw_sends_on_linkedin": value,
        "python_type": type(value).__name__
    })

postanalytics_sends_profile_df = pd.DataFrame(
    postanalytics_sends_profile
)

print("Value type distribution:")
print(
    postanalytics_sends_profile_df[
        "python_type"
    ].value_counts()
)

print("\nMissing values:")
print(
    postanalytics_sends_profile_df[
        "raw_sends_on_linkedin"
    ].isna().sum()
)

print("\nUnique raw values:")
print(
    postanalytics_sends_profile_df[
        "raw_sends_on_linkedin"
    ].dropna().unique()
)


# In[637]:


postanalytics_members_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        "Members reached"
    )

    postanalytics_members_profile.append({
        "file_name": file_name,
        "raw_members_reached": value,
        "python_type": type(value).__name__
    })

postanalytics_members_profile_df = pd.DataFrame(
    postanalytics_members_profile
)

print("Value type distribution:")
print(
    postanalytics_members_profile_df[
        "python_type"
    ].value_counts()
)

print("\nMissing values:")
print(
    postanalytics_members_profile_df[
        "raw_members_reached"
    ].isna().sum()
)

print("\nUnique raw values:")
print(
    postanalytics_members_profile_df[
        "raw_members_reached"
    ].dropna().unique()
)


# In[638]:


postanalytics_profile_viewers_profile_df


# In[639]:


postanalytics_profile_viewers_profile = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE"
    )

    value = get_field_value(
        df,
        "Profile viewers from this post"
    )

    postanalytics_profile_viewers_profile.append({
        "file_name": file_name,
        "raw_profile_viewers": value,
        "python_type": type(value).__name__
    })

postanalytics_profile_viewers_profile_df = pd.DataFrame(
    postanalytics_profile_viewers_profile
)

print("Value type distribution:")
print(
    postanalytics_profile_viewers_profile_df[
        "python_type"
    ].value_counts()
)

print("\nMissing values:")
print(
    postanalytics_profile_viewers_profile_df[
        "raw_profile_viewers"
    ].isna().sum()
)

print("\nUnique raw values:")
print(
    postanalytics_profile_viewers_profile_df[
        "raw_profile_viewers"
    ].dropna().unique()
)


# In[640]:


# Show variables currently available that may contain PostAnalytics data

[var_name for var_name in globals() if "post" in var_name.lower()]


# In[641]:


#Next — inspect postanalytics_files


# In[642]:


type(postanalytics_files), len(postanalytics_files), postanalytics_files[:3]


# In[643]:


print(postanalytics_profile_viewers_profile_df.head(20).to_string(index=False))


# In[644]:


# Inspect the PERFORMANCE sheet from one PostAnalytics file

sample_file = source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"].iloc[0]

sample_path = raw_folder / sample_file

sample_performance_df = pd.read_excel(
    sample_path,
    sheet_name="PERFORMANCE",
    header=None
)

print("Sample file:")
print(sample_file)

print("\nShape:")
print(sample_performance_df.shape)

print("\nFirst 30 rows:")
print(sample_performance_df.head(30).to_string(index=False))


# In[645]:


# Check which PostAnalytics files actually contain
# "Profile viewers from this post"

profile_viewers_presence = []

for file_name in source_files_df[
    source_files_df["source_type"] == "PostAnalytics"
]["file_name"]:

    file_path = raw_folder / file_name

    df = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE",
        header=None
    )

    # Convert all cells to strings for a robust field-name search
    all_values = df.astype(str).apply(
        lambda col: col.str.strip()
    )

    found = all_values.eq(
        "Profile viewers from this post"
    ).any().any()

    profile_viewers_presence.append({
        "file_name": file_name,
        "profile_viewers_field_present": found
    })

profile_viewers_presence_df = pd.DataFrame(
    profile_viewers_presence
)

print(
    profile_viewers_presence_df[
        "profile_viewers_field_present"
    ].value_counts()
)

print("\nFiles where the field is present:")

print(
    profile_viewers_presence_df[
        profile_viewers_presence_df[
            "profile_viewers_field_present"
        ]
    ]["file_name"].to_string(index=False)
)


# In[646]:


# Inspect the PERFORMANCE sheet from a file
# where "Profile viewers from this post" is confirmed to exist

profile_viewer_file = profile_viewers_presence_df[
    profile_viewers_presence_df["profile_viewers_field_present"]
]["file_name"].iloc[0]

profile_viewer_path = raw_folder / profile_viewer_file

profile_viewer_sample_df = pd.read_excel(
    profile_viewer_path,
    sheet_name="PERFORMANCE",
    header=None
)

print("Sample file:")
print(profile_viewer_file)

print("\nShape:")
print(profile_viewer_sample_df.shape)

print("\nRaw PERFORMANCE sheet:")
print(
    profile_viewer_sample_df.to_string(index=False)
)


# In[647]:


import re

def extract_post_id(url):
    ids = re.findall(r"\d{19}", str(url))
    return ids[-1] if ids else None   # last 19-digit number; slug titles can contain other digits

url_id_df = url_validation_df.copy()
url_id_df["post_id"] = url_id_df["post_url"].map(extract_post_id)

print("Rows without a post_id:", url_id_df["post_id"].isna().sum())
print("Unique URL strings:", url_id_df["post_url"].nunique())
print("Unique post_ids:", url_id_df["post_id"].nunique())

print("\nSource types per post_id:")
print(
    url_id_df.groupby("post_id")["source_type"]
    .agg(lambda s: tuple(sorted(set(s))))
    .value_counts()
)


# In[648]:


overlap_ids = (
    url_id_df.groupby("post_id")["source_type"]
    .nunique()
    .loc[lambda s: s == 2]
    .index
)

rows = []
for _, r in url_id_df[url_id_df["post_id"].isin(overlap_ids)].iterrows():
    sheet = "PERFORMANCE" if r["source_type"] == "PostAnalytics" else "Post analytics"
    df = pd.read_excel(raw_folder / r["file_name"], sheet_name=sheet)
    rows.append({
        "post_id": r["post_id"],
        "source_type": r["source_type"],
        "post_date": get_field_value(df, "Post Date"),
        "publish_time": get_field_value(df, "Post Publish Time"),
        "impressions": get_field_value(df, ["Impressions", "Total Impressions"])
    })

overlap_check = pd.DataFrame(rows).sort_values(["post_id", "source_type"])
print("Rows:", len(overlap_check))
print(overlap_check.head(30).to_string(index=False))


# In[649]:


import warnings
warnings.filterwarnings("ignore", message="Workbook contains no default style")

oc = overlap_check.copy()
oc["impressions"] = oc["impressions"].map(standardize_numeric)

pa = oc[oc["source_type"] == "PostAnalytics"].copy()
sp = oc[oc["source_type"] == "SinglePostAnalytics"].copy()

pa["ts"] = pd.to_datetime(pa["post_date"].astype(str) + " " + pa["publish_time"].astype(str),
                          format="%b %d, %Y %I:%M %p")
sp["ts"] = pd.to_datetime(sp["post_date"].astype(str) + " " + sp["publish_time"].astype(str),
                          format="%m/%d/%Y %I:%M %p")

pa_one = pa.groupby("post_id").agg(
    pa_ts=("ts", "first"), pa_ts_distinct=("ts", "nunique"),
    pa_snapshots=("ts", "size"),
    pa_imp_min=("impressions", "min"), pa_imp_max=("impressions", "max"))
sp_one = sp.set_index("post_id")[["ts", "impressions"]].rename(
    columns={"ts": "sp_ts", "impressions": "sp_imp"})

cmp = pa_one.join(sp_one, how="inner")
cmp["time_gap"] = cmp["sp_ts"] - cmp["pa_ts"]

print("Posts compared:", len(cmp))
print("\nPostAnalytics rows per post with differing timestamps:", (cmp["pa_ts_distinct"] > 1).sum())
print("\nTime gap (SinglePost minus PostAnalytics):")
print(cmp["time_gap"].value_counts())
print("\nSinglePost impressions >= PostAnalytics max:", (cmp["sp_imp"] >= cmp["pa_imp_max"]).sum(), "of", len(cmp))
print("\nExceptions:")
print(cmp.loc[cmp["sp_imp"] < cmp["pa_imp_max"], ["pa_imp_min", "pa_imp_max", "sp_imp"]])


# In[650]:


def id_to_utc(post_id):
    return pd.to_datetime(int(post_id) >> 22, unit="ms").floor("min")

pa_ts = (postanalytics_date_types_df[["file_name", "value"]]
         .merge(postanalytics_publish_time_types_df[["file_name", "raw_publish_time"]], on="file_name"))
pa_ts["export_ts"] = pd.to_datetime(
    pa_ts["value"].astype(str) + " " + pa_ts["raw_publish_time"].astype(str),
    format="%b %d, %Y %I:%M %p")
pa_ts["source_type"] = "PostAnalytics"

sp_ts = (single_post_date_types_df[["file_name", "value"]]
         .merge(single_publish_time_types_df[["file_name", "raw_publish_time"]], on="file_name"))
sp_ts["export_ts"] = pd.to_datetime(
    sp_ts["value"].astype(str) + " " + sp_ts["raw_publish_time"].astype(str),
    format="%m/%d/%Y %I:%M %p")
sp_ts["source_type"] = "SinglePostAnalytics"

all_ts = (pd.concat([pa_ts, sp_ts])
          .merge(url_id_df[["file_name", "post_id"]], on="file_name"))
all_ts["id_utc"] = all_ts["post_id"].map(id_to_utc)
all_ts["offset"] = all_ts["export_ts"] - all_ts["id_utc"]

print("Files tested:", len(all_ts))
print(all_ts.groupby(["source_type", "offset"]).size())


# In[651]:


# Review timestamp alignment for both LinkedIn export types

timestamp_review = all_ts[
    [
        "file_name",
        "source_type",
        "post_id",
        "export_ts",
        "id_utc",
        "offset"
    ]
].copy()

print("PostAnalytics — examples:")
print(
    timestamp_review[
        timestamp_review["source_type"] == "PostAnalytics"
    ].head(5).to_string(index=False)
)

print("\nSinglePostAnalytics — examples:")
print(
    timestamp_review[
        timestamp_review["source_type"] == "SinglePostAnalytics"
    ].head(5).to_string(index=False)
)

print("\nPostAnalytics timestamp exceptions:")
print(
    timestamp_review[
        (timestamp_review["source_type"] == "PostAnalytics")
        & (timestamp_review["offset"] != pd.Timedelta(0))
    ].to_string(index=False)
)


# In[652]:


# Compare the post ID in each filename with the ID extracted from its post URL

filename_id_check = url_id_df[
    url_id_df["source_type"] == "SinglePostAnalytics"
].copy()

def extract_filename_id(filename):
    ids = re.findall(r"\d{19}", str(filename))
    return ids[-1] if ids else None

filename_id_check["filename_id"] = (
    filename_id_check["file_name"].map(extract_filename_id)
)

filename_id_check["id_matches"] = (
    filename_id_check["filename_id"]
    == filename_id_check["post_id"]
)

print("SinglePostAnalytics files checked:", len(filename_id_check))
print("\nFilename ID vs URL ID:")
print(filename_id_check["id_matches"].value_counts(dropna=False))

print("\nExamples where the IDs differ:")
print(
    filename_id_check.loc[
        filename_id_check["id_matches"] == False,
        ["file_name", "filename_id", "post_id", "post_url"]
    ].head(10).to_string(index=False)
)


# In[653]:


# Compare timestamps encoded in filename IDs and URL IDs

filename_id_check["filename_id_utc"] = (
    filename_id_check["filename_id"]
    .map(id_to_utc)
)

filename_id_check["url_id_utc"] = (
    filename_id_check["post_id"]
    .map(id_to_utc)
)

print(
    filename_id_check[
        [
            "file_name",
            "filename_id",
            "post_id",
            "filename_id_utc",
            "url_id_utc"
        ]
    ].head(10).to_string(index=False)
)

print("\nDifference between encoded timestamps:")
print(
    (
        filename_id_check["filename_id_utc"]
        - filename_id_check["url_id_utc"]
    ).describe()
)


# In[654]:


# Function: decode the publish time hidden inside a LinkedIn post ID
# (shifting the ID right by 22 bits gives milliseconds since 1970, in UTC)
def id_to_utc(post_id):
    return pd.to_datetime(int(post_id) >> 22, unit="ms").floor("min")

# ---- PostAnalytics files: build the exported publish timestamp ----
# Join the date table and the time table using the file name
pa_ts = (postanalytics_date_types_df[["file_name", "value"]]
         .merge(postanalytics_publish_time_types_df[["file_name", "raw_publish_time"]], on="file_name"))
# Combine date + time text into one timestamp (format like "Apr 16, 2025 10:50 AM")
pa_ts["export_ts"] = pd.to_datetime(
    pa_ts["value"].astype(str) + " " + pa_ts["raw_publish_time"].astype(str),
    format="%b %d, %Y %I:%M %p")
pa_ts["source_type"] = "PostAnalytics"

# ---- SinglePostAnalytics files: same steps, different date format ----
sp_ts = (single_post_date_types_df[["file_name", "value"]]
         .merge(single_publish_time_types_df[["file_name", "raw_publish_time"]], on="file_name"))
# Date format here is month/day/year (like "4/16/2025 4:20 PM")
sp_ts["export_ts"] = pd.to_datetime(
    sp_ts["value"].astype(str) + " " + sp_ts["raw_publish_time"].astype(str),
    format="%m/%d/%Y %I:%M %p")
sp_ts["source_type"] = "SinglePostAnalytics"

# ---- Combine both types and attach the post_id for each file ----
all_ts = (pd.concat([pa_ts, sp_ts])
          .merge(url_id_df[["file_name", "post_id"]], on="file_name"))

# Decode the real UTC publish time from the post_id
all_ts["id_utc"] = all_ts["post_id"].map(id_to_utc)

# Difference between the exported time and the decoded UTC time
all_ts["offset"] = all_ts["export_ts"] - all_ts["id_utc"]

# Show how many files have each offset, split by file type
print("Files tested:", len(all_ts))
print(all_ts.groupby(["source_type", "offset"]).size())


# In[655]:


# Find the 2 PostAnalytics files where the offset is 1 minute (not exactly 0)
odd = all_ts[all_ts["offset"] == pd.Timedelta(minutes=1)].copy()

# Decode the post_id again, this time WITHOUT rounding down to the minute,
# so we can see the exact seconds hidden in the ID
odd["id_utc_exact"] = odd["post_id"].map(
    lambda x: pd.to_datetime(int(x) >> 22, unit="ms")
)

# Show the exported time next to the exact decoded time
print(odd[["file_name", "post_id", "export_ts", "id_utc_exact"]].to_string(index=False))


# In[656]:


# Decode every post_id again WITHOUT rounding, so we keep the exact seconds
all_ts["id_utc_exact"] = all_ts["post_id"].map(
    lambda x: pd.to_datetime(int(x) >> 22, unit="ms")
)

# Take only the seconds part of the decoded time
all_ts["id_seconds"] = all_ts["id_utc_exact"].dt.second

# Put seconds into three groups: 0-29, 30-49 and 50-59
all_ts["sec_bucket"] = pd.cut(
    all_ts["id_seconds"], bins=[-1, 29, 49, 59],
    labels=["0-29s", "30-49s", "50-59s"]
)

# Count files by file type, seconds group and offset
print(all_ts.groupby(["source_type", "sec_bucket", "offset"], observed=True).size())


# In[657]:


# Copy the field inventory (one row per field name per file)
fields = postanalytics_field_inventory_df.copy()

# Look for text like "to Jan 18, 2026" inside each field name and pull out the date part
fields["end_text"] = fields["field_name"].str.extract(
    r"to\s+([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})"
)

# Keep only the rows where a date was found, and turn the text into a real date
dated = fields.dropna(subset=["end_text"]).copy()
dated["end_date"] = pd.to_datetime(dated["end_text"], format="%b %d, %Y")

# For each file, find the earliest, latest and number of distinct end dates
file_export = (dated.groupby("file_name")["end_date"]
               .agg(["min", "max", "nunique"]).reset_index())

# How many files have a date, and do any have more than one?
print("Files with a Highlights date:", len(file_export), "of", fields["file_name"].nunique())
print("Files with more than one distinct end date:", (file_export["nunique"] > 1).sum())

# Which dates appear, and how many files share each one
print(file_export["max"].value_counts().sort_index())


# In[658]:


import warnings
# Hide the repeated openpyxl style warning (it is harmless)
warnings.filterwarnings("ignore", message="Workbook contains no default style")

# Take the file names of the 118 canonical PostAnalytics files
pa_files = all_ts.loc[all_ts["source_type"] == "PostAnalytics", "file_name"]

# Collect every field name (first column) from each file's PERFORMANCE sheet
rows = []
for file_name in pa_files:
    # header=None so the first row is treated as data, not as column names
    df = pd.read_excel(raw_folder / file_name, sheet_name="PERFORMANCE", header=None)
    # Go through each label in column A, skipping empty cells
    for value in df.iloc[:, 0].dropna():
        field_name = str(value).strip()
        if field_name:
            rows.append({"file_name": file_name, "field_name": field_name})

# Turn the list into a DataFrame
postanalytics_field_inventory_df = pd.DataFrame(rows)

# Quick checks: how many files and how many different field names
print("Files:", postanalytics_field_inventory_df["file_name"].nunique())
print("Unique field names:", postanalytics_field_inventory_df["field_name"].nunique())


# In[659]:


# Quick check: does "Post URL" appear as a field in all 118 files?
# (this would explain 127 field names instead of 126)
url_files = postanalytics_field_inventory_df.loc[
    postanalytics_field_inventory_df["field_name"] == "Post URL", "file_name"
].nunique()
print("Files with a 'Post URL' field:", url_files)

# Copy the field inventory (one row per field name per file)
fields = postanalytics_field_inventory_df.copy()

# Look for text like "to Jan 18, 2026" inside each field name and pull out the date part
fields["end_text"] = fields["field_name"].str.extract(
    r"to\s+([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})"
)

# Keep only the rows where a date was found, and turn the text into a real date
dated = fields.dropna(subset=["end_text"]).copy()
dated["end_date"] = pd.to_datetime(dated["end_text"], format="%b %d, %Y")

# For each file, find the earliest, latest and number of distinct end dates
file_export = (dated.groupby("file_name")["end_date"]
               .agg(["min", "max", "nunique"]).reset_index())

# How many files have a date, and do any have more than one?
print("Files with a Highlights date:", len(file_export), "of", fields["file_name"].nunique())
print("Files with more than one distinct end date:", (file_export["nunique"] > 1).sum())

# Which dates appear, and how many files share each one
print(file_export["max"].value_counts().sort_index())


# In[660]:


import os

# Start from the canonical PostAnalytics files and their post_id
pa_map = url_id_df[
    (url_id_df["source_type"] == "PostAnalytics") & (url_id_df["file_name"].isin(pa_files))
]

# Find post_ids that have more than one canonical file (repeat snapshots)
multi_ids = (pa_map.groupby("post_id")["file_name"].nunique()
             .loc[lambda s: s > 1].index)
print("Posts with more than one canonical file:", len(multi_ids))

# For each of those files, read impressions and the file's modified time
rows = []
for _, r in pa_map[pa_map["post_id"].isin(multi_ids)].iterrows():
    path = raw_folder / r["file_name"]
    df = pd.read_excel(path, sheet_name="PERFORMANCE")
    rows.append({
        "post_id": r["post_id"],
        "file_name": r["file_name"],
        "impressions": standardize_numeric(get_field_value(df, ["Impressions", "Total Impressions"])),
        "file_modified": pd.to_datetime(os.path.getmtime(path), unit="s").date(),
    })
snap = pd.DataFrame(rows)

# Add the Highlights end date (empty if the file has none)
snap = snap.merge(file_export[["file_name", "max"]].rename(columns={"max": "highlights_end"}),
                  on="file_name", how="left")

# How many of these files have a Highlights date?
print("Files with a Highlights date:", snap["highlights_end"].notna().sum(), "of", len(snap))

# Show each post's files side by side, in order of impressions
print(snap.sort_values(["post_id", "impressions"])
          [["post_id", "impressions", "highlights_end", "file_modified"]]
          .to_string(index=False))


# In[661]:


import os

# Get the file names of the 40 SinglePostAnalytics files
sp_files = all_ts.loc[all_ts["source_type"] == "SinglePostAnalytics", "file_name"]

# Read each file's modified date (no need to open the Excel files)
sp_mtime = pd.Series({
    f: pd.to_datetime(os.path.getmtime(raw_folder / f), unit="s").date()
    for f in sp_files
})

# Count how many files share each modified date
print(sp_mtime.value_counts().sort_index())


# In[662]:


import openpyxl

# Read the "created" timestamp stored INSIDE each workbook (not the file-system date)
rows = []
for _, r in all_ts[["file_name", "source_type"]].iterrows():
    wb = openpyxl.load_workbook(raw_folder / r["file_name"], read_only=True)
    rows.append({
        "file_name": r["file_name"],
        "source_type": r["source_type"],
        "created": wb.properties.created,
    })
    wb.close()
meta = pd.DataFrame(rows)

# Keep only the date part (drop the time) so it can be compared with Highlights dates
meta["created_date"] = pd.to_datetime(meta["created"]).dt.normalize()

# Add the Highlights end date (empty for files without one)
meta = meta.merge(
    file_export[["file_name", "max"]].rename(columns={"max": "highlights_end"}),
    on="file_name", how="left",
)

# How many files have no created date at all?
print("Files with no created date:", meta["created"].isna().sum())

# Which created dates appear, and how many files of each type share them
print(meta.groupby(["source_type", "created_date"]).size())

# Where both dates exist, do they match?
both = meta.dropna(subset=["highlights_end"])
print("\nFiles with both dates:", len(both))
print("Created date equals Highlights end date:", (both["created_date"] == both["highlights_end"]).sum())

# Show the files where they do not match
print(both.loc[both["created_date"] != both["highlights_end"],
               ["file_name", "created_date", "highlights_end"]].to_string(index=False))


# In[663]:


# Add the full "created" timestamp (date AND time) to the repeat-snapshot table
snap2 = snap.merge(meta[["file_name", "created"]], on="file_name", how="left")

# Put each post's files in order: oldest export first
snap2 = snap2.sort_values(["post_id", "created"])

# For each post, check that impressions never go down as the export gets later
# (equal values are allowed, going down is not)
check = snap2.groupby("post_id")["impressions"].apply(
    lambda s: s.is_monotonic_increasing
)

print("Posts checked:", len(check))
print("Posts where impressions never go down over time:", check.sum())

# Show the files of any post that breaks the rule
bad = check[~check].index
print(snap2[snap2["post_id"].isin(bad)]
      [["post_id", "file_name", "created", "impressions"]].to_string(index=False))


# In[664]:


# Start from each file's source type and its internal created timestamp
manifest = (meta[["file_name", "source_type", "created"]]
            # Attach the post_id and URL for each file
            .merge(url_id_df[["file_name", "post_id", "post_url"]], on="file_name")
            # The created timestamp is our snapshot (export) time
            .rename(columns={"created": "snapshot_ts"}))

# Rank the files of each post: 1 = newest export
manifest["snapshot_rank"] = (manifest.groupby("post_id")["snapshot_ts"]
                             .rank(method="first", ascending=False))

# The newest snapshot of each post is the "current" one
manifest["is_current"] = manifest["snapshot_rank"] == 1

# Check 1: row counts (158 files, 107 posts, 107 current files)
print("Files:", len(manifest))
print("Posts:", manifest["post_id"].nunique())
print("Current files:", manifest["is_current"].sum())

# Check 2: which source type supplies the current snapshot?
print("\nCurrent snapshot by source type:")
print(manifest.loc[manifest["is_current"], "source_type"].value_counts())

# Check 3: posts where two files share the exact same snapshot timestamp (ties)
ties = manifest.groupby("post_id")["snapshot_ts"].apply(lambda s: s.duplicated().any())
print("\nPosts with tied snapshot timestamps:", ties.sum())


# In[665]:


# Find the post(s) where two files share the exact same snapshot timestamp
tied_posts = (manifest.groupby("post_id")["snapshot_ts"]
              .apply(lambda s: s.duplicated().any())
              .loc[lambda s: s].index)

# Show those files with their snapshot time, current flag and impressions
tied = (manifest[manifest["post_id"].isin(tied_posts)]
        .merge(snap[["file_name", "impressions"]], on="file_name", how="left"))
print(tied[["post_id", "file_name", "snapshot_ts", "is_current", "impressions"]]
      .to_string(index=False))


# In[666]:


# Mark files whose name contains "Copy" (manual copies are the less preferred file)
manifest["is_copy_name"] = manifest["file_name"].str.contains("Copy", case=False)

# Sort so the preferred file of each post comes first:
# newest snapshot, then non-copy before copy, then file name (keeps results repeatable)
manifest = manifest.sort_values(
    ["post_id", "snapshot_ts", "is_copy_name", "file_name"],
    ascending=[True, False, True, True]
)

# Rank within each post: the first row is rank 1, and rank 1 is the current snapshot
manifest["snapshot_rank"] = manifest.groupby("post_id").cumcount() + 1
manifest["is_current"] = manifest["snapshot_rank"] == 1

# Check 1: still 158 files, 107 posts and 107 current files?
print("Files:", len(manifest), "| Posts:", manifest["post_id"].nunique(),
      "| Current files:", manifest["is_current"].sum())

# Check 2: which file is current for the previously tied post?
print(manifest.loc[manifest["post_id"] == "6974940149876965376",
                   ["file_name", "snapshot_ts", "is_current"]].to_string(index=False))

# Check 3 (information only): how many current files have "Copy" in their name?
print("Current files with 'Copy' in the name:", manifest.loc[manifest["is_current"], "is_copy_name"].sum())


# In[667]:


# Full list of all 202 raw files with their post_id (not just the 158 canonical ones)
all_files = url_id_df[["file_name", "post_id", "source_type"]].copy()
all_files["is_copy_name"] = all_files["file_name"].str.contains("Copy", case=False)

# Take only the current files that have "Copy" in their name
cur_copy = manifest[manifest["is_current"] & manifest["is_copy_name"]].copy()

# For each post, count the non-copy files in the FULL raw list
noncopy_raw = all_files[~all_files["is_copy_name"]].groupby("post_id").size()
cur_copy["noncopy_in_raw"] = cur_copy["post_id"].map(noncopy_raw).fillna(0).astype(int)

# For each post, count the non-copy files that made it into the manifest (158 canonical files)
noncopy_manifest = manifest[~manifest["is_copy_name"]].groupby("post_id").size()
cur_copy["noncopy_in_manifest"] = cur_copy["post_id"].map(noncopy_manifest).fillna(0).astype(int)

# Count how many current copy files fall into each combination
print(cur_copy.groupby(["noncopy_in_raw", "noncopy_in_manifest"]).size())


# In[668]:


# Find current "Copy" files whose post also has a non-copy file in the manifest
copy_current = manifest[manifest["is_current"] & manifest["is_copy_name"]]
noncopy_manifest = manifest[~manifest["is_copy_name"]].groupby("post_id").size()
odd_ids = copy_current.loc[copy_current["post_id"].isin(noncopy_manifest.index), "post_id"]

# Show every file of that post with its snapshot time, current flag and impressions
odd_post = (manifest[manifest["post_id"].isin(odd_ids)]
            .merge(snap[["file_name", "impressions"]], on="file_name", how="left"))
print(odd_post[["post_id", "file_name", "snapshot_ts", "is_current", "impressions"]]
      .to_string(index=False))


# In[669]:


import warnings
# Hide the repeated openpyxl style warning (it is harmless)
warnings.filterwarnings("ignore", message="Workbook contains no default style")

# Which sheet to read for each source type
sheet_for = {"PostAnalytics": "PERFORMANCE", "SinglePostAnalytics": "Post analytics"}

long_rows = []      # one row per field (label + value)
section_rows = []   # one row per section title

for _, r in manifest.iterrows():
    # Read the sheet with no header row, so every row is kept as data
    df = pd.read_excel(raw_folder / r["file_name"],
                       sheet_name=sheet_for[r["source_type"]], header=None)
    section = None  # remember the latest section title (such as "Engagement")

    for _, row in df.iterrows():
        label = row.iloc[0]
        if pd.isna(label):
            continue                      # skip empty rows
        label = str(label).strip()
        # Column B holds the value, column C (if present) holds an extra value
        value = row.iloc[1] if df.shape[1] > 1 else None
        extra = row.iloc[2] if df.shape[1] > 2 else None

        if pd.isna(value):
            # A label with no value is treated as a section title
            section = label
            section_rows.append({"file_name": r["file_name"], "section": label})
        else:
            long_rows.append({
                "file_name": r["file_name"],
                "source_type": r["source_type"],
                "section": section,
                "label": label,
                "value_raw": value,
                "extra_raw": extra,
            })

raw_fields_long = pd.DataFrame(long_rows)
sections_df = pd.DataFrame(section_rows)

# Check 1: size of the long table and how many files it covers (expect 158)
print("Rows:", len(raw_fields_long), "| Files:", raw_fields_long["file_name"].nunique())

# Check 2: the section titles found, and how many files have each one
print("\nSection titles found:")
print(sections_df.groupby("section")["file_name"].nunique().sort_values(ascending=False))


# In[670]:


# Count how many files have each section title
sec_counts = sections_df.groupby("section")["file_name"].nunique()

# Group 1: normal section titles (no "Highlights" in the name)
normal = sec_counts[~sec_counts.index.str.contains("Highlights")]
print("Normal section titles:")
print(normal.sort_values(ascending=False))

# Group 2: "Highlights" titles contain dates, so remove the dates to see the patterns
hl = sections_df[sections_df["section"].str.contains("Highlights")].copy()
date_range = r"\s+[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}\s+to\s+[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}"
hl["pattern"] = hl["section"].str.replace(date_range, "", regex=True)
print("\nHighlights patterns (files per pattern):")
print(hl.groupby("pattern")["file_name"].nunique())

# See what rows sit under ONE Highlights title (label, value, extra)
one_title = hl["section"].iloc[0]
print("\nExample rows under:", one_title)
print(raw_fields_long.loc[raw_fields_long["section"] == one_title,
                          ["label", "value_raw", "extra_raw"]].to_string(index=False))

# Check the demographics header row: is "Category" being read as a field?
cat = raw_fields_long[raw_fields_long["label"] == "Category"]
print("\nRows with the label 'Category':", len(cat))
print(cat[["source_type", "value_raw", "extra_raw"]].drop_duplicates().to_string(index=False))


# In[671]:


# Mark the rows that belong to "Highlights" blocks (Top job title / location / industry)
is_highlights = raw_fields_long["section"].fillna("").str.contains("Highlights")

# Mark the rows that belong to the SinglePost demographics block
is_demo = raw_fields_long["section"].eq("Post viewer demographics")

# Everything else is a core metric or post header row (URL, date, time)
metrics_long = raw_fields_long[~is_highlights & ~is_demo].copy()

# Make section names comparable: lower-case, and a placeholder for rows above any section
metrics_long["section_norm"] = metrics_long["section"].fillna("(header)").str.casefold()

# Check 1: the three groups must add up to the full table (2617 rows)
print("Metrics:", len(metrics_long), "| Highlights:", is_highlights.sum(),
      "| Demographics:", is_demo.sum(),
      "| Total:", len(metrics_long) + is_highlights.sum() + is_demo.sum())

# Check 2: how many different metric labels are there really?
print("Distinct metric labels:", metrics_long["label"].nunique())

# Check 3: each label, by source type and section, with the number of files that have it
census = (metrics_long.groupby(["source_type", "section_norm", "label"])["file_name"]
          .nunique().rename("n_files").reset_index()
          .sort_values(["source_type", "section_norm", "n_files"],
                       ascending=[True, True, False]))
print(census.to_string(index=False))


# In[672]:


# Use only PostAnalytics metric rows (118 files)
pa_metrics = metrics_long[metrics_long["source_type"] == "PostAnalytics"]

# One row per file, one column per label: True if that label exists in the file
presence = pd.crosstab(pa_metrics["file_name"], pa_metrics["label"]).gt(0)

# Add the export date (workbook created date) of each file
presence = presence.join(meta.set_index("file_name")["created_date"])

# Labels we want to check
labels_to_check = ["Unique views", "Members reached", "Saves", "Sends on LinkedIn",
                   "Profile viewers from this post", "Followers gained from this post",
                   "Comments", "Comment", "Reposts", "Repost",
                   "Impressions", "Total Impressions"]

# Count the files per export date that have each label
summary = presence.groupby("created_date")[labels_to_check].sum()
summary.insert(0, "files", presence.groupby("created_date").size())

# Print with labels as rows and export dates as columns
print(summary.T)

# Do any files have BOTH "Unique views" and "Members reached"?
both = (presence["Unique views"] & presence["Members reached"]).sum()
print("\nFiles with both Unique views and Members reached:", both)


# In[673]:


# CHECK 1: publish dates of the 14 files without "Members reached" in the 2026-01-18 export
s2026 = presence[presence["created_date"] == pd.Timestamp("2026-01-18")].copy()

# Add each file's real publish time (decoded from the post_id earlier)
s2026 = s2026.join(all_ts.set_index("file_name")["id_utc"])

# Compare the two groups: has "Members reached" (True) vs not (False)
print(s2026.groupby("Members reached")["id_utc"].agg(["count", "min", "max"]))

# CHECK 2: values in the rows labelled "Comment" and "Repost" (singular)
singular = metrics_long[metrics_long["label"].isin(["Comment", "Repost"])]
print("\nValues in singular-label rows:")
print(singular.groupby("label")["value_raw"].value_counts())


# In[674]:


# Take the PostAnalytics rows for comments and reposts (singular and plural labels)
chk = metrics_long[
    (metrics_long["source_type"] == "PostAnalytics")
    & metrics_long["label"].isin(["Comments", "Comment", "Reposts", "Repost"])
].copy()

# Treat the singular and plural labels as the same metric for this check
chk["metric"] = chk["label"].replace({"Comment": "Comments", "Repost": "Reposts"})

# Convert values to numbers (remove commas first); text that is not a number becomes empty
chk["value_num"] = pd.to_numeric(chk["value_raw"].astype(str).str.replace(",", ""), errors="coerce")

# Add the export date of each file
chk = chk.merge(meta[["file_name", "created_date"]], on="file_name")

# For each metric and export date: number of rows, how many are 0, how many are not numbers
out = chk.groupby(["metric", "created_date"]).agg(
    rows=("value_num", "size"),
    zeros=("value_num", lambda s: (s == 0).sum()),
    non_numeric=("value_num", lambda s: s.isna().sum()),
)
print(out)


# In[675]:


# Explicit mapping: raw label (as in the Excel file) -> standard metric name
label_map = {
    # Post header fields
    "Post URL": "post_url",
    "Post Date": "post_date_raw",
    "Post Publish Time": "publish_time_raw",
    # Reach and impressions
    "Impressions": "impressions",
    "Total Impressions": "impressions",        # assumed to be the same metric (see note)
    "Unique views": "unique_views",            # kept separate from members_reached
    "Members reached": "members_reached",
    # Engagement
    "Reactions": "reactions",
    "Comments": "comments",
    "Comment": "comments",                     # singular spelling when the value is 1
    "Reposts": "reposts",
    "Repost": "reposts",                       # singular spelling when the value is 1
    "Saves": "saves",
    "Sends on LinkedIn": "sends_on_linkedin",
    "Social engagements": "social_engagements",
    "Link engagements": "link_engagements",
    "Premium custom button engagements": "premium_button_engagements",
    # Audience actions
    "Profile viewers from this post": "profile_viewers",
    "Followers gained from this post": "followers_gained",
    # Video: PostAnalytics labels
    "Views": "video_views_pa",
    "Minutes viewed": "minutes_viewed",
    "Lifetime unique viewers": "lifetime_unique_viewers",
    # Video: SinglePostAnalytics labels
    "Video views": "video_views",
    "Watch time": "watch_time_raw",
    "Average watch time": "avg_watch_time_raw",
    # Article
    "Article views": "article_views",
}

# Apply the mapping; keep the original label column for lineage
metrics_long["metric"] = metrics_long["label"].map(label_map)

# Check 1: any labels not in the dictionary? (expect 0)
print("Unmapped rows:", metrics_long["metric"].isna().sum())
print(metrics_long.loc[metrics_long["metric"].isna(), "label"].unique())

# Check 2: does any file end up with the same metric twice after mapping? (expect 0)
dups = metrics_long.groupby(["file_name", "metric"]).size()
print("Files with the same metric twice:", (dups > 1).sum())

# Check 3: how many files have each standard metric
print(metrics_long.groupby("metric")["file_name"].nunique().sort_values(ascending=False))


# In[676]:


# Keep only the metric rows that belong to the 107 current files
current_files = manifest.loc[manifest["is_current"],
                             ["file_name", "post_id", "source_type", "snapshot_ts"]]
cur = metrics_long.merge(current_files[["file_name", "post_id"]], on="file_name")

# Pivot: one row per post, one column per standard metric
wide = cur.pivot(index="post_id", columns="metric", values="value_raw")

# These columns stay as text; everything else should become numbers
text_metrics = ["post_url", "post_date_raw", "publish_time_raw",
                "watch_time_raw", "avg_watch_time_raw"]
text_cols = [c for c in text_metrics if c in wide.columns]
num_cols = [c for c in wide.columns if c not in text_metrics]

# Count the values present before converting (so we can spot silent failures)
before = wide[num_cols].notna().sum()

# Convert to numbers: remove thousand separators first, then convert
wide_num = wide[num_cols].apply(
    lambda s: pd.to_numeric(s.astype(str).str.replace(",", "", regex=False), errors="coerce")
)

# Check 1: columns where a value failed to convert (expect nothing printed)
after = wide_num.notna().sum()
lost = (before - after)[(before - after) != 0]
print("Columns with values that failed to convert:")
print(lost if len(lost) else "none")

# Join text columns, numeric columns and lineage columns into one table
posts_wide = (wide[text_cols]
              .join(wide_num)
              .join(current_files.set_index("post_id")[["file_name", "source_type", "snapshot_ts"]]))

# Check 2: size of the table (expect 107 rows)
print("\nShape:", posts_wide.shape)

# Check 3: missing values per column (empty = metric not in that source file)
print(posts_wide.isna().sum().sort_values(ascending=False))


# In[677]:


import numpy as np

# Posts that have both a PostAnalytics and a SinglePostAnalytics file (expect 28)
types_per_post = manifest.groupby("post_id")["source_type"].nunique()
overlap = types_per_post[types_per_post == 2].index
print("Overlap posts:", len(overlap))

# For each overlap post, take its newest PostAnalytics file
pa_latest = (manifest[manifest["post_id"].isin(overlap) & (manifest["source_type"] == "PostAnalytics")]
             .sort_values("snapshot_ts", ascending=False)
             .drop_duplicates("post_id")[["post_id", "file_name"]])
sp_cur = manifest[manifest["post_id"].isin(overlap) & (manifest["source_type"] == "SinglePostAnalytics")][["post_id", "file_name"]]

# Metric rows for each side
pa_rows = metrics_long.merge(pa_latest, on="file_name")[["post_id", "metric", "value_raw"]]
sp_rows = metrics_long.merge(sp_cur, on="file_name")[["post_id", "metric", "value_raw"]]

# Put both sides next to each other for each post and metric
both = pa_rows.merge(sp_rows, on=["post_id", "metric"], how="outer",
                     suffixes=("_pa", "_sp"), indicator=True)
both["_merge"] = both["_merge"].map({"left_only": "PA only", "right_only": "SP only", "both": "both"})

# Check 1: which metrics exist on only one side?
print("\nMetric presence (number of posts):")
print(both.groupby(["metric", "_merge"]).size().unstack(fill_value=0))

# Convert both sides to numbers (text fields like the URL become empty and drop out)
for side in ["pa", "sp"]:
    both["num_" + side] = pd.to_numeric(
        both["value_raw_" + side].astype(str).str.replace(",", "", regex=False), errors="coerce")

# Check 2: for shared numeric metrics, is SinglePost equal to, higher than, or lower than PostAnalytics?
shared = both[(both["_merge"] == "both")].dropna(subset=["num_pa", "num_sp"]).copy()
shared["compare"] = (shared["num_sp"] - shared["num_pa"]).apply(
    lambda d: "SP higher" if d > 0 else ("equal" if d == 0 else "SP lower"))
print("\nShared metrics: SinglePost vs PostAnalytics:")
print(shared.groupby(["metric", "compare"]).size().unstack(fill_value=0))


# In[678]:


# CHECK 1: publish dates of SinglePost posts with and without "Members reached"
sp_files = manifest.loc[manifest["source_type"] == "SinglePostAnalytics",
                        ["file_name", "post_id"]].copy()

# Mark SinglePost files that have a "Members reached" row
has_mr = metrics_long.loc[metrics_long["metric"] == "members_reached", "file_name"].unique()
sp_files["has_members_reached"] = sp_files["file_name"].isin(has_mr)

# Add each post's publish time (decoded from the post_id earlier)
sp_files = sp_files.merge(all_ts[["file_name", "id_utc"]], on="file_name")

# Compare the two groups: how many files, earliest and latest publish time
print(sp_files.groupby("has_members_reached")["id_utc"].agg(["count", "min", "max"]))

# CHECK 2: the posts where SinglePost saves are LOWER than PostAnalytics saves
saves_lower = shared[(shared["metric"] == "saves") & (shared["compare"] == "SP lower")]
print("\nPosts with lower saves in SinglePost:")
print(saves_lower[["post_id", "num_pa", "num_sp"]].to_string(index=False))


# In[679]:


# One row per file: export time and the post's real publish time
age = (manifest[["file_name", "source_type", "snapshot_ts"]]
       .merge(all_ts[["file_name", "id_utc"]], on="file_name"))

# How old was the post (in days) when the file was exported?
age["age_days"] = (age["snapshot_ts"] - age["id_utc"]).dt.days

# Keep only exports from 2025-10-08 onward (older export versions never had these fields)
age = age[age["snapshot_ts"] >= "2025-10-08"].copy()

# For each metric, mark whether the file has it
metrics_to_check = ["members_reached", "saves", "sends_on_linkedin", "premium_button_engagements"]
for m in metrics_to_check:
    files_with = metrics_long.loc[metrics_long["metric"] == m, "file_name"].unique()
    age["has_" + m] = age["file_name"].isin(files_with)

# Compare the post's age at export for files with and without each metric
print("Files tested:", len(age))
for m in metrics_to_check:
    print("\n", m)
    print(age.groupby("has_" + m)["age_days"].agg(["count", "min", "max"]))


# In[680]:


# Pivot ALL 158 files: one row per file, one column per standard metric
snap_wide = metrics_long.pivot(index="file_name", columns="metric", values="value_raw")

# Text columns stay as text; every other column should become a number
text_metrics = ["post_url", "post_date_raw", "publish_time_raw",
                "watch_time_raw", "avg_watch_time_raw"]
text_cols = [c for c in text_metrics if c in snap_wide.columns]
num_cols = [c for c in snap_wide.columns if c not in text_metrics]

# Convert to numbers (remove thousand separators first)
snap_num = snap_wide[num_cols].apply(
    lambda s: pd.to_numeric(s.astype(str).str.replace(",", "", regex=False), errors="coerce")
)

# Check 1: no value should be lost in the conversion (expect none)
lost = (snap_wide[num_cols].notna().sum() - snap_num.notna().sum())
print("Values lost in number conversion:", lost[lost != 0].to_dict() or "none")

# Join the text columns, number columns and the manifest columns (post_id, snapshot time, current flag)
snapshot_fact = (snap_wide[text_cols]
                 .join(snap_num)
                 .join(manifest.set_index("file_name")[
                     ["post_id", "source_type", "snapshot_ts", "snapshot_rank", "is_current"]]))

# Exact publish time in UTC, decoded from the post_id (keeping the seconds)
snapshot_fact["publish_ts_utc"] = snapshot_fact["post_id"].map(
    lambda x: pd.to_datetime(int(x) >> 22, unit="ms"))

# Same moment in IST (UTC + 5:30), useful for time-of-day analysis
snapshot_fact["publish_ts_ist"] = snapshot_fact["publish_ts_utc"] + pd.Timedelta(hours=5, minutes=30)

# Age of the post in days when the file was exported
snapshot_fact["post_age_days"] = (snapshot_fact["snapshot_ts"] - snapshot_fact["publish_ts_utc"]).dt.days

# Check 2: table size and number of posts and current rows (expect 158, 107, 107)
print("Rows:", len(snapshot_fact), "| Posts:", snapshot_fact["post_id"].nunique(),
      "| Current:", snapshot_fact["is_current"].sum())

# Check 3: no negative post ages (a post cannot be exported before it exists)
print("Negative post ages:", (snapshot_fact["post_age_days"] < 0).sum())

# Check 4: exported time minus its source offset should match the decoded UTC time (within 1 minute)
chk = snapshot_fact.merge(all_ts[["file_name", "export_ts"]], left_index=True, right_on="file_name")
offset = chk["source_type"].map({"PostAnalytics": pd.Timedelta(0),
                                 "SinglePostAnalytics": pd.Timedelta(hours=5, minutes=30)})
diff = (chk["export_ts"] - offset - chk["publish_ts_utc"]).abs()
print("Files where exported time and decoded UTC differ by more than 1 minute:", (diff > pd.Timedelta(minutes=1)).sum())


# In[681]:


from pathlib import Path

# Folder for cleaned data (created next to the notebook; the full path is printed below)
processed_folder = Path("processed")
processed_folder.mkdir(exist_ok=True)

# Turn the file_name index back into a normal column so it is saved
snapshot_out = snapshot_fact.reset_index()

# Table 1: every snapshot (158 rows, one per source file)
snapshot_out.to_csv(processed_folder / "snapshot_fact.csv", index=False)

# Table 2: only the current snapshot of each post (107 rows, one per post)
posts_current = snapshot_out[snapshot_out["is_current"]].copy()
posts_current.to_csv(processed_folder / "posts_current.csv", index=False)

# Show where the files were saved
print("Saved in:", processed_folder.resolve())

# Reload both files and check that nothing changed
chk_snap = pd.read_csv(processed_folder / "snapshot_fact.csv",
                       dtype={"post_id": str},
                       parse_dates=["snapshot_ts", "publish_ts_utc", "publish_ts_ist"])
chk_cur = pd.read_csv(processed_folder / "posts_current.csv", dtype={"post_id": str})

# Check 1: row counts (expect 158 and 107)
print("snapshot_fact rows:", len(chk_snap), "| posts_current rows:", len(chk_cur))

# Check 2: one current row per post (expect 107 unique post_ids)
print("Unique post_ids in posts_current:", chk_cur["post_id"].nunique())

# Check 3: missing values are still missing (blank), not turned into zeros
print("Missing members_reached before/after saving:",
      snapshot_out["members_reached"].isna().sum(), "/", chk_snap["members_reached"].isna().sum())

# Check 4: post_id kept all 19 digits (a number column could round them)
print("post_id values with 19 digits:", (chk_snap["post_id"].str.len() == 19).sum(), "of", len(chk_snap))


# In[682]:


import warnings
# Hide the repeated openpyxl style warning (it is harmless)
warnings.filterwarnings("ignore", message="Workbook contains no default style")

# For every file in the manifest, list the sheet names it contains
rows = []
for _, r in manifest.iterrows():
    xl = pd.ExcelFile(raw_folder / r["file_name"])
    rows.append({"file_name": r["file_name"],
                 "source_type": r["source_type"],
                 "sheets": tuple(xl.sheet_names)})
sheet_census = pd.DataFrame(rows)

# Add each file's export date so we can see whether sheets depend on the export session
sheet_census = sheet_census.merge(meta[["file_name", "created_date"]], on="file_name")

# Count files for each combination of source type, export date and sheet names
print(sheet_census.groupby(["source_type", "created_date", "sheets"]).size())


# In[683]:


# Files that have a TOP DEMOGRAPHICS sheet (expect 80)
demo_files = sheet_census.loc[
    sheet_census["sheets"].apply(lambda s: "TOP DEMOGRAPHICS" in s), "file_name"
]

shapes = []      # (rows, columns) of the sheet in each file
first_rows = []  # what the first row of each sheet contains

for f in demo_files:
    # header=None so the first row is kept as data and we can see it
    d = pd.read_excel(raw_folder / f, sheet_name="TOP DEMOGRAPHICS", header=None)
    shapes.append(d.shape)
    first_rows.append(tuple(d.iloc[0].astype(str)))

print("Files:", len(demo_files))

# How big are the sheets? (most common sizes first)
print("\nSheet shapes (rows, columns):")
print(pd.Series(shapes).value_counts().head(10))

# What does the first row look like? (most common first rows)
print("\nFirst rows:")
print(pd.Series(first_rows).value_counts().head(5))

# Print the first 25 rows of one example file
example = demo_files.iloc[0]
print("\nExample file:", example)
print(pd.read_excel(raw_folder / example, sheet_name="TOP DEMOGRAPHICS", header=None)
      .head(25).to_string())


# In[684]:



# STEP 1: Check demographic coverage in the selected current snapshots

# Create a file-level flag indicating whether each workbook has
# a TOP DEMOGRAPHICS worksheet.
demo_coverage = manifest[
    [
        "file_name",
        "post_id",
        "source_type",
        "snapshot_ts",
        "is_current"
    ]
].merge(
    sheet_census[["file_name", "sheets"]],
    on="file_name",
    how="left",
    validate="one_to_one"
)

demo_coverage["has_demographics"] = demo_coverage["sheets"].apply(
    lambda sheets: (
        "TOP DEMOGRAPHICS" in sheets
        if isinstance(sheets, (tuple, list))
        else False
    )
)

# Keep only the selected current snapshot for each post.
current_demo_coverage = demo_coverage[
    demo_coverage["is_current"]
].copy()

# Check 1: overall coverage
print("Current posts:", len(current_demo_coverage))
print(
    "Unique current post IDs:",
    current_demo_coverage["post_id"].nunique()
)

print("\nDemographic coverage:")
print(
    current_demo_coverage["has_demographics"]
    .value_counts()
    .rename(index={True: "Has demographics", False: "No demographics"})
)

# Check 2: coverage by export type
print("\nCoverage by source type:")
print(
    current_demo_coverage.groupby("source_type")["has_demographics"]
    .agg(["count", "sum"])
    .rename(columns={
        "count": "current_files",
        "sum": "files_with_demographics"
    })
)

# Check 3: identify current posts without demographic sheets
missing_demo = current_demo_coverage[
    ~current_demo_coverage["has_demographics"]
][
    ["post_id", "source_type", "snapshot_ts", "file_name"]
]

print("\nCurrent posts without demographic sheets:", len(missing_demo))
print(missing_demo.to_string(index=False))


# In[685]:



# STEP 2: Check whether missing current demographics exist in older exports

# Find all posts that have a TOP DEMOGRAPHICS sheet in any source file.
all_demo_posts = set(
    demo_coverage.loc[
        demo_coverage["has_demographics"],
        "post_id"
    ].dropna().astype(str)
)

# Find posts with demographics in their selected current snapshot.
current_demo_posts = set(
    current_demo_coverage.loc[
        current_demo_coverage["has_demographics"],
        "post_id"
    ].dropna().astype(str)
)

# Find posts without current demographics but with historical demographics.
missing_current_demo_ids = set(
    current_demo_coverage.loc[
        ~current_demo_coverage["has_demographics"],
        "post_id"
    ].dropna().astype(str)
)

historical_demo_available_ids = (
    missing_current_demo_ids & all_demo_posts
)

print("Posts without demographics in current snapshot:",
      len(missing_current_demo_ids))

print("Posts with demographics in at least one export:",
      len(all_demo_posts))

print("Posts with historical demographics but none in current snapshot:",
      len(historical_demo_available_ids))

print("Posts with no demographic sheet in any available export:",
      len(missing_current_demo_ids - all_demo_posts))

# Display examples for investigation.
historical_demo_candidates = demo_coverage[
    demo_coverage["post_id"].astype(str).isin(
        historical_demo_available_ids
    )
    & demo_coverage["has_demographics"]
][
    ["post_id", "source_type", "snapshot_ts", "file_name"]
].sort_values(["post_id", "snapshot_ts"])

print("\nHistorical demographic snapshots for these posts:")
print(historical_demo_candidates.head(15).to_string(index=False))


# In[686]:



# Step 3: Find existing demographic DataFrames

import pandas as pd

demo_df_candidates = {
    name: obj
    for name, obj in globals().items()
    if isinstance(obj, pd.DataFrame)
    and ("demo" in name.lower() or "demographic" in name.lower())
}

for name, df in demo_df_candidates.items():
    print(f"\nDataFrame: {name}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")


# In[687]:



# Step 3: Inspect demographic records and their join keys

print("DEMOGRAPHIC DATA")
print("Shape:", demographics_df.shape)
print("Data types:")
print(demographics_df.dtypes)

print("\nSample demographic records:")
display(demographics_df.head(10))

print("\nSample file-level coverage records:")
display(
    demo_coverage[
        [
            "file_name",
            "post_id",
            "source_type",
            "snapshot_ts",
            "has_demographics"
        ]
    ].head(10)
)

print("\nJoin-key summary")
print(
    "Unique demographic post URLs:",
    demographics_df["post_url"].nunique(dropna=True)
)
print(
    "Missing demographic post URLs:",
    demographics_df["post_url"].isna().sum()
)
print(
    "Unique source files in coverage:",
    demo_coverage["file_name"].nunique()
)


# In[688]:



# Step 4: Inspect existing file inventory and path variables

keywords = (
    "path", "folder", "directory", "root",
    "manifest", "file_list", "file_paths",
    "workbook", "excel", "input_dir", "output_dir"
)

for name, obj in list(globals().items()):
    if any(keyword in name.lower() for keyword in keywords):
        if isinstance(obj, (str, list, tuple, pd.DataFrame)):
            if isinstance(obj, pd.DataFrame):
                print(
                    f"{name}: DataFrame, shape={obj.shape}, "
                    f"columns={obj.columns.tolist()}"
                )
            elif isinstance(obj, (list, tuple)):
                print(f"{name}: {type(obj).__name__}, length={len(obj)}")
            else:
                print(f"{name}: {obj}")


# In[689]:



# Step 5: Validate demographic source-file coverage in the manifest

print("Manifest rows:", len(manifest))
print("Unique manifest filenames:", manifest["file_name"].nunique())

print("\nDemographic coverage rows:", len(demo_coverage))
print("Unique coverage filenames:", demo_coverage["file_name"].nunique())

# Compare filenames between the two tables
manifest_names = set(manifest["file_name"].dropna().astype(str))
coverage_names = set(demo_coverage["file_name"].dropna().astype(str))

print("\nFiles in manifest but not in demo_coverage:",
      len(manifest_names - coverage_names))

print("Files in demo_coverage but not in manifest:",
      len(coverage_names - manifest_names))

# Count manifest files with demographic sheets
manifest_demo_check = manifest.merge(
    demo_coverage[["file_name", "has_demographics"]],
    on="file_name",
    how="left",
    validate="one_to_one"
)

print("\nManifest files with demographic sheets:",
      manifest_demo_check["has_demographics"].eq(True).sum())

print("Manifest files without demographic sheets:",
      manifest_demo_check["has_demographics"].eq(False).sum())

print("Files with unknown demographic status:",
      manifest_demo_check["has_demographics"].isna().sum())


# In[690]:



# Step 6: Inspect available Excel file paths and workbook-related objects

print("raw_excel_files type:", type(raw_excel_files).__name__)
print("raw_excel_files count:", len(raw_excel_files))

print("\nFirst 3 raw Excel file paths:")
for file_path in raw_excel_files[:3]:
    print(file_path)

print("\nManifest columns:")
print(manifest.columns.tolist())

print("\nDemographic files from coverage:")
print(
    demo_coverage.loc[
        demo_coverage["has_demographics"].eq(True),
        ["file_name", "post_id", "source_type", "snapshot_ts", "is_current"]
    ].head(5).to_string(index=False)
)


# In[691]:



# Step 7: Match demographic workbooks to their actual file paths

from pathlib import Path

# Build a filename-to-path lookup from the available Excel files
path_lookup = {}

for file_path in raw_excel_files:
    file_name = Path(file_path).name
    path_lookup.setdefault(file_name, file_path)

# Keep only manifest files identified as having demographic sheets
demographic_files = demo_coverage.loc[
    demo_coverage["has_demographics"].eq(True),
    ["file_name", "post_id", "source_type", "snapshot_ts", "is_current"]
].copy()

demographic_files["file_path"] = demographic_files["file_name"].map(path_lookup)

print("Demographic workbook records:", len(demographic_files))
print("Matched to actual paths:", demographic_files["file_path"].notna().sum())
print("Missing actual paths:", demographic_files["file_path"].isna().sum())

if demographic_files["file_path"].isna().any():
    print("\nFiles without matching paths:")
    print(
        demographic_files.loc[
            demographic_files["file_path"].isna(), "file_name"
        ].to_list()
    )

print("\nSample matched records:")
print(demographic_files.head(5).to_string(index=False))


# In[692]:



# Step 8: Inspect worksheet names in the first 5 demographic workbooks

import pandas as pd

for _, row in demographic_files.head(5).iterrows():
    print(f"\nFile: {row['file_name']}")

    try:
        with pd.ExcelFile(row["file_path"]) as workbook:
            print("Worksheets:", workbook.sheet_names)

    except Exception as e:
        print("Error reading workbook:", repr(e))


# In[693]:



# Step 9: Inspect the raw TOP DEMOGRAPHICS worksheet

sample_file = demographic_files.iloc[0]["file_path"]

with pd.ExcelFile(sample_file) as workbook:
    raw_demo_sample = pd.read_excel(
        workbook,
        sheet_name="TOP DEMOGRAPHICS",
        header=None
    )

print("Sample file:", Path(sample_file).name)
print("Raw worksheet shape:", raw_demo_sample.shape)

print("\nFirst 12 rows:")
print(raw_demo_sample.head(12).to_string(index=False, header=False))

print("\nRaw cell values and types:")
for col in raw_demo_sample.columns:
    values = raw_demo_sample[col].dropna().head(6).tolist()
    print(f"Column {col}: {values}")


# In[694]:



# Step 10: Extract demographic rows from one workbook with lineage

sample_metadata = demographic_files.iloc[0]

with pd.ExcelFile(sample_metadata["file_path"]) as workbook:
    sample_demo_extracted = pd.read_excel(
        workbook,
        sheet_name="TOP DEMOGRAPHICS"
    )

# Standardize column names for the extraction test
sample_demo_extracted.columns = [
    str(col).strip().lower() for col in sample_demo_extracted.columns
]

# Attach source and snapshot metadata
sample_demo_extracted["file_name"] = sample_metadata["file_name"]
sample_demo_extracted["post_id"] = sample_metadata["post_id"]
sample_demo_extracted["source_type"] = sample_metadata["source_type"]
sample_demo_extracted["snapshot_ts"] = sample_metadata["snapshot_ts"]
sample_demo_extracted["is_current"] = sample_metadata["is_current"]

print("Extracted shape:", sample_demo_extracted.shape)
print("\nColumns:")
print(sample_demo_extracted.columns.tolist())

print("\nExtracted sample:")
print(sample_demo_extracted.head(10).to_string(index=False))

print("\nMissing values:")
print(sample_demo_extracted.isna().sum().to_string())


# In[695]:



# Step 11: Extract demographic snapshots from all validated workbooks

demographic_snapshot_parts = []
demographic_extraction_errors = []
demographic_schema_issues = []

for _, metadata in demographic_files.iterrows():
    file_path = metadata["file_path"]
    file_name = metadata["file_name"]

    try:
        with pd.ExcelFile(file_path) as workbook:

            if "TOP DEMOGRAPHICS" not in workbook.sheet_names:
                demographic_schema_issues.append({
                    "file_name": file_name,
                    "issue": "TOP DEMOGRAPHICS sheet missing"
                })
                continue

            demo_part = pd.read_excel(
                workbook,
                sheet_name="TOP DEMOGRAPHICS"
            )

        # Normalize column labels for consistent processing
        demo_part.columns = [
            str(col).strip().lower() for col in demo_part.columns
        ]

        required_columns = {"category", "value", "%"}

        if not required_columns.issubset(demo_part.columns):
            demographic_schema_issues.append({
                "file_name": file_name,
                "issue": f"Unexpected columns: {demo_part.columns.tolist()}"
            })
            continue

        # Attach source and snapshot lineage
        demo_part["file_name"] = file_name
        demo_part["post_id"] = metadata["post_id"]
        demo_part["source_type"] = metadata["source_type"]
        demo_part["snapshot_ts"] = metadata["snapshot_ts"]
        demo_part["is_current"] = metadata["is_current"]

        demographic_snapshot_parts.append(demo_part)

    except Exception as e:
        demographic_extraction_errors.append({
            "file_name": file_name,
            "error": repr(e)
        })

# Combine successfully extracted snapshots
if demographic_snapshot_parts:
    demographics_snapshot_fact = pd.concat(
        demographic_snapshot_parts,
        ignore_index=True
    )
else:
    demographics_snapshot_fact = pd.DataFrame()

print("Workbooks targeted:", len(demographic_files))
print("Workbooks extracted successfully:", len(demographic_snapshot_parts))
print("Extraction errors:", len(demographic_extraction_errors))
print("Schema issues:", len(demographic_schema_issues))
print("Combined fact-table shape:", demographics_snapshot_fact.shape)

print("\nCombined columns:")
print(demographics_snapshot_fact.columns.tolist())

print("\nExtraction errors:")
print(demographic_extraction_errors)

print("\nSchema issues:")
print(demographic_schema_issues)


# In[696]:



# Step 12: Standardize demographic fact-table column names

demographics_snapshot_fact = demographics_snapshot_fact.rename(
    columns={"%": "percentage"}
)

expected_columns = [
    "category",
    "value",
    "percentage",
    "file_name",
    "post_id",
    "source_type",
    "snapshot_ts",
    "is_current"
]

print("Actual columns:")
print(demographics_snapshot_fact.columns.tolist())

print("\nExpected columns:")
print(expected_columns)

print("\nColumn schema matches:", 
      demographics_snapshot_fact.columns.tolist() == expected_columns)

print("\nData types:")
print(demographics_snapshot_fact.dtypes.to_string())

print("\nFirst 5 rows:")
print(demographics_snapshot_fact.head().to_string(index=False))


# In[697]:



# Step 13: Profile percentage values before standardization

print("Percentage dtype:", demographics_snapshot_fact["percentage"].dtype)

print("\nPython value types:")
print(
    demographics_snapshot_fact["percentage"]
    .map(lambda x: type(x).__name__)
    .value_counts(dropna=False)
    .to_string()
)

print("\nMissing percentages:",
      demographics_snapshot_fact["percentage"].isna().sum())

print("\nUnique percentage values (first 20):")
print(
    demographics_snapshot_fact["percentage"]
    .dropna()
    .astype(str)
    .drop_duplicates()
    .head(20)
    .to_list()
)

print("\nText-formatted percentage values:")
text_percentage_mask = (
    demographics_snapshot_fact["percentage"].notna()
    & ~demographics_snapshot_fact["percentage"].map(
        lambda x: isinstance(x, (int, float))
    )
)

print("Count:", text_percentage_mask.sum())

print(
    demographics_snapshot_fact.loc[
        text_percentage_mask,
        ["category", "value", "percentage", "file_name"]
    ].head(15).to_string(index=False)
)


# In[698]:



# Step 14: Inspect all text-formatted percentage values

text_percentage_mask = demographics_snapshot_fact["percentage"].map(
    lambda x: isinstance(x, str)
)

text_percentage_values = (
    demographics_snapshot_fact.loc[
        text_percentage_mask, "percentage"
    ]
    .value_counts(dropna=False)
)

print("Text percentage patterns and counts:")
print(text_percentage_values.to_string())

print("\nTotal text percentage rows:", text_percentage_mask.sum())

print(
    "\nRows with text percentages by category:"
)
print(
    demographics_snapshot_fact.loc[
        text_percentage_mask
    ]
    .groupby(["category", "percentage"], dropna=False)
    .size()
    .rename("row_count")
    .reset_index()
    .to_string(index=False)
)

print("\nAre all text percentages '< 1%'?",
      demographics_snapshot_fact.loc[
          text_percentage_mask, "percentage"
      ].eq("< 1%").all())


# In[699]:



# Step 15: Preserve numeric proportions and text percentage labels

demographics_snapshot_fact["percentage_original"] = (
    demographics_snapshot_fact["percentage"].copy()
)

# Standardized column:
# - Numeric proportions remain numeric
# - Text labels such as "< 1%" remain unchanged
demographics_snapshot_fact["percentage"] = (
    demographics_snapshot_fact["percentage"].map(
        lambda x: x if isinstance(x, str) else float(x)
    )
)

print("Original percentage dtype:",
      demographics_snapshot_fact["percentage_original"].dtype)

print("\nStandardized value types:")
print(
    demographics_snapshot_fact["percentage"]
    .map(lambda x: type(x).__name__)
    .value_counts()
    .to_string()
)

print("\nText labels preserved:",
      demographics_snapshot_fact.loc[
          demographics_snapshot_fact["percentage_original"].map(
              lambda x: isinstance(x, str)
          ),
          "percentage"
      ].eq("< 1%").all())

print("\nNumeric values preserved:",
      (
          demographics_snapshot_fact.loc[
              demographics_snapshot_fact["percentage_original"].map(
                  lambda x: isinstance(x, (int, float))
              ),
              "percentage"
          ].astype(float).to_numpy()
          ==
          demographics_snapshot_fact.loc[
              demographics_snapshot_fact["percentage_original"].map(
                  lambda x: isinstance(x, (int, float))
              ),
              "percentage_original"
          ].astype(float).to_numpy()
      ).all())

print("\nShape after standardization:",
      demographics_snapshot_fact.shape)


# In[700]:



# Step 16: Validate demographic snapshot lineage against the manifest

lineage_columns = [
    "file_name",
    "post_id",
    "source_type",
    "snapshot_ts",
    "is_current"
]

# Prepare the expected metadata from the manifest
manifest_lineage = manifest[lineage_columns].copy()

# Compare each demographic row against its source workbook metadata
lineage_check = demographics_snapshot_fact.merge(
    manifest_lineage,
    on="file_name",
    how="left",
    suffixes=("_fact", "_manifest"),
    indicator=True,
    validate="many_to_one"
)

print("Demographic rows checked:", len(lineage_check))

print("\nWorkbook match status:")
print(lineage_check["_merge"].value_counts(dropna=False).to_string())

for column in ["post_id", "source_type", "snapshot_ts", "is_current"]:
    fact_values = lineage_check[f"{column}_fact"]
    manifest_values = lineage_check[f"{column}_manifest"]

    matches = fact_values.eq(manifest_values) | (
        fact_values.isna() & manifest_values.isna()
    )

    print(f"{column} matches: {matches.sum()} / {len(lineage_check)}")

print("\nRows with any lineage mismatch:")

mismatch_mask = lineage_check["_merge"].ne("both")

for column in ["post_id", "source_type", "snapshot_ts", "is_current"]:
    mismatch_mask |= ~(
        lineage_check[f"{column}_fact"].eq(
            lineage_check[f"{column}_manifest"]
        )
        | (
            lineage_check[f"{column}_fact"].isna()
            & lineage_check[f"{column}_manifest"].isna()
        )
    )

print(mismatch_mask.sum())

if mismatch_mask.any():
    print(
        lineage_check.loc[
            mismatch_mask,
            [
                "file_name",
                "post_id_fact", "post_id_manifest",
                "source_type_fact", "source_type_manifest",
                "snapshot_ts_fact", "snapshot_ts_manifest",
                "is_current_fact", "is_current_manifest"
            ]
        ].head(10).to_string(index=False)
    )


# In[701]:



# Step 17: Check exact duplicate demographic records

duplicate_key = [
    "file_name",
    "post_id",
    "source_type",
    "snapshot_ts",
    "category",
    "value",
    "percentage"
]

duplicate_mask = demographics_snapshot_fact.duplicated(
    subset=duplicate_key,
    keep=False
)

print("Total demographic rows:", len(demographics_snapshot_fact))
print("Rows involved in exact duplicates:", duplicate_mask.sum())
print(
    "Distinct duplicate groups:",
    demographics_snapshot_fact.loc[
        duplicate_mask, duplicate_key
    ].drop_duplicates().shape[0]
)

if duplicate_mask.any():
    print("\nSample duplicate records:")
    print(
        demographics_snapshot_fact.loc[
            duplicate_mask
        ].sort_values(
            ["file_name", "category", "value"]
        ).head(20).to_string(index=False)
    )
else:
    print("\nNo exact duplicate demographic records found.")


# In[702]:



# Step 18: Reconcile extracted demographics with coverage metadata

print("=== Workbook-level reconciliation ===")
print("Workbooks extracted:",
      demographics_snapshot_fact["file_name"].nunique())

print("Workbooks marked as having demographics:",
      demographic_files["file_name"].nunique())

print("\n=== Post-level coverage ===")
print("Unique posts with demographic records:",
      demographics_snapshot_fact["post_id"].nunique())

print("Unique posts with demographics in any export:",
      demo_coverage.loc[
          demo_coverage["has_demographics"].eq(True), "post_id"
      ].nunique())

print("\n=== Current versus historical records ===")
print("Rows from current snapshots:",
      demographics_snapshot_fact["is_current"].sum())

print("Rows from historical snapshots:",
      (~demographics_snapshot_fact["is_current"]).sum())

print("Unique posts represented in current demographic snapshots:",
      demographics_snapshot_fact.loc[
          demographics_snapshot_fact["is_current"], "post_id"
      ].nunique())

print("Unique posts represented in historical demographic snapshots:",
      demographics_snapshot_fact.loc[
          ~demographics_snapshot_fact["is_current"], "post_id"
      ].nunique())


# In[703]:



# Step 19: Compare current and historical demographic post coverage

current_demo_posts = set(
    demographics_snapshot_fact.loc[
        demographics_snapshot_fact["is_current"], "post_id"
    ].dropna()
)

historical_demo_posts = set(
    demographics_snapshot_fact.loc[
        ~demographics_snapshot_fact["is_current"], "post_id"
    ].dropna()
)

both_current_and_historical = current_demo_posts & historical_demo_posts
current_only = current_demo_posts - historical_demo_posts
historical_only = historical_demo_posts - current_demo_posts

print("Posts with current demographic snapshots:",
      len(current_demo_posts))

print("Posts with historical demographic snapshots:",
      len(historical_demo_posts))

print("Posts represented in both:",
      len(both_current_and_historical))

print("Posts represented only in current snapshots:",
      len(current_only))

print("Posts represented only in historical snapshots:",
      len(historical_only))

print("\nUnion of current and historical posts:",
      len(current_demo_posts | historical_demo_posts))


# In[704]:



# Step 20: Validate row counts and workbook-level extraction completeness

# Count extracted demographic rows per workbook
extracted_row_counts = (
    demographics_snapshot_fact
    .groupby("file_name")
    .size()
    .rename("extracted_rows")
    .reset_index()
)

# Compare against the original coverage records
workbook_row_check = demographic_files[
    ["file_name", "post_id", "snapshot_ts", "is_current"]
].merge(
    extracted_row_counts,
    on="file_name",
    how="left",
    validate="one_to_one"
)

workbook_row_check["extracted_rows"] = (
    workbook_row_check["extracted_rows"].fillna(0).astype(int)
)

print("Demographic workbooks expected:", len(demographic_files))
print("Workbooks represented in fact table:",
      demographics_snapshot_fact["file_name"].nunique())
print("Workbooks with zero extracted rows:",
      (workbook_row_check["extracted_rows"] == 0).sum())

print("\nRows per workbook — summary:")
print(workbook_row_check["extracted_rows"].describe().to_string())

print("\nTotal rows in workbook-level reconciliation:",
      workbook_row_check["extracted_rows"].sum())

print("Total rows in demographic fact table:",
      len(demographics_snapshot_fact))

print("\nWorkbooks with the fewest extracted rows:")
print(
    workbook_row_check.sort_values("extracted_rows")
    [["file_name", "extracted_rows"]]
    .head(10)
    .to_string(index=False)
)


# In[705]:



# Step 21: Validate required fields and approved percentage representations

required_fields = [
    "category",
    "value",
    "percentage",
    "file_name",
    "post_id",
    "source_type",
    "snapshot_ts",
    "is_current"
]

print("=== Required-field completeness ===")
print(
    demographics_snapshot_fact[required_fields]
    .isna()
    .sum()
    .to_string()
)

print("\n=== Blank text fields ===")
for column in ["category", "value", "file_name", "post_id", "source_type"]:
    blank_count = (
        demographics_snapshot_fact[column]
        .astype("string")
        .str.strip()
        .eq("")
        .sum()
    )
    print(f"{column}: {blank_count}")

print("\n=== Percentage validity ===")
percentage_values = demographics_snapshot_fact["percentage"]

valid_percentage_mask = percentage_values.map(
    lambda x: (
        isinstance(x, (int, float))
        and not isinstance(x, bool)
        and pd.notna(x)
        and 0 <= x <= 1
    ) or (
        isinstance(x, str)
        and x == "< 1%"
    )
)

print("Valid percentage values:", valid_percentage_mask.sum())
print("Invalid percentage values:", (~valid_percentage_mask).sum())

if (~valid_percentage_mask).any():
    print("\nUnexpected percentage values:")
    print(
        demographics_snapshot_fact.loc[
            ~valid_percentage_mask,
            ["category", "value", "percentage", "file_name"]
        ].to_string(index=False)
    )

print("\n=== Workbook metadata uniqueness ===")
print("Unique filenames in fact table:",
      demographics_snapshot_fact["file_name"].nunique())
print("Unique filenames in manifest:", manifest["file_name"].nunique())
print("Unique manifest records per filename:",
      manifest["file_name"].is_unique)


# In[706]:


# Step 22: Inspect the demographic fact-table structure

print("=== Demographic fact-table shape ===")
print(demographics_snapshot_fact.shape)

print("\n=== Current columns ===")
print(demographics_snapshot_fact.columns.tolist())

print("\n=== Data types ===")
print(demographics_snapshot_fact.dtypes.to_string())

print("\n=== First 5 records ===")
display(demographics_snapshot_fact.head())

print("\n=== Last 5 records ===")
display(demographics_snapshot_fact.tail())


# In[707]:


# Step 23: Confirm the audit column is safe to remove

audit_match = demographics_snapshot_fact["percentage"].eq(
    demographics_snapshot_fact["percentage_original"]
)

print("=== Percentage audit ===")
print("Rows checked:", len(audit_match))
print("Matching original values:", audit_match.sum())
print("Mismatched values:", (~audit_match).sum())

if audit_match.all():
    demographics_snapshot_fact = demographics_snapshot_fact.drop(
        columns=["percentage_original"]
    )
    print("\nTemporary audit column removed.")
else:
    print("\nAudit mismatches found. Column has been retained for investigation.")

print("\n=== Final schema ===")
print("Shape:", demographics_snapshot_fact.shape)
print("Columns:", demographics_snapshot_fact.columns.tolist())


# In[708]:


# Step 24: Final demographic fact-table validation

expected_columns = [
    "category",
    "value",
    "percentage",
    "file_name",
    "post_id",
    "source_type",
    "snapshot_ts",
    "is_current"
]

print("=== Final structure ===")
print("Shape:", demographics_snapshot_fact.shape)
print("Column order correct:",
      demographics_snapshot_fact.columns.tolist() == expected_columns)
print("Temporary audit column removed:",
      "percentage_original" not in demographics_snapshot_fact.columns)

print("\n=== Record counts ===")
print("Total demographic records:",
      len(demographics_snapshot_fact))
print("Unique demographic workbooks:",
      demographics_snapshot_fact["file_name"].nunique())
print("Unique posts:",
      demographics_snapshot_fact["post_id"].nunique())
print("Current snapshot records:",
      demographics_snapshot_fact["is_current"].sum())
print("Historical snapshot records:",
      (~demographics_snapshot_fact["is_current"]).sum())

print("\n=== Data integrity ===")
print("Exact duplicate rows:",
      demographics_snapshot_fact.duplicated().sum())
print("Missing values:",
      demographics_snapshot_fact.isna().sum().sum())
print("Snapshot timestamps are datetime:",
      pd.api.types.is_datetime64_any_dtype(
          demographics_snapshot_fact["snapshot_ts"]
      ))
print("Current flag is Boolean:",
      demographics_snapshot_fact["is_current"].dtype == bool)

print("\n=== Percentage representations ===")
print(
    demographics_snapshot_fact["percentage"]
    .map(type)
    .value_counts()
    .to_string()
)


# In[709]:


# Step 25: Inspect the existing project output paths

print("Current working directory:")
print(os.getcwd())

print("\nRelevant path variables:")
for name in [
    "output_dir",
    "output_folder",
    "export_dir",
    "project_dir",
    "base_dir"
]:
    if name in globals():
        print(f"{name}: {globals()[name]}")


# In[710]:


# Step 26: Inspect folders in the current working directory

import os

print("Folders inside:", os.getcwd())

for item in os.listdir(os.getcwd()):
    full_path = os.path.join(os.getcwd(), item)

    if os.path.isdir(full_path):
        print("[FOLDER]", item)


# In[711]:


# Step 27: Inspect likely project locations

folders_to_check = [
    r"C:\Users\Shifa\extracted_data",
    r"C:\Users\Shifa\processed",
    r"C:\Users\Shifa\Documents",
    r"C:\Users\Shifa\Desktop"
]

for folder in folders_to_check:
    print(f"\n=== {folder} ===")

    if os.path.isdir(folder):
        for item in os.listdir(folder)[:30]:
            full_path = os.path.join(folder, item)

            if os.path.isdir(full_path):
                print("[FOLDER]", item)
            else:
                print("[FILE]", item)
    else:
        print("Folder not found.")


# In[712]:


# Step 28: Save the demographic fact table

output_path = os.path.join(
    r"C:\Users\Shifa\processed",
    "demographics_snapshot_fact.csv"
)

demographics_snapshot_fact.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("Export completed.")
print("File path:", output_path)
print("Rows exported:", len(demographics_snapshot_fact))
print("Columns exported:", len(demographics_snapshot_fact.columns))
print("File exists:", os.path.isfile(output_path))
print("File size (bytes):", os.path.getsize(output_path))


# In[713]:


# Step 29: Reload and validate the exported CSV

reloaded_demographics = pd.read_csv(
    output_path,
    parse_dates=["snapshot_ts"],
    dtype={"post_id": "string"}
)

# Restore numeric proportions while preserving "< 1%" labels
reloaded_demographics["percentage"] = (
    reloaded_demographics["percentage"].map(
        lambda x: x if x == "< 1%" else float(x)
    )
)

print("=== Export round-trip validation ===")
print("File exists:", os.path.isfile(output_path))
print("Reloaded shape:", reloaded_demographics.shape)
print(
    "Column order correct:",
    reloaded_demographics.columns.tolist()
    == demographics_snapshot_fact.columns.tolist()
)

print("\n=== Data integrity ===")
print("Missing values:", reloaded_demographics.isna().sum().sum())
print("Exact duplicate rows:", reloaded_demographics.duplicated().sum())
print("Unique posts:", reloaded_demographics["post_id"].nunique())
print("Unique workbooks:", reloaded_demographics["file_name"].nunique())
print("Percentage value types:")
print(reloaded_demographics["percentage"].map(type).value_counts().to_string())

print("\n=== Comparison with original dataframe ===")
print(
    "Row counts match:",
    len(reloaded_demographics) == len(demographics_snapshot_fact)
)
print(
    "Post IDs match:",
    reloaded_demographics["post_id"].astype(str).equals(
        demographics_snapshot_fact["post_id"].astype(str)
    )
)
print(
    "Percentage values match:",
    reloaded_demographics["percentage"].equals(
        demographics_snapshot_fact["percentage"]
    )
)
print(
    "Snapshot timestamps match:",
    reloaded_demographics["snapshot_ts"].equals(
        demographics_snapshot_fact["snapshot_ts"]
    )
)
print(
    "Current flags match:",
    reloaded_demographics["is_current"].equals(
        demographics_snapshot_fact["is_current"]
    )
)


# In[714]:



# Step 30: Check the project's expected output files

import os

processed_dir = r"C:\Users\Shifa\processed"

expected_files = [
    "posts_current.csv",
    "snapshot_fact.csv",
    "demographics_snapshot_fact.csv",
    "file_manifest.csv"
]

print("=== Expected Project Deliverables ===")

for filename in expected_files:
    path = os.path.join(processed_dir, filename)

    if os.path.isfile(path):
        print(f"{filename} | Exists: True | Size: {os.path.getsize(path):,} bytes")
    else:
        print(f"{filename} | Exists: False")

print("\n=== All Files Currently in Processed Folder ===")

for filename in sorted(os.listdir(processed_dir)):
    print(filename)


# In[715]:



# Step 31: Validate the existing file manifest before export

print("=== Manifest Structure ===")
print("Shape:", manifest.shape)
print("Columns:", manifest.columns.tolist())

print("\n=== First 5 Rows ===")
display(manifest.head())

print("\n=== Data Types ===")
print(manifest.dtypes)

print("\n=== Data Quality ===")
print("Missing values by column:")
print(manifest.isna().sum())

print("\nExact duplicate rows:", manifest.duplicated().sum())

if "file_name" in manifest.columns:
    print("Unique filenames:", manifest["file_name"].nunique())
    print("Filename column has no missing values:",
          manifest["file_name"].notna().all())
    print("Filenames are unique:",
          manifest["file_name"].is_unique)


# In[716]:



# Step 32: Export the validated file manifest

manifest_output_path = os.path.join(
    r"C:\Users\Shifa\processed",
    "file_manifest.csv"
)

manifest.to_csv(
    manifest_output_path,
    index=False,
    encoding="utf-8-sig"
)

print("=== Manifest Export ===")
print("File exists:", os.path.isfile(manifest_output_path))
print("Output path:", manifest_output_path)
print("Rows exported:", len(manifest))
print("Columns exported:", len(manifest.columns))
print("File size:", f"{os.path.getsize(manifest_output_path):,} bytes")


# In[717]:



# Step 33: Reload and validate the exported manifest

reloaded_manifest = pd.read_csv(
    manifest_output_path,
    parse_dates=["snapshot_ts"],
    dtype={"post_id": "string"}
)

print("=== Manifest Round-Trip Validation ===")
print("File exists:", os.path.isfile(manifest_output_path))
print("Reloaded shape:", reloaded_manifest.shape)
print("Column order correct:",
      reloaded_manifest.columns.tolist() == manifest.columns.tolist())

print("\n=== Data Integrity ===")
print("Missing values:", reloaded_manifest.isna().sum().sum())
print("Exact duplicate rows:", reloaded_manifest.duplicated().sum())
print("Unique filenames:", reloaded_manifest["file_name"].nunique())
print("Unique post IDs:", reloaded_manifest["post_id"].nunique())

print("\n=== Comparison with Original DataFrame ===")
print("Row counts match:",
      len(reloaded_manifest) == len(manifest))

print("Filenames match:",
      reloaded_manifest["file_name"].equals(manifest["file_name"]))

print("Post IDs match:",
      reloaded_manifest["post_id"].equals(
          manifest["post_id"].astype("string")
      ))

print("Snapshot timestamps match:",
      reloaded_manifest["snapshot_ts"].equals(manifest["snapshot_ts"]))

print("Current flags match:",
      reloaded_manifest["is_current"].equals(manifest["is_current"]))

print("Copy-name flags match:",
      reloaded_manifest["is_copy_name"].equals(manifest["is_copy_name"]))

print("Snapshot ranks match:",
      reloaded_manifest["snapshot_rank"].equals(manifest["snapshot_rank"]))


# In[718]:



# Step 34: Diagnose manifest comparison failures

print("=== Index and Data Type Checks ===")
print("Original index starts:", manifest.index[:5].tolist())
print("Reloaded index starts:", reloaded_manifest.index[:5].tolist())

print("\nOriginal dtypes:")
print(manifest.dtypes)

print("\nReloaded dtypes:")
print(reloaded_manifest.dtypes)

print("\n=== Compare Values After Resetting Index ===")

columns_to_check = [
    "file_name",
    "source_type",
    "post_id",
    "post_url",
    "snapshot_ts",
    "snapshot_rank",
    "is_current",
    "is_copy_name"
]

for col in columns_to_check:
    original = manifest[col].reset_index(drop=True)
    reloaded = reloaded_manifest[col].reset_index(drop=True)

    # Normalize post IDs to string for a fair comparison.
    if col == "post_id":
        original = original.astype("string")
        reloaded = reloaded.astype("string")

    matches = original.equals(reloaded)
    print(f"{col}: {matches}")

    if not matches:
        differences = original.ne(reloaded).fillna(
            original.isna() & reloaded.isna()
        )
        mismatch_positions = differences[~differences].index.tolist()

        # Find actual unequal positions, handling missing values safely.
        unequal_positions = []
        for i in range(len(original)):
            a, b = original.iloc[i], reloaded.iloc[i]
            if pd.isna(a) and pd.isna(b):
                continue
            if a != b:
                unequal_positions.append(i)

        print("  Unequal value count:", len(unequal_positions))
        if unequal_positions:
            i = unequal_positions[0]
            print("  First mismatch at row position:", i)
            print("  Original:", repr(original.iloc[i]))
            print("  Reloaded:", repr(reloaded.iloc[i]))


# In[719]:



# Step 35: Check key project dataframes and exported files

key_variables = [
    "manifest",
    "posts_current",
    "snapshot_fact",
    "demographics_snapshot_fact",
    "postanalytics_field_inventory_df"
]

print("=== Key Dataframe Availability ===")

for var_name in key_variables:
    if var_name in globals():
        obj = globals()[var_name]
        if hasattr(obj, "shape"):
            print(f"{var_name}: Available | Shape: {obj.shape}")
        else:
            print(f"{var_name}: Available | Type: {type(obj).__name__}")
    else:
        print(f"{var_name}: Not currently defined")

print("\n=== Exported CSV Files ===")

processed_dir = r"C:\Users\Shifa\processed"

for filename in [
    "posts_current.csv",
    "snapshot_fact.csv",
    "demographics_snapshot_fact.csv",
    "file_manifest.csv"
]:
    path = os.path.join(processed_dir, filename)
    print(f"{filename}: {'Exists' if os.path.isfile(path) else 'Missing'}")


# In[720]:



# Step 36: Inspect the analytics field inventory

print("=== Field Inventory Overview ===")
print("Shape:", postanalytics_field_inventory_df.shape)
print("Columns:", postanalytics_field_inventory_df.columns.tolist())

print("\n=== First 15 Rows ===")
display(postanalytics_field_inventory_df.head(15))

print("\n=== Data Types ===")
print(postanalytics_field_inventory_df.dtypes)

print("\n=== Missing Values ===")
print(postanalytics_field_inventory_df.isna().sum())

print("\n=== Exact Duplicate Rows ===")
print(postanalytics_field_inventory_df.duplicated().sum())


# In[721]:



# Step 37: Investigate duplicate filename-field combinations

field_key = ["file_name", "field_name"]

duplicate_mask = postanalytics_field_inventory_df.duplicated(
    subset=field_key,
    keep=False
)

duplicate_records = postanalytics_field_inventory_df.loc[
    duplicate_mask
].sort_values(field_key)

print("=== Duplicate Inventory Analysis ===")
print("Total inventory rows:", len(postanalytics_field_inventory_df))
print("Rows involved in duplicate combinations:", int(duplicate_mask.sum()))
print(
    "Distinct duplicated filename-field combinations:",
    duplicate_records.drop_duplicates(subset=field_key).shape[0]
)

print("\n=== Sample Duplicate Combinations ===")
display(
    duplicate_records.groupby(field_key, dropna=False)
    .size()
    .reset_index(name="occurrences")
    .sort_values("occurrences", ascending=False)
    .head(15)
)

print("\n=== Files Affected ===")
print(
    "Number of affected files:",
    duplicate_records["file_name"].nunique()
)

print("\n=== Field Names Involved ===")
print(
    duplicate_records["field_name"]
    .value_counts()
    .head(15)
)


# In[722]:



# Step 38: Inspect one affected file's field inventory

sample_file = (
    duplicate_records["file_name"].iloc[0]
)

sample_inventory = postanalytics_field_inventory_df.loc[
    postanalytics_field_inventory_df["file_name"] == sample_file
].copy()

print("Sample workbook:")
print(sample_file)

print("\nTotal inventory rows for this workbook:",
      len(sample_inventory))

print("\nUnique field names:",
      sample_inventory["field_name"].nunique())

print("\nField inventory in original order:")
display(sample_inventory.reset_index(drop=True))

print("\nRepeated fields in this workbook:")
display(
    sample_inventory[
        sample_inventory.duplicated(
            subset=["field_name"],
            keep=False
        )
    ].sort_values("field_name")
)


# In[724]:



# Step 40: Verify repeated labels in the original Excel worksheet

sample_path = raw_folder / sample_file

sample_sheet = pd.read_excel(
    sample_path,
    sheet_name="PERFORMANCE",
    header=None
)

print("Workbook:", sample_file)
print("Worksheet shape:", sample_sheet.shape)

print("\n=== First-column labels with Excel row numbers ===")

for row_position, value in sample_sheet.iloc[:, 0].items():
    if pd.notna(value) and str(value).strip():
        print(f"Excel row {row_position + 1}: {str(value).strip()}")



# In[725]:



# Step 41: Summarize field names across the analytics workbooks

field_summary = (
    postanalytics_field_inventory_df
    .groupby("field_name")
    .agg(
        inventory_rows=("file_name", "size"),
        files_containing_field=("file_name", "nunique")
    )
    .sort_values(
        ["files_containing_field", "field_name"],
        ascending=[False, True]
    )
    .reset_index()
)

print("=== Field Inventory Summary ===")
print("Distinct field names:", field_summary["field_name"].nunique())
print("Total inventory rows:", len(postanalytics_field_inventory_df))
print("Distinct workbooks:", postanalytics_field_inventory_df["file_name"].nunique())

print("\n=== Most Common Fields ===")
display(field_summary.head(25))

print("\n=== Highlight Section Labels ===")
display(
    field_summary[
        field_summary["field_name"].str.contains(
            "Highlights", case=False, na=False
        )
    ]
)


# In[726]:



# Step 42: Validate inventory coverage against the canonical manifest

canonical_pa_files = set(
    manifest.loc[
        manifest["source_type"] == "PostAnalytics",
        "file_name"
    ]
)

inventory_files = set(
    postanalytics_field_inventory_df["file_name"].dropna()
)

print("=== Inventory Coverage Validation ===")
print("Canonical PostAnalytics files:", len(canonical_pa_files))
print("Files represented in inventory:", len(inventory_files))
print("Canonical files missing from inventory:",
      len(canonical_pa_files - inventory_files))
print("Inventory files outside canonical set:",
      len(inventory_files - canonical_pa_files))

if canonical_pa_files - inventory_files:
    print("\nSample missing filenames:")
    print(sorted(canonical_pa_files - inventory_files)[:10])

if inventory_files - canonical_pa_files:
    print("\nSample unexpected filenames:")
    print(sorted(inventory_files - canonical_pa_files)[:10])

print("\nCoverage complete:",
      canonical_pa_files == inventory_files)


# In[727]:



# Step 43: Check for existing metric-mapping objects

mapping_keywords = (
    "metric",
    "mapping",
    "field",
    "schema",
    "inventory"
)

print("=== Existing Mapping-Related Variables ===")

for name in sorted(globals()):
    if any(keyword in name.lower() for keyword in mapping_keywords):
        obj = globals()[name]

        if isinstance(obj, pd.DataFrame):
            print(f"{name}: DataFrame {obj.shape}")
        elif isinstance(obj, (dict, list, tuple, set)):
            print(f"{name}: {type(obj).__name__}, length={len(obj)}")


# In[728]:



# Step 44: Inspect existing metric dataframes

tables_to_inspect = {
    "metrics_long": metrics_long,
    "pa_metrics": pa_metrics,
    "raw_fields_long": raw_fields_long
}

for name, df in tables_to_inspect.items():
    print(f"\n{'=' * 60}")
    print(f"DATAFRAME: {name}")
    print("=" * 60)

    print("\nShape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes.to_string())

    print("\nFirst 5 rows:")
    display(df.head())


# In[729]:



# Step 45: Audit existing metric mappings

print("=== Standardized Metric Coverage ===")
print("Total rows:", len(metrics_long))
print("Rows with missing metric:", metrics_long["metric"].isna().sum())
print("Distinct standardized metrics:", metrics_long["metric"].nunique(dropna=True))

print("\n=== Most Common Standardized Metrics ===")
display(
    metrics_long["metric"]
    .value_counts(dropna=False)
    .rename_axis("metric")
    .reset_index(name="row_count")
    .head(25)
)

print("\n=== Raw Labels Mapped to Multiple Metrics ===")
label_mapping_counts = (
    metrics_long.dropna(subset=["label", "metric"])
    .groupby("label")["metric"]
    .nunique()
    .sort_values(ascending=False)
)

display(
    label_mapping_counts[label_mapping_counts > 1]
    .rename("distinct_metric_count")
    .reset_index()
    .head(25)
)

print("\n=== Labels With Missing Metric Mapping ===")
display(
    metrics_long.loc[
        metrics_long["metric"].isna(),
        ["source_type", "section", "label", "value_raw"]
    ]
    .drop_duplicates()
    .head(30)
)


# In[731]:



# Step 46: Review raw-label-to-metric mapping rules

metric_mapping_audit = (
    metrics_long[
        ["source_type", "section_norm", "label", "metric"]
    ]
    .drop_duplicates()
    .sort_values(
        ["source_type", "section_norm", "label"],
        na_position="first"
    )
    .reset_index(drop=True)
)

print("=== Mapping Rule Audit ===")
print("Distinct mapping combinations:", len(metric_mapping_audit))

display(metric_mapping_audit.to_string(index=False))


# In[732]:



# Step 47: Inspect potentially overlapping metric labels

labels_to_review = [
    "Impressions",
    "Total Impressions",
    "Views",
    "Video views",
    "Watch time",
    "Average watch time"
]

metric_label_review = metrics_long.loc[
    metrics_long["label"].isin(labels_to_review),
    [
        "source_type",
        "file_name",
        "section",
        "label",
        "value_raw",
        "metric"
    ]
].copy()

print("=== Row Counts by Source, Section, Label and Mapping ===")
display(
    metric_label_review.groupby(
        ["source_type", "section", "label", "metric"],
        dropna=False
    )
    .size()
    .reset_index(name="row_count")
    .sort_values(["label", "source_type", "section"])
)

print("\n=== Sample Extracted Values ===")
display(
    metric_label_review
    .sort_values(["label", "source_type", "file_name"])
    .groupby(["source_type", "label"], dropna=False)
    .head(3)
    .reset_index(drop=True)
)


# In[733]:



# Step 48: Trace Total Impressions records to manifest metadata

total_impressions_records = metrics_long.loc[
    metrics_long["label"].eq("Total Impressions"),
    ["file_name", "source_type", "section", "label", "value_raw", "metric"]
].copy()

total_impressions_trace = total_impressions_records.merge(
    manifest[
        [
            "file_name",
            "post_id",
            "snapshot_ts",
            "snapshot_rank",
            "is_current",
            "is_copy_name"
        ]
    ],
    on="file_name",
    how="left",
    validate="many_to_one",
    indicator=True
)

print("=== Total Impressions Lineage ===")
display(
    total_impressions_trace.sort_values(
        ["post_id", "snapshot_ts"]
    ).reset_index(drop=True)
)

print("\n=== Manifest Join Validation ===")
print(total_impressions_trace["_merge"].value_counts().to_dict())


# In[735]:


source_sheet.iloc[:, 0].astype("string").str.strip().eq("Total Impressions")


# In[736]:



# Step 49: Inspect source worksheet context for Total Impressions

for file_name in total_impressions_records["file_name"].drop_duplicates():
    file_path = raw_folder / file_name

    print(f"\n{'=' * 70}")
    print("Workbook:", file_name)
    print("=" * 70)

    source_sheet = pd.read_excel(
        file_path,
        sheet_name="PERFORMANCE",
        header=None
    )

    labels = (
        source_sheet.iloc[:, 0]
        .astype("string")
        .str.strip()
    )

    matches = source_sheet.index[
        labels.eq("Total Impressions").fillna(False)
    ].tolist()

    print("Matching worksheet rows:", [idx + 1 for idx in matches])

    for idx in matches:
        start = max(0, idx - 3)
        end = min(len(source_sheet), idx + 4)

        print(f"\nWorksheet rows {start + 1} to {end}:")
        display(source_sheet.iloc[start:end].reset_index(drop=True))


# In[737]:



# Step 50: Identify standardized metrics with multiple source labels

mapping_label_groups = (
    metrics_long[
        ["metric", "source_type", "section_norm", "label"]
    ]
    .drop_duplicates()
    .groupby("metric")
    .agg(
        distinct_labels=("label", "nunique"),
        source_labels=(
            "label",
            lambda s: sorted(s.dropna().unique().tolist())
        ),
        source_types=(
            "source_type",
            lambda s: sorted(s.dropna().unique().tolist())
        )
    )
    .reset_index()
)

multi_label_metrics = (
    mapping_label_groups.loc[
        mapping_label_groups["distinct_labels"] > 1
    ]
    .sort_values(
        ["distinct_labels", "metric"],
        ascending=[False, True]
    )
)

print("=== Metrics With Multiple Source Labels ===")
print("Metrics with multiple labels:", len(multi_label_metrics))

display(multi_label_metrics)


# In[738]:



# Step 51: Inspect datasets and CSV exports before SQL

import os

print("=== In-Memory Dataset Inventory ===")

datasets_to_check = {
    "posts_current": posts_current,
    "snapshot_fact": snapshot_fact,
    "demographics_snapshot_fact": demographics_snapshot_fact,
    "metrics_long": metrics_long
}

for name, df in datasets_to_check.items():
    print(f"\n{name}")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())

print("\n=== Processed CSV Export Inventory ===")

csv_files_to_check = [
    "posts_current.csv",
    "snapshot_fact.csv",
    "demographics_snapshot_fact.csv",
    "file_manifest.csv",
    "metrics_long.csv"
]

for filename in csv_files_to_check:
    path = os.path.join(processed_dir, filename)

    if os.path.isfile(path):
        size_kb = os.path.getsize(path) / 1024
        print(f"{filename}: EXISTS ({size_kb:.1f} KB)")
    else:
        print(f"{filename}: NOT FOUND")


# In[739]:



# Step 53: Validate post-level keys and duplicates

print("=== Snapshot Fact Key Check ===")

print(
    "Missing post_id:",
    snapshot_fact["post_id"].isna().sum()
)

print(
    "Duplicate post_id + snapshot_ts:",
    snapshot_fact.duplicated(
        subset=["post_id", "snapshot_ts"]
    ).sum()
)

print("\n=== Current Posts Key Check ===")

print(
    "Missing post_id:",
    posts_current["post_id"].isna().sum()
)

print(
    "Duplicate post_id:",
    posts_current["post_id"].duplicated().sum()
)

print("\n=== Snapshot Flag Check ===")

print(
    "Current snapshot rows:",
    snapshot_fact["is_current"].sum()
)

print(
    "Rows in posts_current:",
    len(posts_current)
)


# In[740]:



# Step 54: Inspect duplicate post snapshot keys

duplicate_key_rows = snapshot_fact.loc[
    snapshot_fact.duplicated(
        subset=["post_id", "snapshot_ts"],
        keep=False
    )
].sort_values(["post_id", "snapshot_ts"])

print("=== Duplicate Snapshot Key Details ===")
print("Rows involved:", len(duplicate_key_rows))

display(duplicate_key_rows)


# In[741]:



# Step 55: Compare the duplicate records field by field

row_a = duplicate_key_rows.iloc[0]
row_b = duplicate_key_rows.iloc[1]

excluded_columns = {"snapshot_rank", "is_current"}
differences = []

for col in duplicate_key_rows.columns:
    if col in excluded_columns:
        continue

    value_a = row_a[col]
    value_b = row_b[col]

    both_missing = pd.isna(value_a) and pd.isna(value_b)

    if not both_missing and value_a != value_b:
        differences.append({
            "column": col,
            "record_1": value_a,
            "record_2": value_b
        })

print("=== Differences Beyond Snapshot Selection Metadata ===")

if differences:
    display(pd.DataFrame(differences))
else:
    print("No differences found in the compared columns.")

print("\n=== Selection Metadata ===")
print("Record 1 — rank:", row_a["snapshot_rank"],
      "| is_current:", row_a["is_current"])
print("Record 2 — rank:", row_b["snapshot_rank"],
      "| is_current:", row_b["is_current"])


# In[743]:



# Step 56: Check whether the manifest already identifies the copied workbook

target_files = [
    "PostAnalytics_ShifaNaaz_6974940149876965376.xlsx",
    "PostAnalytics_ShifaNaaz_6974940149876965376 - Copy.xlsx"
]

manifest_check = manifest.loc[
    manifest["file_name"].isin(target_files)
].copy()

columns_to_show = [
    col for col in [
        "file_name",
        "source_type",
        "snapshot_ts",
        "post_id",
        "snapshot_rank",
        "is_current",
        "is_copy_name"
    ]
    if col in manifest_check.columns
]

print("=== Manifest Verification ===")
print("Matching manifest rows:", len(manifest_check))
display(manifest_check[columns_to_show])


# In[744]:



# Step 57: Audit all duplicate snapshot keys against the manifest

duplicate_key_mask = snapshot_fact.duplicated(
    subset=["post_id", "snapshot_ts"],
    keep=False
)

all_duplicate_keys = snapshot_fact.loc[
    duplicate_key_mask
].copy()

print("=== Overall Duplicate-Key Audit ===")
print("Rows involved in duplicate keys:", len(all_duplicate_keys))

print(
    "Distinct duplicate key combinations:",
    all_duplicate_keys[
        ["post_id", "snapshot_ts"]
    ].drop_duplicates().shape[0]
)

if not all_duplicate_keys.empty:
    display(
        all_duplicate_keys[
            ["post_id", "snapshot_ts", "snapshot_rank", "is_current"]
        ].sort_values(["post_id", "snapshot_ts", "snapshot_rank"])
    )

print("\n=== Manifest Copy-Flag Summary ===")
print(manifest["is_copy_name"].value_counts(dropna=False))


# In[746]:



# Step 58: Create a curated snapshot table without the verified copied row

# The duplicate row's filename is stored in the index, not a column.
copy_file_names = set(
    manifest.loc[
        manifest["is_copy_name"].eq(True),
        "file_name"
    ]
)

# Identify only duplicate-key rows whose index is a filename
duplicate_copy_index = duplicate_key_rows.index[
    duplicate_key_rows.index.isin(copy_file_names)
]

print("=== Verified Copy Exclusion ===")
print("Copied duplicate rows identified:", len(duplicate_copy_index))

# Preserve the original DataFrame; create a separate curated version
snapshot_fact_curated = snapshot_fact.drop(
    index=duplicate_copy_index
).copy()

print("\n=== Curated Snapshot Validation ===")
print("Original rows:", len(snapshot_fact))
print("Curated rows:", len(snapshot_fact_curated))

print(
    "Duplicate post_id + snapshot_ts keys remaining:",
    snapshot_fact_curated.duplicated(
        subset=["post_id", "snapshot_ts"]
    ).sum()
)

print(
    "Current rows in curated table:",
    snapshot_fact_curated["is_current"].sum()
)

print(
    "Current post IDs match posts_current:",
    set(
        snapshot_fact_curated.loc[
            snapshot_fact_curated["is_current"], "post_id"
        ]
    ) == set(posts_current["post_id"])
)


# In[747]:



# Step 59: Export the validated curated snapshot

from pathlib import Path

curated_snapshot_path = Path(processed_dir) / "snapshot_fact_curated.csv"

snapshot_fact_curated.to_csv(
    curated_snapshot_path,
    index=False
)

# Read it back to validate the export
snapshot_fact_curated_check = pd.read_csv(
    curated_snapshot_path
)

print("=== Curated Snapshot Export Validation ===")
print("File exists:", curated_snapshot_path.exists())
print("Exported rows:", len(snapshot_fact_curated_check))
print("Expected rows:", len(snapshot_fact_curated))
print(
    "Column names match:",
    list(snapshot_fact_curated_check.columns)
    == list(snapshot_fact_curated.columns)
)
print(
    "Duplicate snapshot keys after export:",
    snapshot_fact_curated_check.duplicated(
        subset=["post_id", "snapshot_ts"]
    ).sum()
)
print("Export path:", curated_snapshot_path)


# In[748]:



# Step 60: Verify files for the MySQL handoff

from pathlib import Path

sql_handoff_files = [
    "posts_current.csv",
    "snapshot_fact_curated.csv",
    "demographics_snapshot_fact.csv",
    "file_manifest.csv"
]

print("=== SQL Handoff File Check ===")

for file_name in sql_handoff_files:
    file_path = Path(processed_dir) / file_name
    print(
        f"{file_name}: "
        f"{'EXISTS' if file_path.exists() else 'MISSING'}"
    )


# In[749]:



# Step 61: Verify the MySQL connection and target database

from sqlalchemy import create_engine, text

# Reuse your existing MySQL connection settings if already defined.
# Do not paste your password into the chat.

print("Checking MySQL connection setup...")

print("SQLAlchemy engine already defined:", "engine" in globals())
print("Database name:", "linkedin_post")


# In[750]:



# Step 62: Check required MySQL connection libraries

import importlib.util

required_libraries = ["sqlalchemy", "pymysql"]

for library in required_libraries:
    installed = importlib.util.find_spec(library) is not None
    print(f"{library}: {'INSTALLED' if installed else 'NOT INSTALLED'}")


# In[4]:



# Step 63: Test direct MySQL authentication

import pymysql
from getpass import getpass

mysql_password = getpass("Enter your MySQL password: ")

try:
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=mysql_password,
        database="linkedin_post",
        connect_timeout=5,
        read_timeout=5,
        write_timeout=5
    )

    print("MySQL login successful!")

    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE(), VERSION()")
        result = cursor.fetchone()

        print("Database:", result[0])
        print("MySQL version:", result[1])

    connection.close()

except Exception as error:
    print("MySQL login failed.")
    print("Error type:", type(error).__name__)
    print("Details:", str(error)[:500])


# In[5]:



# Step 64: Create and test the SQLAlchemy engine

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from getpass import getpass

mysql_password = getpass("Enter your MySQL password: ")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=mysql_password,
    host="127.0.0.1",
    port=3306,
    database="linkedin_post",
    query={"connect_timeout": "5"}
)

engine = create_engine(
    connection_url,
    pool_pre_ping=True,
    connect_args={
        "connect_timeout": 5,
        "read_timeout": 5,
        "write_timeout": 5
    }
)

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DATABASE(), VERSION()")
        ).fetchone()

        print("SQLAlchemy connection successful!")
        print("Database:", result[0])
        print("MySQL version:", result[1])

except Exception as error:
    print("SQLAlchemy connection failed.")
    print("Error type:", type(error).__name__)
    print("Details:", str(error)[:500])


# In[6]:



# Step 67: Inspect existing tables in linkedin_post

from sqlalchemy import inspect

inspector = inspect(engine)
existing_tables = inspector.get_table_names()

print("=== Existing Tables in linkedin_post ===")

if existing_tables:
    for table_name in existing_tables:
        print("-", table_name)
else:
    print("No tables found in this database.")


# In[8]:



# Step 68: Preview datasets before importing into MySQL

from pathlib import Path
import pandas as pd

processed_dir = Path(r"C:\Users\Shifa\processed")

sql_handoff_files = {
    "posts_current": "posts_current.csv",
    "snapshot_fact_curated": "snapshot_fact_curated.csv",
    "demographics_snapshot_fact": "demographics_snapshot_fact.csv",
    "file_manifest": "file_manifest.csv"
}

for table_name, file_name in sql_handoff_files.items():
    file_path = processed_dir / file_name

    print(f"\n=== {table_name} ===")
    print("File exists:", file_path.exists())

    if not file_path.exists():
        print("File not found:", file_path)
        continue

    df_preview = pd.read_csv(file_path, nrows=5)

    print("Columns:", len(df_preview.columns))
    print("Column names:")
    print(df_preview.columns.tolist())
    display(df_preview.head(2))


# In[9]:



# Step 69: Validate dataset sizes and important data types

from pathlib import Path
import pandas as pd

processed_dir = Path(r"C:\Users\Shifa\processed")

sql_handoff_files = {
    "posts_current": "posts_current.csv",
    "snapshot_fact_curated": "snapshot_fact_curated.csv",
    "demographics_snapshot_fact": "demographics_snapshot_fact.csv",
    "file_manifest": "file_manifest.csv"
}

for table_name, file_name in sql_handoff_files.items():
    file_path = processed_dir / file_name
    df = pd.read_csv(file_path)

    print(f"\n=== {table_name} ===")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Duplicate column names:", df.columns.duplicated().sum())
    print("Missing post_id values:",
          df["post_id"].isna().sum() if "post_id" in df.columns else "N/A")

    important_columns = [
        col for col in [
            "post_id", "snapshot_ts", "is_current",
            "snapshot_rank", "percentage", "is_copy_name"
        ]
        if col in df.columns
    ]

    print("\nImportant column data types:")
    print(df[important_columns].dtypes)


# In[10]:



# Step 70: Prepare datasets for SQL import

import pandas as pd
from pathlib import Path

processed_dir = Path(r"C:\Users\Shifa\processed")

sql_datasets = {}

for table_name, file_name in sql_handoff_files.items():
    df = pd.read_csv(
        processed_dir / file_name,
        dtype={"post_id": "string"}
    )

    # Convert timestamp columns to proper datetime values
    for col in ["snapshot_ts", "publish_ts_utc", "publish_ts_ist"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="raise")

    # Preserve mixed percentage values, including entries such as "< 1%"
    if "percentage" in df.columns:
        df["percentage"] = df["percentage"].astype("string")

    sql_datasets[table_name] = df

    print(f"\n=== {table_name} ===")
    print("Shape:", df.shape)
    print("post_id type:",
          df["post_id"].dtype if "post_id" in df.columns else "N/A")
    print("snapshot_ts type:",
          df["snapshot_ts"].dtype if "snapshot_ts" in df.columns else "N/A")

print("\nAll four datasets prepared in memory.")
print("Total rows:", sum(len(df) for df in sql_datasets.values()))


# In[11]:



# Step 71: Review column data types before creating MySQL tables

for table_name, df in sql_datasets.items():
    print(f"\n=== {table_name} ===")

    schema_review = pd.DataFrame({
        "column_name": df.columns,
        "pandas_dtype": [str(df[col].dtype) for col in df.columns],
        "missing_values": [int(df[col].isna().sum()) for col in df.columns],
        "distinct_values": [int(df[col].nunique(dropna=True)) for col in df.columns]
    })

    display(schema_review)


# In[12]:



# Step 72: Final safety check before SQL table creation

from sqlalchemy import inspect

inspector = inspect(engine)
existing_tables = inspector.get_table_names()

print("Database: linkedin_post")
print("Existing tables:", existing_tables)

if len(existing_tables) == 0:
    print("\nSAFE TO PROCEED: No existing tables will be overwritten.")
else:
    print("\nSTOP: Tables already exist. Review them before importing.")


# In[13]:



# Step 73: Import posts_current into MySQL

from sqlalchemy import types, inspect

table_name = "posts_current"
df = sql_datasets[table_name]

# Confirm the destination table does not already exist
if table_name in inspect(engine).get_table_names():
    print(f"STOP: Table '{table_name}' already exists. Nothing imported.")
else:
    sql_dtypes = {
        "file_name": types.String(255),
        "post_url": types.Text(),
        "post_id": types.String(30),
        "source_type": types.String(50),
        "snapshot_ts": types.DateTime(),
        "publish_ts_utc": types.DateTime(),
        "publish_ts_ist": types.DateTime(),
        "is_current": types.Boolean(),
        "snapshot_rank": types.Integer(),
        "post_age_days": types.Integer()
    }

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="fail",
        index=False,
        dtype=sql_dtypes,
        chunksize=100
    )

    print(f"Import completed for '{table_name}'.")
    print("Rows submitted:", len(df))
    print("Columns submitted:", len(df.columns))


# In[14]:



# Step 74: Validate posts_current in MySQL

from sqlalchemy import text, inspect

with engine.connect() as connection:
    sql_row_count = connection.execute(
        text("SELECT COUNT(*) FROM posts_current")
    ).scalar_one()

    sql_post_id_count = connection.execute(
        text("""
            SELECT COUNT(DISTINCT post_id)
            FROM posts_current
        """)
    ).scalar_one()

    sql_missing_post_ids = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM posts_current
            WHERE post_id IS NULL OR post_id = ''
        """)
    ).scalar_one()

expected_rows = len(sql_datasets["posts_current"])

print("=== MySQL Import Validation ===")
print("Expected rows:", expected_rows)
print("Rows in MySQL:", sql_row_count)
print("Distinct post IDs:", sql_post_id_count)
print("Missing post IDs:", sql_missing_post_ids)
print("Row count matches:", sql_row_count == expected_rows)
print("Expected unique post IDs:", sql_datasets["posts_current"]["post_id"].nunique())


# In[15]:



# Step 75: Import curated historical snapshots into MySQL

from sqlalchemy import types, inspect

table_name = "snapshot_fact_curated"
df = sql_datasets[table_name]

if table_name in inspect(engine).get_table_names():
    print(f"STOP: Table '{table_name}' already exists. Nothing imported.")
else:
    sql_dtypes = {
        "post_url": types.Text(),
        "post_id": types.String(30),
        "source_type": types.String(50),
        "snapshot_ts": types.DateTime(),
        "publish_ts_utc": types.DateTime(),
        "publish_ts_ist": types.DateTime(),
        "is_current": types.Boolean(),
        "snapshot_rank": types.Integer(),
        "post_age_days": types.Integer()
    }

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="fail",
        index=False,
        dtype=sql_dtypes,
        chunksize=100
    )

    print(f"Import completed for '{table_name}'.")
    print("Rows submitted:", len(df))
    print("Columns submitted:", len(df.columns))


# In[16]:



# Step 76: Validate snapshot_fact_curated in MySQL

from sqlalchemy import text

with engine.connect() as connection:
    row_count = connection.execute(
        text("SELECT COUNT(*) FROM snapshot_fact_curated")
    ).scalar_one()

    distinct_posts = connection.execute(
        text("SELECT COUNT(DISTINCT post_id) FROM snapshot_fact_curated")
    ).scalar_one()

    duplicate_keys = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM (
                SELECT post_id, snapshot_ts
                FROM snapshot_fact_curated
                GROUP BY post_id, snapshot_ts
                HAVING COUNT(*) > 1
            ) AS duplicate_groups
        """)
    ).scalar_one()

    current_rows = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM snapshot_fact_curated
            WHERE is_current = TRUE
        """)
    ).scalar_one()

print("=== Historical Snapshot Validation ===")
print("Expected rows:", len(sql_datasets["snapshot_fact_curated"]))
print("Rows in MySQL:", row_count)
print("Distinct post IDs:", distinct_posts)
print("Duplicate post_id + snapshot_ts groups:", duplicate_keys)
print("Current snapshot rows:", current_rows)

print("Row count matches:", row_count == len(sql_datasets["snapshot_fact_curated"]))
print("Duplicate check passed:", duplicate_keys == 0)
print("Current rows match:", current_rows == int(sql_datasets["snapshot_fact_curated"]["is_current"].sum()))


# In[17]:



# Step 77: Import demographics_snapshot_fact into MySQL

from sqlalchemy import types, inspect

table_name = "demographics_snapshot_fact"
df = sql_datasets[table_name]

if table_name in inspect(engine).get_table_names():
    print(f"STOP: Table '{table_name}' already exists. Nothing imported.")
else:
    sql_dtypes = {
        "category": types.String(100),
        "value": types.Text(),
        "percentage": types.String(30),
        "file_name": types.String(255),
        "post_id": types.String(30),
        "source_type": types.String(50),
        "snapshot_ts": types.DateTime(),
        "is_current": types.Boolean()
    }

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="fail",
        index=False,
        dtype=sql_dtypes,
        chunksize=250
    )

    print(f"Import completed for '{table_name}'.")
    print("Rows submitted:", len(df))
    print("Columns submitted:", len(df.columns))


# In[18]:



# Step 78: Validate demographics_snapshot_fact in MySQL

from sqlalchemy import text

with engine.connect() as connection:
    row_count = connection.execute(
        text("SELECT COUNT(*) FROM demographics_snapshot_fact")
    ).scalar_one()

    distinct_posts = connection.execute(
        text("SELECT COUNT(DISTINCT post_id) FROM demographics_snapshot_fact")
    ).scalar_one()

    current_rows = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM demographics_snapshot_fact
            WHERE is_current = TRUE
        """)
    ).scalar_one()

    historical_rows = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM demographics_snapshot_fact
            WHERE is_current = FALSE
        """)
    ).scalar_one()

    missing_post_ids = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM demographics_snapshot_fact
            WHERE post_id IS NULL OR post_id = ''
        """)
    ).scalar_one()

    percentage_values = connection.execute(
        text("""
            SELECT
                SUM(CASE WHEN percentage = '< 1%' THEN 1 ELSE 0 END)
            FROM demographics_snapshot_fact
        """)
    ).scalar_one()

expected_df = sql_datasets["demographics_snapshot_fact"]

print("=== Demographics Import Validation ===")
print("Expected rows:", len(expected_df))
print("Rows in MySQL:", row_count)
print("Distinct posts:", distinct_posts)
print("Current rows:", current_rows)
print("Historical rows:", historical_rows)
print("Missing post IDs:", missing_post_ids)
print("Values preserved as '< 1%':", percentage_values)

print("Row count matches:", row_count == len(expected_df))
print("Current/historical totals match:",
      current_rows + historical_rows == row_count)


# In[19]:



# Step 79: Import file_manifest into MySQL

from sqlalchemy import types, inspect

table_name = "file_manifest"
df = sql_datasets[table_name]

if table_name in inspect(engine).get_table_names():
    print(f"STOP: Table '{table_name}' already exists. Nothing imported.")
else:
    sql_dtypes = {
        "file_name": types.String(255),
        "source_type": types.String(50),
        "snapshot_ts": types.DateTime(),
        "post_id": types.String(30),
        "post_url": types.Text(),
        "snapshot_rank": types.Integer(),
        "is_current": types.Boolean(),
        "is_copy_name": types.Boolean()
    }

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="fail",
        index=False,
        dtype=sql_dtypes,
        chunksize=100
    )

    print(f"Import completed for '{table_name}'.")
    print("Rows submitted:", len(df))
    print("Columns submitted:", len(df.columns))


# In[20]:



# Step 80: Validate file_manifest and inspect all imported tables

from sqlalchemy import text, inspect

with engine.connect() as connection:
    manifest_count = connection.execute(
        text("SELECT COUNT(*) FROM file_manifest")
    ).scalar_one()

    missing_file_names = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM file_manifest
            WHERE file_name IS NULL OR file_name = ''
        """)
    ).scalar_one()

    copy_file_count = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM file_manifest
            WHERE is_copy_name = TRUE
        """)
    ).scalar_one()

    current_file_count = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM file_manifest
            WHERE is_current = TRUE
        """)
    ).scalar_one()

print("=== file_manifest Validation ===")
print("Expected rows:", len(sql_datasets["file_manifest"]))
print("Rows in MySQL:", manifest_count)
print("Missing file names:", missing_file_names)
print("Copy-named files:", copy_file_count)
print("Current files:", current_file_count)
print("Row count matches:",
      manifest_count == len(sql_datasets["file_manifest"]))

print("\n=== All Tables in linkedin_post ===")

inspector = inspect(engine)

for table_name in sorted(inspector.get_table_names()):
    with engine.connect() as connection:
        row_count = connection.execute(
            text(f"SELECT COUNT(*) FROM `{table_name}`")
        ).scalar_one()

    print(f"{table_name}: {row_count} rows")


# In[1]:


# Import tools for working with folders and copying files
from pathlib import Path
import shutil

# Folder where the notebook already saved the CSV files
source_dir = Path(r"C:\Users\Shifa\processed")

# Your project folder (change this path if you want a different place)
project_dir = Path(r"C:\Users\Shifa\OneDrive\Resume\Linkedin post Analysis\processed")

# Create the destination folder if it does not exist yet
project_dir.mkdir(parents=True, exist_ok=True)

# Copy every CSV file from the old folder to the project folder
for csv_file in source_dir.glob("*.csv"):
    shutil.copy(csv_file, project_dir / csv_file.name)
    print("Copied:", csv_file.name)

# Show what is now inside the project folder
print("\nFiles in project folder:")
for item in sorted(project_dir.iterdir()):
    print("-", item.name)


# In[ ]:




