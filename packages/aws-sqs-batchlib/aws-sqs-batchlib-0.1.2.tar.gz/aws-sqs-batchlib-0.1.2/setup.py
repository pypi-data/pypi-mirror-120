# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_sqs_batchlib', 'py']
install_requires = \
['botocore<2']

setup_kwargs = {
    'name': 'aws-sqs-batchlib',
    'version': '0.1.2',
    'description': 'Library working with Amazon SQS',
    'long_description': '# aws-sqs-batchlib for Python\n\nConsume and process Amazon SQS queues in large batches.\n\n## Features\n\n* Customizable batch size and batch window to consume and process messages\n  in larger (> 10 message) batches. Collect up-to 10,000 messages from a queue\n  and process them in one go.\n\n## Installation\n\nInstall from PyPI with pip\n\n```\npip install aws-sqs-batchlib\n```\n\nor with the package manager of choice.\n\n## Usage\n\n```python\nimport aws_sqs_batchlib\n\n# Consume up-to 100 messages from the given queue, polling the queue for\n# up-to 1 second to fill the batch.\nres = aws_sqs_batchlib.consume(\n    queue_url = "https://sqs.eu-north-1.amazonaws.com/123456789012/MyQueue",\n    batch_size=100,\n    maximum_batching_window_in_seconds=1,\n    VisibilityTimeout=300,\n)\n\n# Returns messages in the same format as boto3 / botocore SQS Client\n# receive_message() method.\nassert res == {\n    \'Messages\': [\n        {\'MessageId\': \'[.]\', \'ReceiptHandle\': \'AQ[.]JA==\', \'MD5OfBody\': \'[.]\', \'Body\': \'[.]\'},\n        {\'MessageId\': \'[.]\', \'ReceiptHandle\': \'AQ[.]wA==\', \'MD5OfBody\': \'[.]\', \'Body\': \'[.]\'}\n        # ... up-to 1000 messages\n    ]\n}\n```\n\n## Development\n\nRequires Python 3 and Poetry. Useful commands:\n\n```bash\n# Run tests\npoetry run tox -e test\n\n# Run linters\npoetry run tox -e lint\n\n# Format code\npoetry run tox -e format\n```\n\n## Benchmarks & Manual Testing\n\nUse `benchmark/benchmark.py` to benchmark and test the library functionality and performance. Execute following commands in Poetry virtualenv (execute `poetry shell` to get there):\n\n```bash\n# Setup\nexport PYTHONPATH=$(pwd)\nexport AWS_DEFAULT_REGION=eu-north-1\n\n# Send messages to a queue\npython3 benchmark/benchmark.py \\\n  --queue-url https://sqs.eu-north-1.amazonaws.com/123456789012/MyQueue producer\n\n# Consume messages with the plain SQS ReceiveMessage polling\npython3 benchmark/benchmark.py \\\n  --queue-url https://sqs.eu-north-1.amazonaws.com/123456789012/MyQueue consumer-plain\n\n# Consume messages with the libary\npython3 benchmark/benchmark.py \\\n  --queue-url https://sqs.eu-north-1.amazonaws.com/123456789012/MyQueue consumer-lib \\\n  --batch-size 1000\n  --batch-window 1\n```\n\nSingle thread is able to receive / send around 400 messages per second to an SQS queue on the same AWS region (eu-north-1, m5.large instance).\n\n## License\n\nMIT.',
    'author': 'Sami Jaktholm',
    'author_email': 'sjakthol@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
