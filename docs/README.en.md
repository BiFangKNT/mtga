# MTGA

<picture>
    <img alt="MTGA" src="https://github.com/BiFangKNT/mtga/blob/gui/icons/hero-img_f0bb32.png?raw=true">
</picture>

[![English](https://img.shields.io/badge/docs-English-purple)](README.en.md) [![简体中文](https://img.shields.io/badge/文档-简体中文-yellow)](../README.md) [![日本語](https://img.shields.io/badge/ドキュ-日本語-b7003a)](README.ja.md) [![한국어 문서](https://img.shields.io/badge/docs-한국어-green)](README.ko.md) [![Documentación en Español](https://img.shields.io/badge/docs-Español-orange)](README.es.md) [![Documentation en Français](https://img.shields.io/badge/docs-Français-blue)](README.fr.md) [![Documentação em Português (Brasil)](https://img.shields.io/badge/docs-Português-purple)](README.pt.md) [![Dokumentation auf Deutsch](https://img.shields.io/badge/docs-Deutsch-darkgreen)](README.de.md) [![Документация на русском языке](https://img.shields.io/badge/доки-Русский-darkblue)](README.ru.md)

## Introduction

MTGA is a local proxy-based IDE fixed model provider solution for Windows and macOS.

**Note: This project currently only supports APIs in OpenAI format. Please confirm. Other formats can be converted to OpenAI format before use.**

<details>
  <summary>You can't see anything~~</summary>
  <br>
  <p>MTGA stands for Make Trae Great Again!</p>
 </details>

## Table of Contents

- [MTGA](#mtga)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Changelog](#changelog)
    - [v1.2.0 (Latest)](#v120-latest)
    - [v1.1.1](#v111)
    - [v1.1.0](#v110)
    - [v1.0.0](#v100)
  - [Quick Start](#quick-start)
    - [Windows Users (GUI One-Click Startup)](#windows-users-gui-one-click-startup)
    - [macOS Users (Application Installation)](#macos-users-application-installation)
      - [Installation Method](#installation-method)
      - [Usage Instructions](#usage-instructions)
  - [macOS Fix "The package is damaged" Issue](#macos-fix-the-package-is-damaged-issue)
    - [Graphical Solution](#graphical-solution)
    - [CLI Solution](#cli-solution)
  - [Troubleshooting 'Add Model Failed' Prompt on Trae Side](#troubleshooting-add-model-failed-prompt-on-trae-side)
  - [Starting from Script](#starting-from-script)
    - [Step 0: Environment Preparation](#step-0-environment-preparation)
      - [Windows](#windows)
        - [Step 1: Generate a Self-Signed Certificate](#step-1-generate-a-self-signed-certificate)
        - [Step 2: Make Windows Trust Your CA Certificate](#step-2-make-windows-trust-your-ca-certificate)
        - [Step 3: Modify the Hosts File](#step-3-modify-the-hosts-file)
        - [Step 4: Run the Local Proxy Server (Python)](#step-4-run-the-local-proxy-server-python)
        - [Step 5: Configure Trae IDE](#step-5-configure-trae-ide)
      - [macOS](#macos)
  - [😎 Stay Updated](#-stay-updated)
  - [References](#references)

---

## Changelog

### v1.2.0 (Latest)

- 🔄 **Refactored Model Mapping Architecture** - Changed from "One-to-One Mapping" to "Unified Mapping Model" architecture
  - Trae side uses a unified mapping model ID, MTGA switches the actual backend model through configuration groups
  - Proxy server supports model ID mapping and MTGA authentication verification
  - Global configuration supports mapping model ID and MTGA authentication key settings
- ⚡ **Configuration Group Management Optimization** - Refactored configuration group fields and validation logic
  - Configuration group name changed to optional, API URL, actual model ID, and API Key set as mandatory
  - Removed target model ID field, switching to global mapping configuration
  - Renamed configuration group table headers with backward compatibility for old config files
- 🧪 **Added Automated Testing Features** - Comprehensive model connectivity testing system
  - Automatically test model connectivity after saving configurations (GET `/v1/models/{model_id}`)
  - Manual liveness test feature, supports chat completion testing (POST `/v1/chat/completions`)
  - Detailed test logs output, including response content and token consumption statistics
- 🎯 **Enhanced User Experience** - Added liveness test button and detailed prompts
  - Liveness test button supports tooltip hints explaining token consumption risks
  - Asynchronous testing to avoid UI blocking with improved error handling mechanism
  - API Key security display (masked)

<details>
<summary>Changelog</summary>

### v1.1.1

- 🐛 **Fixed hosts modification issue** - Resolved abnormal line breaks when modifying hosts file

### v1.1.0

- ✨ **Added user data management functionality** - Single-file version supports persistent storage of user data
  - Data storage location: Windows `%APPDATA%\MTGA\`, macOS/Linux `~/.mtga/`
  - Supports backup, restore, and clear user data
  - Configuration files, SSL certificates, hosts backups are automatically persisted
- 🔧 **Optimized single-file build** - Improved `build_onefile.bat`, supports version number variable
- 🎯 **Improved user interface** - Added configuration group list refresh button, optimized interface layout
- 📖 **Enhanced documentation** - Added single-file build guide, updated project documentation

### v1.0.0

- ✅ **Adapted for Mac OS** - Supports macOS application installation
- 🔄 **Default provider changed** - Changed from DeepSeek to OpenAI
- 📦 **File restructuring** - Renamed ds-related files to `*_ds.*` format for archiving
- 🌐 **API URL format changed** - From `https://your-api.example.com/v1` to `https://your-api.example.com`

</details>

---

## Quick Start

### Windows Users (GUI One-Click Startup)

1. Download the latest version of `MTGA_GUI-v{version}-x64.exe` from [GitHub Releases](https://github.com/BiFangKNT/mtga/releases)
2. Double-click the downloaded exe file to run (requires administrator privileges)
3. In the opened graphical interface, fill in the API URL and Model ID
   - **API URL only needs the domain name (port number is optional, do not fill if unsure), no need to include the route, for example: `https://your-api.example.com`**
   - **If you wish to enable multimodal capabilities, you can map the model name to the built-in multimodal model name:**
   - <img width="247" height="76" alt="model mapping" src="../images/model-mapping.png?raw=true" />
   - <img width="380" height="141" alt="model mapping effects" src="../images/model-mapping-effects.png?raw=true" />
4. Click the "Start All Services with One Click" button
5. Wait for the program to automatically complete the following operations:
   - Generate and install the certificate
   - Modify the hosts file
   - Start the proxy server
6. After completion, proceed with IDE configuration according to [Step 5: Configure Trae IDE](#第-5-步配置-trae-ide)

> [!NOTE]
>
> - First run may require allowing firewall access permissions
> - The single-file version supports persistent storage of user data; configurations and certificates are automatically saved
> - If adding a model on the Trae side fails, please refer to [Troubleshooting 'Add Model Failed' Prompt on Trae Side](#troubleshooting-add-model-failed-prompt-on-trae-side)

### macOS Users (Application Installation)

#### Installation Method

1. Download the latest version of `MTGA_GUI-v{version}-aarch64.dmg` from [GitHub Releases](https://github.com/BiFangKNT/mtga/releases)
2. Double-click the DMG file, the system will automatically mount the installation package
3. Drag `MTGA_GUI.app` to the `Applications` folder
4. Launch the application from Launchpad or the Applications folder

#### Usage Instructions

1. Launch `MTGA_GUI.app` (first run may require allowing it to run in System Preferences)
2. Fill in the graphical interface:
   - **API URL**: Your API service address (e.g., `https://your-api.example.com`)
   - **If you wish to enable multimodal capabilities, you can map the model name to the built-in multimodal model name:**
   - <img width="247" height="76" alt="model mapping" src="../images/model-mapping.png?raw=true" />
   - <img width="380" height="141" alt="model mapping effects" src="../images/model-mapping-effects.png?raw=true" />
3. Click the "Start All Services with One Click" button
4. The program will automatically complete:
   - Generate and install the SSL certificate into the system keychain
   - Modify the `/etc/hosts` file (requires administrator privileges)
5. Manually trust the generated certificate in the opened keychain window; the default name is `MTGA_CA`
6. Start the local proxy server
7. Complete the setup by following the [Trae IDE Configuration](#第-5-步配置-trae-ide) below

> [!NOTE]
>
> - Certificate installation and hosts modification require administrator privileges
> - If prompted with "The package is damaged", please refer to [macOS Fix "The package is damaged" Issue](#macos-fix-the-package-is-damaged-issue)
> - If adding a model on the Trae side fails, please refer to [Troubleshooting 'Add Model Failed' Prompt on Trae Side](#troubleshooting-add-model-failed-prompt-on-trae-side)

## macOS Fix "The package is damaged" Issue

If you see a prompt like this when launching `MTGA_GUI.app`:

<img width="244" height="223" alt="app corrupted" src="../images/app-corrupted.png?raw=true" />

**Click Cancel**. Then follow the steps below to resolve the issue:

### Graphical Solution

1. Go to [Sentinel Releases](https://github.com/alienator88/Sentinel/releases/latest) and download `Sentinel.dmg`
2. Double-click the `Sentinel.dmg` file, then drag `Sentinel.app` to the `Applications` folder
3. Launch `Sentinel.app` from Launchpad or the Applications folder
4. Drag the `MTGA_GUI.app` from this project into the left window of `Sentinel.app`
   - <img width="355.33" height="373.33" alt="sentinel add app" src="../images/sentinel-add-app.png?raw=true" />

`MTGA_GUI.app` will be automatically processed and launched

### CLI Solution

1. Locate the full path of `MTGA_GUI.app`, e.g., `/Applications/MTGA_GUI.app`.
2. Open the Terminal application.
3. Run the following command to remove the signature quarantine from `MTGA_GUI.app`:
   ```zsh
   xattr -d com.apple.quarantine <full path of the app>
   ```
   This removes the `com.apple.quarantine` extended attribute from `MTGA_GUI.app`.
4. Launch `MTGA_GUI.app`.

## Troubleshooting 'Add Model Failed' Prompt on Trae Side

Please check:

- Whether the hosts file contains the line `127.0.0.1 api.openai.com`, and that it is not commented out (starting with #).
- Ensure no other programs are using port 443 (such as browsers, VPNs, etc.).
  - You can check using the following commands:

    ```
    # windows
    netstat -ano | find ":443" | find "LISTENING"

    # macos
    netstat -lnp tcp | grep :443
    ```

  - If there is a process listening on port 443, it is recommended to close that process.

---

## Starting from Script

### Step 0: Environment Preparation

#### Windows

- System requirements: Windows 10 or above
- Administrator privileges required
- Install Python environment, recommended Python 3.10 or above
- Install Git

##### Step 1: Generate a Self-Signed Certificate

Open Git Bash:

```bash
# Change to the ca directory
cd "mtga/ca"

# 1. Generate the CA certificate (ca.crt and ca.key)
./genca.sh
```

When executing `./genca.sh`, it will ask "Do you want to generate ca cert and key? [yes/no]". Enter `y` and press Enter. Afterwards, it will prompt for some information:

- `Country Name (2 letter code) []`: Enter `CN` (or another country code)
- Other fields (like State, Locality, Organization, Common Name for CA) can be filled as needed or left blank; it's suggested to fill them with `X`. The Common Name can be something like `MTGA_CA`. The email field can be left empty.

```bash
# 2. Generate the SSL certificate for api.openai.com (api.openai.com.crt and api.openai.com.key)
# This script uses the configuration files api.openai.com.subj and api.openai.com.cnf in the same directory
./gencrt.sh api.openai.com
```

After execution completes, you will find the following important files in the `mtga\ca` directory:

- `ca.crt` (Your custom CA certificate)
- `ca.key` (Your custom CA private key - **DO NOT LEAK**)
- `api.openai.com.crt` (SSL certificate for the local proxy server)
- `api.openai.com.key` (SSL private key for the local proxy server - **DO NOT LEAK**)

##### Step 2: Make Windows Trust Your CA Certificate

1.  Locate the `mtga\ca\ca.crt` file.
2.  Double-click the `ca.crt` file to open the certificate viewer.
3.  Click the "Install Certificate..." button.
4.  Choose "Current User" or "Local Machine". It is recommended to choose "Local Machine" (this requires administrator privileges) to apply it to all users.
5.  In the next dialog, select "Place all certificates in the following store", then click "Browse...".
6.  Select "Trusted Root Certification Authorities", then click "OK".
7.  Click "Next", then "Finish". If a security warning pops up, select "Yes".

##### Step 3: Modify the Hosts File

**⚠️WARNING: After performing this step, you will not be able to access the original OpenAI API. Web usage is unaffected.**

You need to modify the Hosts file with administrator privileges to point `api.openai.com` to your local machine.

1.  Hosts file path: `C:\Windows\System32\drivers\etc\hosts`
2.  Open this file with Notepad (or another text editor) as an administrator.
3.  Add the following line at the end of the file:
    ```
    127.0.0.1 api.openai.com
    ```
4.  Save the file.

##### Step 4: Run the Local Proxy Server (Python)

**Before running the proxy server:**

1.  **Install Dependencies**:
    ```bash
    pip install Flask requests
    ```
2.  **Configure the Script**:
    - Open the `trae_proxy.py` file.
    - **Modify `TARGET_API_BASE_URL`**: Replace it with the base URL of the actual OpenAI-format API site you want to connect to (e.g., `"https://your-api.example.com"`).
    - **Confirm Certificate Paths**: The script defaults to reading `api.openai.com.crt` and `api.openai.com.key` from `mtga\ca`. If your certificates are not in this path, modify the values of `CERT_FILE` and `KEY_FILE`, or copy these two files to the `CERT_DIR` specified by the script.

**Run the Proxy Server:**

Open Command Prompt (cmd) or PowerShell **Run as Administrator** (because it needs to listen on port 443), then execute:

```bash
python trae_proxy.py
```

If everything goes well, you should see the server startup logs.

##### Step 5: Configure Trae IDE

1.  Open and log in to Trae IDE.
2.  In the AI dialog box, click the model icon in the lower right corner and select "Add Model" at the end.
3.  **Provider**: Select `OpenAI`.
4.  **Model**: Select "Custom Model".
5.  **Model ID**: Enter the value you defined for `CUSTOM_MODEL_ID` in the Python script (e.g., `my-custom-local-model`).
6.  **API Key**:
    - If your target API requires an API key and Trae will pass it via `Authorization: Bearer <key>`, then the key entered here will be forwarded by the Python proxy.
    - When configuring OpenAI in Trae, the API key is related to the `remove_reasoning_content` configuration. Our Python proxy does not handle this logic; it simply forwards the Authorization header. You can try entering the key required by your target API, or an arbitrary key in the `sk-xxxx` format.

7.  Click "Add Model".
8.  Return to the AI chat box and select the custom model you just added from the lower right corner.

Now, when you interact with this custom model through Trae, the requests should go through your local Python proxy and be forwarded to your configured `TARGET_API_BASE_URL`.

**Troubleshooting Tips:**

- **Port Conflict**: If port 443 is already occupied (e.g., by IIS, Skype, or other services), the Python script will fail to start. You need to stop the service occupying that port, or modify the Python script and Nginx (if used) to listen on a different port (though this is more complex because Trae hardcodes access to `https://api.openai.com` on port 443).
- **Firewall**: Ensure the Windows firewall allows inbound connections for Python listening on port 443 (even though it's a local connection `127.0.0.1`, firewall configuration is usually not required, but it's worth checking).
- **Certificate Issues**: If Trae reports SSL/TLS related errors, carefully check if the CA certificate has been correctly installed into the "Trusted Root Certification Authorities" store, and if the Python proxy correctly loaded `api.openai.com.crt` and `.key`.
- **Proxy Logs**: The Python script will print some logs that can help you diagnose issues.

This solution is more integrated than the direct vproxy + nginx approach, placing both TLS termination and proxy logic within a single Python script, making it more suitable for rapid prototyping on Windows.

#### macOS

-> [Mac OS Script Startup Method](https://github.com/BiFangKNT/mtga/blob/gui/docs/README_macOS_cli.md)

---

## 😎 Stay Updated

Click the Star and Watch buttons at the top right of the repository to get the latest updates.

![star to keep latest](https://github.com/BiFangKNT/mtga/blob/gui/images/star-to-keep-latest.gif?raw=true)

---

## Documentation

- [Contribution Guidelines](../CONTRIBUTING.md)
- [Local Build Guide](BUILD.md)

---

## References

The `ca` directory is referenced from the `wkgcass/vproxy` repository. Thanks to the original author!
