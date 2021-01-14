<img src="./logo.png" align="left" width="128" height="128" alt="Server Manager Logo"/>

# Server Manager
[![Version](https://img.shields.io/github/tag-pre/Macro303/Server-Manager.svg?label=version&style=flat-square)](https://github.com/Macro303/Server-Manager/releases)
[![Issues](https://img.shields.io/github/issues/Macro303/Server-Manager.svg?style=flat-square)](https://github.com/Macro303/Server-Manager/issues)
[![Contributors](https://img.shields.io/github/contributors/Macro303/Server-Manager.svg?style=flat-square)](https://github.com/Macro303/Server-Manager/graphs/contributors)
[![License](https://img.shields.io/github/license/Macro303/Server-Manager.svg?style=flat-square)](https://opensource.org/licenses/MIT)

A custom built role bot for **<u>The Playground</u> Discord Server**  
*See <u>Socials</u> section below for links*

## Commands
| Name | Restricted | Command | Description |
| ------- | ---------- | ------- | ----------- |
| List roles | False | `>Role` | Lists all the possible roles a user can give themselves |
| Give/Take role/s | False | `>Role [RoleName]` | Adds/Removes the role to the message sender, roles with spaces require to be surrounded by "quotes". Can be given multiple roles. |
| List blacklisted roles | True | `>Blacklist` | Lists all the roles a user can't give themselves |
| Add/Remove role to blacklist | True | `>Blacklist [RoleName]` | Adds/Removes the role to the role blacklist, roles with spaces require to be surrounded by "quotes". Can be given multiple roles. |

## Built Using
 - [Python: 3.9.1](https://www.python.org/)
 - [pip: 20.3.3](https://pypi.org/project/pip/)
 - [discord.py: 1.6.0](https://pypi.org/project/discord.py/)
 - [PyYAML: 5.3.1](https://pypi.org/project/PyYAML/)

## Execution
1. Execute the following to generate the default files:
   ```bash
   $ pip install -r requirements.txt
   $ python -m Bot
   ```
2. Update the generated `config.yaml` with your Discord Token and preferred Prefix
3. Run the following:
   ```bash
   $ python -m Bot
   ```

## Socials
[![Discord | The Bot Playground](https://discord.com/api/v6/guilds/797975024907976705/widget.png?style=banner2)](https://discord.gg/wsbSUYqDRP)
[![Discord | The Playground](https://discord.com/api/v6/guilds/618581423070117932/widget.png?style=banner2)](https://discord.gg/nqGMeGg)