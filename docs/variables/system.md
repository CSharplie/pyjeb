# System variables

| Name           | Sample         | Description |
|----------------|:--------------:|-------------|
| $sys.timestamp | 20231218101000 | Return the current timestamp with format YYYYMMDDhhmmss
| $sys.date      | 20231218       | Return the current date with format YYYYMMDD

# System functions

| Name                        |  Sample  | Parameters | Description |
|-----------------------------|:--------:|------------|------------:|
| $sys.timestamp('\<format>') | 20231218 | Format     | Return the current timestamp with format provided. See below allowed formats


# Date format
| PyJeb Format | Python format | Description            |
|--------------|:-------------:|------------------------|
| YYYY         |       %Y      | Year (exemple: 2023)   |
| MM           |       %m      | Month (Exemple: 08)    |
| DD           |       %d      | Day (Exemple: 01)      |
| hh           |       %H      | Hours (Exemple: 03)    |
| mm           |       %M      | Minutes (Exemple: 09)  |
| ss           |       %S      | Secondes (Exemple: 00) |