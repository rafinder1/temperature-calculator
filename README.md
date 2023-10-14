### Temperature Calculator

Aby uruchomić testy, wykonaj komendę:
```shell
 python -m pytest -v --log-cli-level=INFO --log-cli-format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s" 
```

Zainstaluj pakiet za pomocą `pip`:
```shell
pip install -r requirements.txt
```

Użyj pakietu w swoim kodzie:

```python
from calculator.basic.calculator import TempCalculator

TempCalculator.calculate()
```
