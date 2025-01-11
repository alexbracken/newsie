# Getting Started
These instructions are primarily for those using MacOS. I'm on Sequoia (15.2), and these instructions are based on that system.



# Prerequisities
Don't skip this part.
### Python
You may already have this installed, especially if you're using Windows. Open a PowerShell or Terminal window, and use the following command to check.
```bash
python -v
```
If that doesn't work, trying using `python3 -v` to check your installation.
#### Install Python (Mac)
1. Open a Terminal window.
2. Check if Python is already installed by typing:
   ```bash
   python3 --version
   ```
   If Python is installed, you will see the version number.

3. If Python is not installed, you can install it using a package manager.

   **For Mac:**
   - Install Homebrew if you haven't already by running:
     ```
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Install Python using Homebrew:
     ```
     brew install python
     ```

4. Verify the installation by typing:
   ```bash
   python3 --version
   ```
   You should see the version of Python you installed.

#### Installing Python (Windows)
1. Go to the official Python website: [python.org](https://www.python.org/downloads/windows/)
2. Download the latest version of Python for Windows.
3. Run the installer and **make sure to check the box that says "Add Python to PATH".**
4. Follow the installation instructions.

Verify the installation by opening a PowerShell or Command Prompt window and typing:
   ```
   python --version
   ```
   You should see the version of Python you installed.

## Download script
### Method 1: Using git
If you already have git installed, clone the repository into a folder on your machine.

```
git clone https://github.com/alexbracken/newsie.git
```
The ``clone`` command will create a new directory in the location of the terminal, so you may need to use the ``cd`` command to 
### Method 2: Using Github website
Download the latest release from the [releases page](https://github.com/alexbracken/newsie/releases) of the repository, and unzip at the location.

