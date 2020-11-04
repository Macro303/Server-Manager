<img src="./logo.png" align="left" width="128" height="128" alt="Server Manager Logo"/>

# Server Manager
[![Version](https://img.shields.io/github/tag-pre/Macro303/Server-Manager.svg?label=version&style=flat-square)](https://github.com/Macro303/Server-Manager/releases)
[![Issues](https://img.shields.io/github/issues/Macro303/Server-Manager.svg?style=flat-square)](https://github.com/Macro303/Server-Manager/issues)
[![Contributors](https://img.shields.io/github/contributors/Macro303/Server-Manager.svg?style=flat-square)](https://github.com/Macro303/Server-Manager/graphs/contributors)
[![License](https://img.shields.io/github/license/Macro303/Server-Manager.svg?style=flat-square)](https://opensource.org/licenses/MIT)

_TODO_

## Commands

| Command | Restricted | Description | Example |
| ------- | ---------- | ----------- | ------- |
| `>Role` | True | Lists all the possible roles a user can give themselves |
| `>Role [<RoleName>]` | False | Adds/Removes the role to the message sender, roles with spaces require to be surrounded by "quotes". Can be given multiple roles. |
| `>Blacklist` | True | Lists all the roles a user can't give themselves |
| `>Blacklist [<RoleName>]` | True | Adds/Removes the role to the role blacklist, roles with spaces require to be surrounded by "quotes". Can be given multiple roles. |

## Built Using
 - [Python: 3.8.5](https://www.python.org/)
 - [pip: 20.2.4](https://pypi.org/project/pip/)
 - [discord.py: 1.5.1](https://pypi.org/project/discord.py/)
 - [PyYAML: 5.3.1](https://pypi.org/project/PyYAML/)

## Execution
1. Run the following:
   ```bash
   $ pip install -r requirements.txt
   $ python -m Bot
   ```
2. Update the generated `config.yaml` with your Token and preferred Prefix
3. Run the following:
   ```bash
   $ python -m Bot
   ```

## Socials
[![Discord | The Playground](https://discord.com/api/v6/guilds/618581423070117932/widget.png?style=banner2)](https://discord.gg/nqGMeGg)