@Echo off
pyuic5 -x dialog.ui -o dialog.py
echo CREATE: %file_name% -- %python%