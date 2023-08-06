# BasketCase
Fetch resources from Instagram.

It can download images and videos in their highest quality from any type of publication. You need a session cookie to avoid rate limits and access controls.

## Installation and usage
1. Install it from [PyPI](https://pypi.org/project/basketcase/). The `--user` flag means it will be installed in your home directory.

```sh
pip install --user basketcase
```

> This will put the executable `basketcase` on your PATH.

2. Create a text file (e.g. `basketcase.txt`) and populate it with resource URLs:

```
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
```

3. Pipe the contents of the file to the script, passing the session cookie as its first argument.

```sh
cat urls.txt | basketcase <session_cookie_id>
```

> Downloaded resources will be stored in the current working directory (i.e. `$PWD/basketcase/`).

## Development setup
1. `cd` to the project root and create a virtual environment in a directory named `venv`, which is conveniently ignored in version control.
2. Install the dependencies.

```sh
pip install -r requirements.txt
```

2. Install this package in editable mode.

```sh
pip install -e .
```

