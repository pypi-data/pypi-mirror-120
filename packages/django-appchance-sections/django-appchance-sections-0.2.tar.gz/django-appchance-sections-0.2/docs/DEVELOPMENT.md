How to develop?
===============

1. Go to `cd ./sample_project`

1. Run `./ctl.sh install` to create virtual environment and install all requirements.

1. From now you can:

    run all commands via ./ctl.sh script e.g. `./ctl.sh runserver`
    - for more details see `./ctl.sh --help`

    or

    you can activate virtual environment manualy `source ../.env/bin/activate`
    and call any commands directly e.g. `python manage.py runserver`

1. Translations:

    run `./ctl.sh makemessages -l pl`
    Note: It is equivalent of `../ && django-admin makemessages -l pl && cd ./sample_project`

1. Generating distribution archives `./ctl.sh build`

1. Uploading the distribution archives `./ctl.sh upload_test`