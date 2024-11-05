# Setup

1. [Register a new Acoustid application](https://acoustid.org/my-applications).
2. Install packages.
```
sudo dnf -y install *chromaprint*
pip install pyacoustid -U
```

# Usage

```
ACOUSTID_KEY=YOUR-API-KEY sort-music.py x y
```
