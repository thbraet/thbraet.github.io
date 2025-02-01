---
layout: page
title: "CV"
permalink: /resume/
---

## Contact
- **Name:** {{ site.data.resume.contact.firstname }} {{ site.data.resume.contact.lastname }}
- **Job Title:** {{ site.data.resume.contact.jobtitle }}
- **Email:** [{{ site.data.resume.contact.email_address }}](mailto:{{ site.data.resume.contact.email_address }})
- **LinkedIn:** [LinkedIn Profile]({{ site.data.resume.contact.socials.linkedin }})
- **GitHub:** [GitHub Profile]({{ site.data.resume.contact.socials.github }})

## Education
{% for edu in site.data.resume.education %}
- **{{ edu.topic }}**  
  *{{ edu.institution }} ({{ edu.begin_year }} - {{ edu.end_year }})*
{% endfor %}

## Employment History
{% for job in site.data.resume.employment_history %}
- **{{ job.company }}** ({{ job.begin }} - {{ job.end }})
  - **Title:** {{ job.title }}
  - **Description:** {{ job.topic }}
  - **Tech Stack:** {{ job.tech_stack | join: ", " }}
  - **Key Skills:** {{ job.key_skills | join: ", " }}
{% endfor %}

## Highlights
{% for highlight in site.data.resume.highlights %}
- **{{ highlight.company }}**
  - **Description:** {{ highlight.description }}
  - **Tech Stack:** {{ highlight.tech_stack | join: ", " }}
  - **Key Skills:** {{ highlight.key_skills | join: ", " }}
{% endfor %}

## Skills
{% for skill in site.data.resume.skills %}
- **{{ skill }}**
{% endfor %}

## Languages
{% for language in site.data.resume.languages %}
- **{{ language.language }}:** {{ language.level }}
{% endfor %}

## Certifications
{% for cert in site.data.resume.certifications %}
- **{{ cert.title }}**
  ![{{ cert.title }}]
  <img src="{{ cert.badge_image }}" alt="{{ cert.title }}" style="width: 75px; height: 75px;">

{% endfor %}