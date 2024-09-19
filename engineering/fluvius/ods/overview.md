# How to get data on the ODS layer
1. Create a data contract ([Template](https://mononline.sharepoint.com/:x:/r/sites/PRJ00120/Gedeelde%20documenten/Product/36.%20Intake%20Databron/_TEMPLATE_Databon_Contract.xlsx?d=w11ffe273009c476b82716fdb347671b1&csf=1&web=1&e=1Zf5hh))
2. Create connection with source system
3. Create delivery kit
4. Test delivery kit
5. Push changes to DataMgmt repo

# 1. Creating the datacontract
To know what data to onboard and how to onboard it (e.g. incremental, sensitive fields, ...) a data contract needs to be set up together with business
Please refer to the dedicated [Data Contract](../datacontract.md) page

# 2. Creating the connection with source system
This is something set-up by the platform team.
This is what we call the so called "highway" at Fluvius

# 3. Createing the delivery kit
**Speciciations**
- Server: `sql-datamgt-we-p-001.database.windows.net`
- Database: `sqldb-datamgt-we-p-004`

**How**
Connect using [SQL Server Management Studio](https://learn.microsoft.com/en-us/sql/ssms/sql-server-management-studio-ssms?view=sql-server-ver16)
