from datetime import datetime, timedelta
import time
import logseq_func
import calaner_func
import viewer_config
import html_func


''' [1] Initial Setting '''
# Get Main Task List from a specific page
main_task_list=logseq_func.get_maintask_list(viewer_config.page_address, viewer_config.page_name)

# set html config
html_func.set_html_config() 


''' [2] TASK SCHEDULE TABLE '''
logseq_func.create_task_Table(main_task_list)


''' [3] DEADLINE TODO TABLE & NORMAL PRIORITY TABLE'''
progress_page_list=[]

for mt in main_task_list:
    progress_page_list.append(mt["main_task"]+".md")

deadline_tasklist, normal_tasklist=logseq_func.get_todo_list(progress_page_list)

# [3]-1 Deadline Table
logseq_func.create_deadline_todo_Table(deadline_tasklist)

# [3]-2 Normal & Priority Table
logseq_func.create_normal_todo_table(normal_tasklist)



