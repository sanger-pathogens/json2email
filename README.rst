json2email
===========

Takes some json and a template and sends an email. Json can be provided
as a filename or via stdin. Templates are rendered using
`Jinja2 <http://jinja.pocoo.org/docs/dev/>`_. If the template renders
only whitespace, json2email does not send an email. This can be used to
implement logic within the template itself.

json2email accepts an argument for an email address which it will try
and inform if there are errors. Obviously this isn't possible for some
classes of error.

This is still pretty untested so please raise an issue if you spot any
bugs.

Usage
-----

::

    $ json2email -h
    usage: json2email [-h] [--plain PLAIN] [--subject SUBJECT]
                         [--to TO [TO ...]] [--from SENDER] [--server SERVER]
                         [--error [ERROR [ERROR ...]]] [--noop] [--json JSON]

    Takes a jinja2 template and some json and sends an email

    optional arguments:
      -h, --help            show this help message and exit
      --plain PLAIN, -p PLAIN
                            Template with plain text template for email
      --subject SUBJECT, -s SUBJECT
                            Subject line for email
      --to TO [TO ...], -t TO [TO ...]
                            To: recipient of email
      --from SENDER, -f SENDER
                            From: sender of email
      --server SERVER       SMTP server
      --error [ERROR [ERROR ...]], -e [ERROR [ERROR ...]]
                            Email address to send errors to (if any)
      --noop, -n            Noop: if set, prints email to stdout instead of
                            sending
      --json JSON, -j JSON  Json formated data file (use '-' for stdin)

Example
-------

Our team manages a pipeline to which users can add jobs. Some of these
jobs need to be approved by an admin before they run. We output a json
summary of the jobs which is shown below. We then use a template (also
below) to render an email every day to remind us to approve the jobs.

Example command (with noop):

::

    $ json2email --plain examples/pipeline_jobs.txt.jinja \
                    --subject '[Pipeline-bot] Jobs needing approval' \
                    --to an_email_address@sanger.ac.uk \
                    --from no-reply@sanger.ac.uk \
                    --server localhost \
                    --error an_admin_address@sanger.ac.uk \
                    --json examples/pipeline_jobs_data.json \
                    --noop

Example output:

::

    Content-Type: text/plain; charset="us-ascii"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit
    Subject: [Pipeline-bot] Jobs needing approval
    From: no-reply@sanger.ac.uk
    To: an_email_address@sanger.ac.uk

    3 jobs require approval
    /parent\_dir/annotation\_job\_tracker.conf has 1 jobs needing admin attention
    /parent\_dir/assembly\_job\_tracker.conf has 2 jobs needing admin attention
    Report last updated at 2015-03-24T15:26:17.246253

Example json:

::

    {
      "created_at": "2015-03-24T15:26:17.246253",
      "jobs": [
        {
          "approval_required": true,
          "config_file": "/parent_dir/assembly_jobs/job_1.conf",
          "job_type": "__Assembly__",
          "pipeline_tracker": "/parent_dir/assembly_job_tracker.conf"
        },
        {
          "approval_required": true,
          "config_file": "/parent_dir/assembly_jobs/job_2.conf",
          "job_type": "__Assembly__",
          "pipeline_tracker": "/parent_dir/assembly_job_tracker.conf"
        },
        {
          "approval_required": false,
          "config_file": "/parent_dir/assembly_jobs/job_3.conf",
          "job_type": "__Assembly__",
          "pipeline_tracker": "/parent_dir/assembly_job_tracker.conf"
        },
        {
          "approval_required": true,
          "config_file": "/parent_dir/annotation_jobs/job_1.conf",
          "job_type": "__Annotation__",
          "pipeline_tracker": "/parent_dir/annotation_job_tracker.conf"
        },
        {
          "approval_required": false,
          "config_file": "/parent_dir/mapping_jobs/job_1.conf",
          "job_type": "__Mapping__",
          "pipeline_tracker": "/parent_dir/mapping_job_tracker.conf"
        },
        {
          "approval_required": false,
          "config_file": "/parent_dir/mapping_jobs/job_2.conf",
          "job_type": "__Mapping__",
          "pipeline_tracker": "/parent_dir/mapping_job_tracker.conf"
        }
      ]
    }

Example template:

::

    {% set jobs_requiring_approval = jobs | selectattr('approval_required') | list -%}
    {%- if jobs_requiring_approval -%}
    {{ jobs_requiring_approval | count }} jobs require approval
    {%- for jobs_in_tracker in jobs_requiring_approval | groupby('pipeline_tracker') %}
    {{ jobs_in_tracker.grouper }} has {{ jobs_in_tracker.list | count }} jobs needing admin attention
    {%- endfor %}
    Report last updated at {{ created_at }}
    {%- endif -%}

Requirements
------------

-  jinja2
-  smtplib
-  email
-  re

For tests:

- unittest
- mock

Testing
-------

Test are run using:

::

    ./run_tests.sh

json2email has been tested on Ubuntu 12.04 with python 2.7.3
