# Dr.Sploitberg
![Tests](https://github.com/TeamSploitberg/Dr.Sploitberg/actions/workflows/run-tests.yml/badge.svg)
![PyPi Test Upload](https://github.com/TeamSploitberg/Dr.Sploitberg/actions/workflows/publish-pypi.yml/badge.svg?event=release)
![PyPi Upload](https://github.com/TeamSploitberg/Dr.Sploitberg/actions/workflows/publish-test-pypi.yml/badge.svg?event=push,pull_request)

Dr.Sploitberg is a library of tools to aide with ethical hacking.

## Installation

Install using [pip](https://pip.pypa.io/en/stable/getting-started/ "pip"):
```bash
pip install DrSploitberg
```

Or you can install using the wheel file located here:
```bash
pip install dir/to/wheel/file.whl
```

## Example

```python
import DrSploitberg

dos = DrSploitberg.attack.DoS(targetIP='127.0.0.1', targetPort=80, threadNum=25)
dos.start()
try:
    while True:
	print(dos.getInfo())
except KeyboardInterrupt:
    dos.stop()
```

## Contributing
Please refer to [CONTRIBUTING.md](https://github.com/TeamSploitberg/Dr.Sploitberg/blob/master/CONTRIBUTING.md "CONTRIBUTING.md").

## Contact
You can contact us through our [discord server](https://discord.gg/kGYe3ZYCgf "discord server") or via our email: [TeamSploitberg@outlook.com](mailto:TeamSploitberg@outlook.com "TeamSploitberg@outlook.com").

## License
[MIT](https://choosealicense.com/licenses/mit/)
