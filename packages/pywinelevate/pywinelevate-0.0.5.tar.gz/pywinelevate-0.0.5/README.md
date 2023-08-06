# pywinelevate
a symple decorator that elevates a function rerunning the script as Admin if is not (in windows)

```from import pywinelevate import elevate

@elevate
def function_to_elevate(args*, argv**):
    foo = bar
    return foo
```

it will run ALL THE SCRIPT not only the function. be aware...