# Anaconda

## 🐍 **Conda Environment: Setup & Usage Guide**

### 🔹 1. Open the Conda Shell

* If you're on Windows and installed Anaconda:

  * Use the **Anaconda Prompt** or type `cmd` and activate the base environment like this:

    ```bash
    conda activate
    ```

### 🔹 2. Create a New Conda Environment

```bash
conda create -n myenv python=3.11
```

* Replace `myenv` with your desired environment name (e.g., project name).
* Replace `3.11` with the Python version you want.

### 🔹 3. Activate the Environment

```bash
conda activate myenv
```

* Now you're working **inside** your environment.

### 🔹 4. Install Packages

```bash
pip install jupyterlab
```

* Or use `conda install` if available:

```bash
conda install jupyterlab
```

### 🔹 5. Deactivate the Environment

```bash
conda deactivate
```

### 🔹 6. List All Conda Environments

```bash
conda env list
```

### 🔹 7. Delete a Conda Environment (optional)

```bash
conda remove -n myenv --all
```

---

### ✅ Tip:

* You can export the environment to a file for later use:

```bash
conda env export > environment.yml
```

* And recreate it with:

```bash
conda env create -f environment.yml
```

---


