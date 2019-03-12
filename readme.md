# Python libraries for usaepay.com credit card gateway #

Python library for https://usaepay.info/ payment card processing.

Written by reverse engineering PHP code from official SDK: https://help.usaepay.info/developer/sdks/php/

## Example use

```python
from usaepay import usaepay
tran = usaepay.UmTransaction()
tran.key = "YOUR_API_KEY"
tran.card = "4111111111111111"
tran.exp = "0120"
tran.amount = "5.00"
tran.invoice = "123456789"
tran.command = "cc:sale"
res = tran.process()
```

## Testing

When using sandbox, set:

```python
tran.usesandbox = True
```

## Limitations

Only `cc:sale` command is implemented at the moment.

## License

BSD license. See `LICENSE` for details.

## Develop

### tests

You will need to your API key to run those tests which actually send requests to gateway. Use sandbox for tests.

All tests:
```bash
python -m unittest discover
```
