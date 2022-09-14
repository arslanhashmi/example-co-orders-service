# Order Service ![ci](https://github.com/arslanhashmi/example-co-orders-service/actions/workflows/ci.yaml/badge.svg)

## Getting started
Setup your development environment:
```bash
# start db container, setup env, install requirements, apply migrations and start the serverless process
$ make up

# run tests
$ make test
```

### Install the git hook scripts
run pre-commit install to set up the git hook scripts which lets you prettify your
code and fix flake8 violations(if any) before you could commit your code.

```bash
$ pip3 install pre-commit  # https://github.com/pre-commit/pre-commit
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

Now, pre-commit will run automatically on git commit!
