# ibmrcms




IBM RCMS & Retain System Terminal Tools for Macos

---------------
FUNCTION I. CR
---------------
1. Call Read
    Usage:  cr,<Call No.>
2. Call Read every 30 seconds waiting for parts PO
    Usage:  cr,<Call No.>,w

---------------
FUNCTION II. CS
---------------
1. Call Search for current login user
    Usage: cs
2. Call Search for user specified
    Usage: cs,<Notes ID>
3. Type of Call Search for user specified
    Usage: cs,<Notes ID>,CRR|INS|MES|PMA
4. IPS Call Search for user specified
    Usage: cs,SDLINC,<Notes ID>

----------------
FUNCTION III. CI
----------------
Call Inventory
    Usage: ci,<Cust No.>,<Machine SN>,<Machine Type>
    All 3 args or few of them.

---------------
FUNCTION IV. IN
---------------
Product Inventory
    Usage: in,<Machine Type>,<Machine SN>,<Cust No.>
    All 3 args or fre of them.

---------------
FUNCTION V. RED
---------------
1. Red Time Reporting List for Current User
    Usage: red
2. Summary for Current User of this Cutoff
    Usage: red,s
3. Backup Time Reporting Records to Excel File
    Usage: red,b
4. Red or Summary or Backup for Other Users
    Usage: red,AVR71D | red,AVR71D,s | red,AVR71d,b


----------------
FUNCTION VI. PMH
----------------
1. Read Open Problem for Current User
    Usage: z
2. Read Problem
    Usage: z,49123,000,672
3. Search Cust No.
    Usage: z,805543 | z,0805543 | z,00805543
4. Search Cust Name
    Usage: z,Gansu ICBC
5. Search Retain User
    Usage: z,Zhang Zhi Jie,open

    All These Args or Few of Them.
-------------------------------
1. Display User Profile
    Usage: dr,149715
    <Only Support Retain ID>

-------------------------------
1. Create Problem
    Usage: ce,<Machine Type>,<Machine SN>
2. Create Problem with RCMS Call No. Specified
    Usage: ce,call,P462YK9
    <Not supported yet.>

-----------------
NECESSARY PACKAGE
-----------------
1. python3 for MacOS or Windows
# Download from website and double click install

2. s3270 for MacOS/Linux or ws3270 for Windows
# Download from website, compile & install.
# Or install via homebrew

3. openpyxl for python3
# pip3 install openpyxl

Start Program:
# python3 rcmsMenu.py


