from datetime import datetime, timedelta
import time
import logseq_func
import calaner_func
import viewer_config
import html_func


def create_log_Doc(logseq_address, debug_flag):
    ''' [1] Initial Setting '''
    if debug_flag==True: # debug mode
        logseq_folder_addr=viewer_config.DEBUGGING_ADDRESS# test address
    else:
        logseq_folder_addr=logseq_address

    # Get Main Task List from a specific page

    main_task_list=logseq_func.get_maintask_list(logseq_folder_addr, viewer_config.page_name)

    # set html config
    doc_address=logseq_folder_addr+"\\"+viewer_config.logseq_doc_name

    html_func.set_html_config(doc_address) 


    ''' [2] TASK SCHEDULE TABLE '''
    logseq_func.create_task_Table(doc_address,main_task_list)


    ''' [3] DEADLINE TODO TABLE & NORMAL PRIORITY TABLE'''
    progress_page_list=[]

    for mt in main_task_list:
        progress_page_list.append(mt["main_task"]+".md")

    deadline_tasklist, normal_tasklist=logseq_func.get_todo_list(logseq_folder_addr,progress_page_list)

    # [3]-1 Deadline Table
    logseq_func.create_deadline_todo_Table(doc_address,deadline_tasklist)

    # [3]-2 Normal & Priority Table
    logseq_func.create_normal_todo_table(doc_address,normal_tasklist)

