\# Screenshot to Code Skill



A reusable agent skill for converting UI screenshots, mockups, and visual references into accurate frontend implementations.



\## Purpose



Use this skill when a user provides:



\- A UI screenshot

\- A mockup

\- A visual reference

\- Multiple screenshots

\- A design that needs to be recreated in code



The skill guides the agent through:



1\. Understanding the reference

2\. Inspecting the existing project

3\. Identifying assets

4\. Planning the implementation

5\. Building the UI

6\. Running the application

7\. Capturing the result

8\. Comparing the result with the reference

9\. Refining visual differences



\## Structure



```text

screenshot-to-code-skill/

├── SKILL.md

├── README.md

├── references/

│   └── workflow.md

└── scripts/

&#x20;   ├── inspect\_project.py

&#x20;   ├── capture\_screenshot.py

&#x20;   ├── compare\_screenshots.py

&#x20;   └── analyze\_assets.py

