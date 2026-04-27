# Phosphor565 - 2026
FROM ubuntu:24.04

# Image felshing out and config - - - - - - - - - - - - - - - - - - - - -
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git git-lfs zsh sudo locales tzdata \
    build-essential make pkg-config \
    libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev \
    liblzma-dev \
    openssh-client wget unzip zip gnupg lsb-release \
    vim nano direnv \
    python3-pip gitpipx \cd
 && rm -rf /var/lib/apt/lists/*

# Set time and language
RUN locale-gen en_GB.UTF-8 && update-locale LANG=en_GB.UTF-8
ENV LANG=en_GB.UTF-8
ENV LC_ALL=en_GB.UTF-8

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Additional Development Specific Tools - - - - - - - - - - - - - - - - -

# Azure CLI - https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Azure Function App Local Dev - https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
RUN sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
RUN sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs 2>/dev/null)-prod $(lsb_release -cs 2>/dev/null) main" > /etc/apt/sources.list.d/dotnetdev.list'
RUN sudo apt-get update
RUN sudo apt-get install azure-functions-core-tools-4

# UV Python Package Manager - https://docs.astral.sh/uv/
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# Creature Comforts - - - - - - - - - - - - - - - - - - - - - - - - - - -

# OhMyZsh - https://ohmyz.sh/
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended \
 && git config --global init.defaultBranch main \
 && git config --global pull.rebase false \
 && git lfs install

# Ensure zsh is configured
RUN cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc \
 && sed -i 's/^ZSH_THEME=.*/ZSH_THEME="robbyrussell"/' ~/.zshrc \
 && sed -i 's/^plugins=.*/plugins=(git python pip pyenv docker docker-compose)/' ~/.zshrc \
 && printf '\n# pyenv\nexport PYENV_ROOT="$HOME/.pyenv"\nexport PATH="$PYENV_ROOT/bin:$PATH"\neval "$(pyenv init -)"\neval "$(pyenv virtualenv-init -)"\n' >> ~/.zshrc \
 && printf '\n# direnv\nexport EDITOR=vim\neval "$(direnv hook zsh)"\n' >> ~/.zshrc \
 && printf '\n# pipx\nexport PATH="$HOME/.local/bin:$PATH"\n' >> ~/.zshrc

 # create new user and ensure Image uses user and has working dir
RUN useradd -m -s /usr/bin/zsh developer \
 && echo "developer ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/99-developer \
 && chmod 0440 /etc/sudoers.d/99-developer

USER developer
RUN sudo mkdir -p /development
WORKDIR /development
ENV HOME=/home/developer
ENV SHELL=/usr/bin/zsh

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Keep the container running by running a terminal  - - - - - - - - - - -
CMD ["zsh"]