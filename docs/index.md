---
layout: default
title: Home
nav_order: 1
description: "Deemon Redux is a monitoring utility for new artist releases that can provide email alerts and automate downloading via the deemix library"
permalink: /
---

# Deemon Redux 2.25 Documentation
{: .fs-9 }

Deemon Redux is a monitoring utility for new artist releases that can provide email alerts and automate downloading via the deemix library
{: .fs-6 .fw-300 }

[Get started now](#getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub]({{ site.github.repository_url | default: site.repository_url | default: "https://github.com/mon5termatt/deemon-redux" }}){: .btn .fs-5 .mb-4 .mb-md-0 }

<small>Version 2.25</small>
---

## Disclaimer

Deemon Redux does not download anything by itself. It requires a third party library 
called *deemix* in order to do this and will be installed automatically when 
installed via pip. [deemix on PyPI](https://pypi.org/project/deemix/)

Deemix Development has been discontinued and is no longer being actively developed. Deemon Redux will attempt to stay updated with the latest versions of deemix as long as possible. If this becomes an issue, please open an issue on the GitHub repository. 

The maintained fork of deemix is not compatible with Deemon Redux and is not recommended for use. See [bambanah/deemix](https://github.com/bambanah/deemix) if you are interested in using it.

---

## Getting started

### Dependencies

Deemon Redux depends on various python modules and libraries to perform all of its functions. Please refer to the `requirements.txt` file to see what those dependencies are.

### Installation & Configuration

When you're ready to install Deemon Redux, head on over to the 
[installation]({{ site.baseurl }}{% link docs/installation.md %}) page. Once 
you've installed Deemon Redux, it is important to 
[configure]({{ site.baseurl }}{% link docs/configuration.md %}) it properly to 
get the best experience.


---

## About the project

Deemon Redux (**dee**zer **mon**itor) is a continuation of the archived [deemon](https://github.com/digitalec/deemon) project — an open source tool for staying on top of new releases by your favorite artists.

### License

Deemon Redux is distributed under a [GPL-3.0 license]({{ site.github.repository_url | default: site.repository_url | default: "https://github.com/mon5termatt/deemon-redux" }}/blob/main/LICENSE).
