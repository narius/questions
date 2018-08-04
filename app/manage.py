#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='migrare_questions', url='postgresql://postgres:880515@localhost:5432/question_dev', debug='False')
