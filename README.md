# SimPy environment Examples
This repository contains my code examples to create various simulation environments
* What is SimPy?
  SimPy is a discrete event simulation framework that contains variety of classes that can <br>
  help you build simulation environments of real world systems and processes.
  https://simpy.readthedocs.io/en/latest/

## local env setup
```bash
conda create -n simpy_env python=3.10.12
conda activate simpy_env

make install_develop
```

## How to install dependencies

1. Add the package to `src/requirements.in`
2. Run `make _compile` to create new `src/requirements.txt` file
3. Run `make install_develop` to install new dependencies from `src/requirements.txt`


## Other project setup info
Please refer to my template repository [mlops_template_repo](https://github.com/thakur-ro/mlops_template_repo)
