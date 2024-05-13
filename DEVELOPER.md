# Developer notes

## Using the VSCode debugger for debugging the simulation

1. Create a `launch.json` file with the following debugging config in your VSCode workspace. Example here shows how to debug the project module pipeline where the repository is nested within the `mlops_template_repo`

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Kedro debug",
            "type": "python",
            "request": "launch",
            "module": "kedro",
            "args": [
                "run",
                "-p",
                "${module_name}" add other kedro run args here
            ],
            "justMyCode": false,
            # Change this as needed
            "cwd": "${mlops_template_repo}/"
        }
    ]
}
```

2. Add breakpoints to examine the state of the simulation at different contexts in the code from the debug console
