# Logseq_Viewer



### *Introduction*

I think Logseq is awesome free tool to manage todo lists or daily notes. However, It is hard to manage all tasks effectively if I only use Logseq. So, I decided to make a viewer program to visually manage all tasks written in Logseq. 



### *Concept*

Logseq Task Management Program to visualize task lists and their respective statuses



### *How to use?*

1. The location of the logseq.json must be in the Logseq folder.

```bash
dir
```

'''Text
pages
journals
assets
logseq.json
logseq_view.html
'''

2. The logseq.json file should contain the necessary information, 
'''json
{
"Logseq_Address" : "C:\\ ... \\logseq",
"Mode":"RUN"
}
'''

- Logseq_Address : Directory of Logseq folder
- Mode "RUN" : Create logseq_view.html automatically 

3. You can set debugging mode in the main.py file

``` Python
''' [DEVELOPER SETTING] '''

DEBUG_MODE=True # True : Debugging Mode
```

4. You can use filtering with priority


