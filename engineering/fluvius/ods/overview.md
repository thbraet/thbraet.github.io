# How to get data on the ODS layer
1. Create a data contract ([Template](https://mononline.sharepoint.com/:x:/r/sites/PRJ00120/Gedeelde%20documenten/Product/36.%20Intake%20Databron/_TEMPLATE_Databon_Contract.xlsx?d=w11ffe273009c476b82716fdb347671b1&csf=1&web=1&e=1Zf5hh))
2. Create connection with source system
3. Create delivery kit
    - Manual
    - Accelerator
4. Test delivery kit
5. Push changes to DataMgmt repo

# 1. Creating the datacontract
To know what data to onboard and how to onboard it (e.g. incremental, sensitive fields, ...) a data contract needs to be set up together with business
Please refer to the dedicated [Data Contract](../datacontract.md) page

# 2. Creating the connection with source system
This is something set-up by the platform team.
This is what we call the so called "highway" at Fluvius

# 3. Creating the delivery kit
**Specifiations**
- Server: `sql-datamgt-we-p-001.database.windows.net`
- Database: `sqldb-datamgt-we-p-004`

**How**

Connect using [SQL Server Management Studio](https://learn.microsoft.com/en-us/sql/ssms/sql-server-management-studio-ssms?view=sql-server-ver16)

![image](https://github.com/user-attachments/assets/d2f5b020-5cdb-47ef-95e9-4f67b1c71b52)
![image](https://github.com/user-attachments/assets/af2fa120-2499-4593-9302-2913c561d47f)

## Manual
You need to fill out the following tables.
If you only fill out the first two. you can already load the data to the _landing_ zone. By filling out all four, you can load the data to the ODS table
Details of the meaning for every field can be found in this [notebook](https://adb-7926212962831610.10.azuredatabricks.net/?o=7926212962831610#notebook/1636174388296770/command/1636174388296771)

- `meta.configuration`: One line per   
  ```
  INSERT INTO [meta].[configuration] (
       DataAsset,
       DataAssetGroup,
       DataAssetID,
       DataFactoryPipelineName,
       IngestionMethod,
       HeadCapability,
       RetentionPeriodData,
       DataLandingZone
  ) VALUES (
       'OVLIMABA',
       'SQL Server',
       '021',
       'pl_COPY_OVLIMABA_BronzeLandingPARQUET',
       'Pull',
       'Asset- en Netinformatie',
       'nvt',
       'athena'
   );
  ```
- `meta.dataassetentities`: One line per specified _table_ in your data contract
  ```
  INSERT INTO [meta].[dataassetentities] (
       ADFCopyTable,
       ApplyTechnicalValidation,
       CertificateID,
       DataAssetEntityID,
       DataAssetID,
       Description,
       HasHeader,
       LoadUntilA,
       LoadUntilO,
       LoadUntilP,
       LoadUntilT,
       LoadingScheduleA,
       LoadingScheduleO,
       LoadingScheduleP,
       LoadingScheduleT,
       LoadingTechnique,
       PlatformName,
       Source,
       SourceName,
       SourceSchema,
       SensitivityClassification,
       InformationClassification,
       RLSRule,
       PushMethod,
       Catalog,
       ColumnDelimiter,
       ConfidentialityClass,
       SensitivityClass,
       PriorityWorkflow,
       ApplyHistorization
  ) VALUES (
      'Yes',
       'DT',
       '021_0001',
       '0001',
       '021',
       '',
       'Yes',
       'ODS',
       'ODS',
       'NONE',
       'ODS',
       '0 1 * * *',
       '0 1 * * *',
       '0 1 * * *',
       '0 1 * * *',
       'Incremental',
       'OVLIMABA_AangebodenBrandprogramma',
       'Table',
       'AangebodenBrandprogramma',
       'ovbrandprogramma',
       'Low',
       'Intern',
       '',
       '',
       'dataplatform',
       '',
       '',
       '',
       'Medium',
       'Yes'
  );
  ```
- `meta.columndefinitions`: One line per column for every table specified in the data contract
  ```
  INSERT INTO [meta].[columndefinitions] (
      CertificateID,
      ColumnDescription,
      ColumnName,
      ColumnNumber,
      Format,
      IsSensitive,
      Length,
      LoadColumn,
      LoadIncrementally,
      Mandatory,
      Precision,
      Scale,
      SourceName,
      SourceSchema,
      Trim,
      Type,
      ReplaceStartDateTimeColumn,
      ReplaceEndDateTimeColumn
  ) VALUES (
      '021_0001',
      '',
      'BrandprogrammaId',
      '1',
      '',
      '',
      16,
      'Yes',
      '',
      'Yes',
      '',
      '',
      'AangebodenBrandprogramma',
      'ovbrandprogramma',
      'Yes',
      'string',
      'No',
      'No'
  );
  ```
- `meta.businesskeys`: One line per primary/foreign key for every table in the data contract
  ```
  INSERT INTO [meta].[businesskeys] (
      BusinessKey,
      CertificateID,
      Columns,
      PrimaryKey,
      ReferenceBusinessKey,
      TimestampColumn,
      ReferenceCertificateID,
      ReferencePlatformName,
      [Unique]
  ) VALUES (
      'Ovlimaba_Aangebodenbrandprogramma_BKey',
      '021_0001',
      'Id',
      'Yes',
      '',
      '',
      '',
      '',
      'Yes'
  ), (
      'Ovlimaba_Aangebodenbrandprogramma_BKey',
      '021_0001',
      'BrandprogrammaId',
      'No',
      'Ovlimaba_Brandprogramma_BKey',
      '',
      '021_0006',
      'OVLIMABA_Brandprogramma',
      'No'
  );
  ```


  
-  



## Accelerator

# Open Questions
[ ] What script takes these four tables as input?
[ ] What is the function of the landing zone?
[ ] How does data go from operational to landing to raw to ods?
