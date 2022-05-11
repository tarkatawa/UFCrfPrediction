# UFCPred RF API

Flask application to run my UFC Pred Machine Learning Model.

## Usage

- Clone this repository.

```bash
git clone https://github.com/tarkatawa/UFCrfPrediction.git
```

- Create virtual environment.

```bash
cd UFCrfPrediction/venv/Scripts
activate
```

- Install dependencies.

```bash
cd ../..
pip install -r requirements.txt

# or install essential dependencies
pip install sklearn, pandas, numpy, openpyxl, flask
```

- Run app.

```bash
flask run
```

- Open `localhost:5000`.

- You can do `black .` and `isort .` to beautify your code.

## TODO List

- Write validations in application level.
- Deploy to the Internet.
