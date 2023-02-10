# PrintMailAttachment
This script gets new E-Mails from the specified imap server , stores them in an attachment-folder and prints them, depending on filenames.


## Usage


### Clone the script:
```bash
git clone git@github.com:nordcomputer/printmailattachment.git
```

### Run the script
To run this script, you need to have a running cups service.
copy and rename the env-samplefile to .env und specify your variables.


#### Linux ####
```bash
python3 printmailattachments.py
```

#### Windows ####
```bash
python3 winprintmailattachments.py
```

### See a list of printers
If you want to see a list of your printers from cups, run:

#### Linux ####
```bash
python3 printers.py
```

#### Windows ####
```bash
python3 winprinters.py
```


You may need to install the correct modules via pip.
Be aware, that you need the pycups module and not the cups module.

### To uninstall the cups module via pip:

```bash
pip uninstall cups
```


### To install pycups:

```bash
pip install pycups
```


You can use the same method to install missing modules.
