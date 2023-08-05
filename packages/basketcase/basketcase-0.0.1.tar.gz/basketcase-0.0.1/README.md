# BasketCase
Fetch resources from Instagram.

## Main dependencies
- requests
- youtube-dl
- Pillow

## Development setup
1. Create a virtual environment with `venv` and `cd` to the root directory of the project.
2. Ensure `pip` is up-to-date

```sh
pip install --upgrade pip
```
3. Install the dependencies.

```sh
pip install -r requirements.txt
```
4. Install the package in editable mode

```sh
pip install -e .
```

## Usage
Create a text file (e.g. `urls.txt`) and populate it with resource URLs:

```
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
```

Pipe the file to the script, passing the session cookie as its argument.

```sh
cat urls.txt | basketcase <session_cookie>
```

Downloaded resources will be stored in the current working directory (i.e. `$PWD/basketcase/`).

