# Website Structure

## backend

- Flask

### apis

- `/api/dates`
- `/api/date/<date_str>`
- `/api/date/<date_str>/<csv_str>`
- `/api/symbols`
- `/api/symbol/<symbol_str>?download=...&overwrite=...`
    - `download`: 1 or else
    - `overwrite`: 1 or else
- `/api/get_file?file_name=...`

## frontend

- React
    - React Router
- Ant Design
- Highcharts

### routes

- `/`
- `/stock`
- `/stock/:date_str`
- `/stock/:date_str/:csv_str`
- `/download`
- `/download/:symbol_str`
