# `savvihub-python-sdk`

## Basic usage

```python
import savvihub

savvihub.init(organization_name="my-organization")
savvihub.create_experiment(...)
```

## Integrations

### Keras

- Use ExperimentCallback

```python
import savvihub
from savvihub.integration.keras import ExperimentCallback

savvihub.init()

# Keras training code
model = Model()
model.compile(...)

# Add integration
model.fit(x, y, epochs=5, callbacks=[ExperimentCallback()])
```

- Run experiment on Savvihub using Web UI or SDK
