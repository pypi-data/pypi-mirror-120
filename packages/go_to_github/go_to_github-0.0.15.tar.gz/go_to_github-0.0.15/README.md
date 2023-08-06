`go_to_github` is a tool to test whether `github.com` is reachable right now. If not, it will work it out automatically.

# Notice
It might be in need for people who come from countries blocking github.
This project only applies to `macOS` and `Linux`.

# Usage
```python
sudo gotogithub

```
Don't forget `sudo`. Github ip will be updated if the program detects that you cannot connect to github.com. The update happens in your `/private/etc/hosts` file, which requires root user. 

Meanwhile, before any modification, your original hosts file will be copied to `~/.local/share/gotogithub/hosts`. If the program fails to connect to github in the end, it will restore the backup hosts file automatically to `/private/etc/hosts`.

# Installation
```python
pip install go_to_github
```


