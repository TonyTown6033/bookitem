# Node.js 安装指南

当前项目需要 **Node.js 18+** 才能运行。

## 错误信息

如果你看到以下错误：
```
SyntaxError: Unexpected reserved word
    at Loader.moduleStrategy (internal/modules/esm/translators.js:133:18)
```

这表明你的 Node.js 版本太低了。

## 解决方案

### 方案 1：使用 nvm（推荐）

nvm 可以让你轻松管理多个 Node.js 版本。

#### 1. 安装 nvm

```bash
# Linux/macOS
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 或者使用 wget
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

#### 2. 重新加载配置

```bash
# 如果使用 bash
source ~/.bashrc

# 如果使用 zsh
source ~/.zshrc
```

#### 3. 安装 Node.js 18

```bash
nvm install 18
nvm use 18
nvm alias default 18
```

#### 4. 验证安装

```bash
node --version  # 应该显示 v18.x.x
npm --version   # 应该显示 9.x.x 或更高
```

#### 5. 运行项目

```bash
cd ~/web/bookitem
./start.sh
```

### 方案 2：从官网安装

访问 [Node.js 官网](https://nodejs.org/) 下载并安装 Node.js 18 LTS 版本。

### 方案 3：使用包管理器

#### Ubuntu/Debian
```bash
# 添加 NodeSource 仓库
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# 安装 Node.js
sudo apt-get install -y nodejs
```

#### CentOS/RHEL
```bash
# 添加 NodeSource 仓库
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -

# 安装 Node.js
sudo yum install -y nodejs
```

#### macOS (Homebrew)
```bash
brew install node@18
brew link node@18
```

## 项目 Node.js 版本要求

- **最低版本**: Node.js 18.0.0
- **推荐版本**: Node.js 18.20.0 LTS
- **原因**: Vite 5.x 需要 Node.js 18+ 才能运行（top-level await 支持）

## 快速切换 Node.js 版本（使用 nvm）

项目根目录和 `frontend/` 目录下有 `.nvmrc` 文件，运行以下命令即可自动切换到正确版本：

```bash
cd ~/web/bookitem
nvm use
```

这会自动读取 `.nvmrc` 文件并切换到 Node.js 18.20.0。

## 验证环境

运行以下命令验证你的环境：

```bash
cd ~/web/bookitem
node --version    # 应该 >= v18.0.0
npm --version     # 应该 >= 9.0.0
./start.sh        # 应该能正常启动
```

## 常见问题

### Q: 我的系统上已经有其他项目使用 Node.js 12，会冲突吗？

A: 不会。使用 nvm 可以在不同项目之间轻松切换 Node.js 版本。每个终端窗口可以使用不同的版本。

### Q: nvm use 后，新开终端又变回旧版本了？

A: 设置默认版本：
```bash
nvm alias default 18
```

或者在项目目录下自动切换（推荐），在 `~/.bashrc` 或 `~/.zshrc` 中添加：
```bash
# 自动加载 .nvmrc
autoload -U add-zsh-hook
load-nvmrc() {
  local node_version="$(nvm version)"
  local nvmrc_path="$(nvm_find_nvmrc)"

  if [ -n "$nvmrc_path" ]; then
    local nvmrc_node_version=$(nvm version "$(cat "${nvmrc_path}")")

    if [ "$nvmrc_node_version" = "N/A" ]; then
      nvm install
    elif [ "$nvmrc_node_version" != "$node_version" ]; then
      nvm use
    fi
  elif [ "$node_version" != "$(nvm version default)" ]; then
    echo "Reverting to nvm default version"
    nvm use default
  fi
}
add-zsh-hook chpwd load-nvmrc
load-nvmrc
```

### Q: 安装后还是报错？

A: 尝试以下步骤：
```bash
cd ~/web/bookitem/frontend
rm -rf node_modules package-lock.json
npm install
cd ..
./start.sh
```

## 需要帮助？

如果遇到问题，请提供以下信息：
- 操作系统版本
- 当前 Node.js 版本（`node --version`）
- 完整的错误信息

