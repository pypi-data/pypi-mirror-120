# bpptkg-querybulletin

Simple Python library to query seismic bulletin database.

## Installation

Install the latest version from PyPI:

    pip install -U bpptkg-querybulletin

Install database vendor dependent client package, e.g. for MySQL:

    pip install mysqlclient

## Database Credentials

Create JSON file in `~/.bulletin/querybulletin/config.json` to store your
seismic bulletin database credentials. For example:

```json
{
  "dburl": "mysql://user:password@localhost/seismic_bulletin"
}
```

If you have custom config file path, add `-c` or `--config` option to the full
path of JSON config file in the script arguments.

## Examples

Query bulletin for certain time range:

    querybulletin -s "2021-08-01 06:00:00" -e "2021-08-10 06:00:00"

Query bulletin for certain time range and event type:

    querybulletin -s "2021-08-01 06:00:00" -e "2021-08-10 06:00:00" -t VTB

Query bulletin for certain event ID:

    querybulletin -u "2021-07#2355"

Store output to the CSV file:

    querybulletin -s "2021-08-01 06:00:00" -e "2021-08-10 06:00:00" -t VTB -o bulletin.csv

## License

[MIT](https://github.com/bpptkg/bpptkg-querybulletin/blob/main/LICENSE)
