# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['py']
install_requires = \
['boto3>=1.18.43,<2.0.0']

entry_points = \
{'console_scripts': ['aws-dynamodb-parallel-scan = '
                     'aws_dynamodb_parallel_scan:cli']}

setup_kwargs = {
    'name': 'aws-dynamodb-parallel-scan',
    'version': '0.2.0',
    'description': 'Amazon DynamoDB Parallel Scan Paginator for boto3.',
    'long_description': '# aws-dynamodb-parallel-scan\n\nAmazon DynamoDB parallel scan paginator for boto3.\n\n## Installation\n\nInstall from PyPI with pip\n\n```\npip install aws-dynamodb-parallel-scan\n```\n\nor with the package manager of choice.\n\n## Usage\n\nThe library is a drop-in replacement for [boto3 DynamoDB Scan Paginator](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Paginator.Scan). Example:\n\n```python\nimport aws_dynamodb_parallel_scan\nimport boto3\n\n# Create DynamoDB client to use for scan operations\nclient = boto3.resource("dynamodb").meta.client\n\n# Create the parallel scan paginator with the client\npaginator = aws_dynamodb_parallel_scan.get_paginator(client)\n\n# Scan "mytable" in five segments. Each segment is scanned in parallel.\nfor page in paginator.paginate(TableName="mytable", TotalSegments=5):\n    items = page.get("Items", [])\n```\n\nNotes:\n\n* `paginate()` accepts the same arguments as boto3 `DynamoDB.Client.scan()` method. Arguments\n  are passed to `DynamoDB.Client.scan()` as-is.\n\n* `paginate()` uses the value of `TotalSegments` argument as parallelism level. Each segment\n  is scanned in parallel in a separate thread.\n\n* `paginate()` yields DynamoDB Scan API responses in the same format as boto3\n  `DynamoDB.Client.scan()` method.\n\nSee boto3 [DynamoDB.Client.scan() documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan)\nfor details on supported arguments and the response format.\n\n## CLI\n\nThis package also provides a CLI tool (`aws-dynamodb-parallel-scan`) to scan a DynamoDB table\nwith parallel scan. The tool supports all non-deprecated arguments of DynamoDB Scan API. Execute\n`aws-dynamodb-parallel-scan -h` for details\n\nHere\'s some examples:\n\n```bash\n# Scan "mytable" sequentially\n$ aws-dynamodb-parallel-scan --table-name mytable\n{"Items": [...], "Count": 10256, "ScannedCount": 10256, "ResponseMetadata": {}}\n{"Items": [...], "Count": 12, "ScannedCount": 12, "ResponseMetadata": {}}\n\n# Scan "mytable" in parallel (5 parallel segments)\n$ aws-dynamodb-parallel-scan --table-name mytable --total-segments 5\n{"Items": [...], "Count":32, "ScannedCount":32, "ResponseMetadata": {}}\n{"Items": [...], "Count":47, "ScannedCount":47, "ResponseMetadata": {}}\n{"Items": [...], "Count":52, "ScannedCount":52, "ResponseMetadata": {}}\n{"Items": [...], "Count":34, "ScannedCount":34, "ResponseMetadata": {}}\n{"Items": [...], "Count":40, "ScannedCount":40, "ResponseMetadata": {}}\n\n# Scan "mytable" in parallel and return items, not Scan API responses (--output-items flag)\n$\xa0aws-dynamodb-parallel-scan --table-name mytable --total-segments 5 \\\n    --output-items\n{"pk": {"S": "item1"}, "quantity": {"N": "99"}}\n{"pk": {"S": "item24"}, "quantity": {"N": "25"}}\n...\n\n# Scan "mytable" in parallel, return items with native types, not DynamoDB types (--use-document-client flag)\n$\xa0aws-dynamodb-parallel-scan --table-name mytable --total-segments 5 \\\n    --output-items --use-document-client\n{"pk": "item1", "quantity": 99}\n{"pk": "item24", "quantity": 25}\n...\n\n# Scan "mytable" with a filter expression, return items\n$ aws-dynamodb-parallel-scan --table-name mytable --total-segments 5 \\\n    --filter-expression "quantity < :value" \\\n    --expression-attribute-values \'{":value": {"N": "5"}}\' \\\n    --output-items\n{"pk": {"S": "item142"}, "quantity": {"N": "4"}}\n{"pk": {"S": "item874"}, "quantity": {"N": "1"}}\n\n# Scan "mytable" with a filter expression using native types, return items\n$ aws-dynamodb-parallel-scan --table-name mytable --total-segments 5 \\\n    --filter-expression "quantity < :value" \\\n    --expression-attribute-values \'{":value": 5}\' \\\n    --use-document-client --output-items\n{"pk": "item142", "quantity": 4}\n{"pk": "item874", "quantity": 1}\n```\n\n## Development\n\nRequires Python 3 and Poetry. Useful commands:\n\n```bash\n# Run tests\npoetry run tox -e test\n\n# Run linters\npoetry run tox -e lint\n\n# Format code\npoetry run tox -e format\n```\n\n## License\n\nMIT\n\n## Credits\n\n* Alex Chan, [Getting every item from a DynamoDB table with Python](https://alexwlchan.net/2020/05/getting-every-item-from-a-dynamodb-table-with-python/)\n',
    'author': 'Sami Jaktholm',
    'author_email': 'sjakthol@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sjakthol/python-aws-dynamodb-parallel-scan',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
