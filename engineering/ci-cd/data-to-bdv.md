# How to bring data from ODS to BDV

# 1. Local Prototype
Best practice is write some prototype queries in individual cells on your personal workspace

You can assume that the relevant ODS tables are already present on the ACC environment.

# 2. BDV table Script
Once your prototypes are ready, you can move these queries to a new notebook under `/Workspace/Repos/pmm203@fluvius.be/athena/src/databricks/02. Capability Domains/assetsennet/Bdv/Bdv Tables`

There you will find a [`Template.ipynb`](https://adb-7926212962831610.10.azuredatabricks.net/?o=7926212962831610#notebook/3497450983502764/command/3497450983507644) notebook which you can clone and where you can insert your query.

You should apply the following naming conventions to name your notebook
- **Link** : `L_<entity_name_1>_<entity_name_2>` in alphabetical order
- **Satellite**: `S_<entity_name>_<sattelite_name>`
    - When using the sattelite name `Masterdata` you are talking about the "central object". The amoun tof unique keys in your hub should be equal to the amount of unique keys in your sattellite
- **Link Satellite**: `LS_<link_name>_<satellite_name>`

This is a script where you should just paste your

```python
# Widgets
dbutils.widgets.removeAll()
dbutils.widgets.text("Key vault", "kvss-001", "Key vault")

# Initialize key vault
key_vault = dbutils.widgets.get("Key vault")

# Query read environment
databricks_environment = dbutils.secrets.get(scope = key_vault, key = 'databricks-environment')[1]
```

First you can manually create the tables on the `dataplatform_o` environment. This will run the [BDV Load Notebook](https://adb-7926212962831610.10.azuredatabricks.net/?o=7926212962831610#notebook/3497450983502929/command/3497450983503355)

```python
dbutils.notebook.run("/Workspace/Repos/pmm203@fluvius.be/athena/src/databricks/01. Data Lakehouse/00. Framework/Load/Bdv_Load", 600000, {"Platform_name": "S_Project_Locatie"})

```

[Text](./template.ipynb)
# 3. Release Script

This is located under `/Workspace/Repos/pmm203@fluvius.be/athena/src/databricks/02. Capability Domains/assetsennet/Release/ReleaseScripts/<RELEASE_YEAR>/<RELEASE_YEAR>.<SPRINT_NUMBER>`

# 4. Changes to your BDV table
