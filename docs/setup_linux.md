# Linux Setup

## Prerequisites

Install Miniconda (backend package manager):
```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
conda init bash
```

Install Taskfile (task runner):
```bash
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
```

Install Node and pnpm (frontend package manager):
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install --lts
corepack enable pnpm
```


Then proceed as in `README.md`.