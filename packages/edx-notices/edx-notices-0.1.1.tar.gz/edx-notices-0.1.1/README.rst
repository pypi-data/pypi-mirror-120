platform-plugin-notices
=============================

|pypi-badge| |ci-badge| |codecov-badge| |doc-badge| |pyversions-badge|
|license-badge|

**This repo is not currently accepting open source contributions**

Overview
--------

This plugin for edx-platform manages notices that a user must acknowledge. It only stores the content of the notices and whether a user has acknowledged them. Presentation and other client side decisions will be left to the frontends that utilize these APIs.

This Django app contains notices that a user must acknowledge before continuing to use the site. This app will have two API endpoints to facilitate that:
1. An endpoint to return any messages the user needs to see (in a limited HTML format) which a client can use to present to the user in a format chosen by the client.
2. An endpoint to acknowledge that a user has seen the notice. This endpoint's URL will be passed to the client via the first endpoint.

Documentation
-------------

(TODO: `Set up documentation <https://openedx.atlassian.net/wiki/spaces/DOC/pages/21627535/Publish+Documentation+on+Read+the+Docs>`_)

Developing in Devstack
~~~~~~~~~~~~~~~~~~~~~~
Make sure the LMS container is running in Devstack, then

.. code-block::

  git clone git@github.com:tuchfarber/platform-plugin-notices.git <devstack_folder>/src
  cd <devstack_folder>/devstack
  make dev.shell.lms
  pip install -e /edx/src/platform-plugin-notices
  cd /edx/app/edxapp/edx-platform
  ./manage.py lms migrate

Once that is done, LMS will pickup the plugin and saves to existing files should cause a devserver restart with your changes. Occasionally when adding a new file, you may need to restart the LMS container in order for it to pickup the changes.

Example client side code
~~~~~~~~~~~~~~~~~~~~~~~~~
This is example plain JS code that will call the API, then show a fixed banner across the top with a button to acknowledge. This is only supposed to be a proof of concept and thus no guarantees are made for this code.

.. code-block:: javascript

    // Gets cookie by name
    const getCookie = (cookieName) =>
      document.cookie
        .split("; ")
        .filter((cookie) => cookie.startsWith(`${cookieName}=`))[0]
        .split("=")[1];

    // Adds banner to screen with an OK button that acknowledges the notice
    const addBanner = (htmlContent, noticeId) => {
      let banner = document.createElement("div");
      let html = document.querySelector("html");
      let acknowledgeButton = document.createElement("button");

      banner.style =
        "padding: 50px; background-color: black; color: white; position: fixed; top: 0%; width: 100%; z-index: 1010";

      acknowledgeButton.textContent = "OK";
      acknowledgeButton.onclick = () => {
        let params = { notice_id: noticeId };
        let postRequest = new XMLHttpRequest();
        postRequest.open("POST", "/api/notices/v1/acknowledge");
        postRequest.setRequestHeader("Content-type", "application/json");
        postRequest.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        postRequest.send(JSON.stringify(params));
        postRequest.onreadystatechange = () => {
          if (postRequest.readyState === 4 && postRequest.status === 200) {
            console.log("acknowledgment successful");
            banner.remove();
          }
        };
      };
      banner.innerHTML = htmlContent;
      banner.append(acknowledgeButton);
      html.append(banner);
    };

    // Check for unacknowledged notices. If they exist add an banner to the screen
    function checkForNotices() {
      let request = new XMLHttpRequest();
      request.open("GET", "/api/notices/v1/unacknowledged");
      request.responseType = "json";
      request.send(null);
      request.onreadystatechange = () => {
        if (request.readyState === 4 && request.status === 200) {
          if (request.response.length > 0) {
            let firstNotice = request.response[0];
            addBanner(firstNotice.html_content, firstNotice.id);
          }
        }
      };
    }


To see this proof of concept once the app is install in LMS, you can:
1. Load an LMS page (e.g. localhost:18000/dashboard)
2. Open the console of your browser
3. Copy and paste the code above [NOTE: Only paste code in your browser that you trust and have reviewed!!!]
4. Run ``checkForNotices()`` in your browser console.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

Contributions are very welcome.
Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.
Even though they were written with ``edx-platform`` in mind, the guidelines
should be followed for all Open edX projects.

The pull request description template should be automatically applied if you are creating a pull request from GitHub. Otherwise you
can find it at `PULL_REQUEST_TEMPLATE.md <.github/PULL_REQUEST_TEMPLATE.md>`_.

The issue report template should be automatically applied if you are creating an issue on GitHub as well. Otherwise you
can find it at `ISSUE_TEMPLATE.md <.github/ISSUE_TEMPLATE.md>`_.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Getting Help
------------

If you're having trouble, we have discussion forums at https://discuss.openedx.org where you can connect with others in the community.

Our real-time conversations are on Slack. You can request a `Slack invitation`_, then join our `community Slack workspace`_.

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx-slack-invite.herokuapp.com/
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help

.. |pypi-badge| image:: https://img.shields.io/pypi/v/platform-plugin-notices.svg
    :target: https://pypi.python.org/pypi/platform-plugin-notices/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/edx/platform-plugin-notices/workflows/Python%20CI/badge.svg?branch=master
    :target: https://github.com/edx/platform-plugin-notices/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/edx/platform-plugin-notices/coverage.svg?branch=master
    :target: https://codecov.io/github/edx/platform-plugin-notices?branch=master
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/platform-plugin-notices/badge/?version=latest
    :target: https://platform-plugin-notices.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/platform-plugin-notices.svg
    :target: https://pypi.python.org/pypi/platform-plugin-notices/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/edx/platform-plugin-notices.svg
    :target: https://github.com/edx/platform-plugin-notices/blob/master/LICENSE.txt
    :alt: License
