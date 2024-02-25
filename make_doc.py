from datetime import datetime, timedelta
import time
import logseq_func
import calaner_func
import viewer_config
import html_func

# Get Main Task List from a specific page
main_task_list=logseq_func.get_maintask_list(viewer_config.page_address, viewer_config.page_name)

# set html config
html_func.set_html_config() 


''' --------------- [TASK SCHEDULE TABLE begin] --------------- '''

# Create Table Header
now=datetime.now() # View from today

progress_table_header_html=''
for idx in range(viewer_config.logView_Date_Range+2):

    if idx==0: # Main Task Name Col
        table_header_line='<th class="Schedule_Table__tasklist">Main Task</th>'
    elif idx==1: # Sub Task
        table_header_line='<th class="Schedule_Table__tasklist">Sub Task</th>'
    else:      # Day
        idx_date=now+timedelta(days=idx-2) # from today    
        table_header_line='<th class="Schedule_Table__day{0}">{1}</th>'.format(idx,str(idx_date.month)+"/"+str(idx_date.day)+"\n"+calaner_func.convert_weekday(idx_date.weekday()))

    progress_table_header_html=progress_table_header_html+table_header_line+"\n"



# Create Table Contents
progress_table_contents_html=""

# Task Information
total_task_num=0
task_start_point=[]
for mt_idx in range(len(main_task_list)):
    # task total number
    total_task_num=total_task_num+main_task_list[mt_idx]["sub_task_num"]

    # task start point
    if mt_idx<len(main_task_list)-1:
        if mt_idx==0:
            task_start_point.append(0)
        else:
            task_start_point.append(task_start_point[-1]+main_task_list[mt_idx-1]["sub_task_num"])

    print("task start point",task_start_point)


# Create Table Row
cur_row_idx=0 # current row index

def calc_rowIdx(mt_idx, st_idx):
    if mt_idx==0:
        return st_idx
    

for mt_idx in range(len(main_task_list)):
    for st_idx in range(len(main_task_list[mt_idx]["sub_task_list"])):
        
        # (1) Get subtask info
        sub_task_info=logseq_func.get_subtask_info(main_task_list,mt_idx,st_idx)

  
        cur_row_idx=cur_row_idx+1     # row count +1

        # open <tr> tag
        table_row_start='<tr class="Schedule_Table_ROW{0} {1} {2} {3} {4}">'.format(cur_row_idx,
                                                                                    logseq_func.get_maintask_name(main_task_list,mt_idx),
                                                                                    sub_task_info["sub_task_name"],
                                                                                    sub_task_info["status"],
                                                                                    sub_task_info["priority"])
        
        
        progress_table_contents_html=progress_table_contents_html+table_row_start

        for day_idx in range(viewer_config.logView_Date_Range+2):
            if day_idx==0:

                if cur_row_idx-1 in task_start_point:
                    mt_info_display=main_task_list[mt_idx]["main_task"] # main task name
                else:
                    mt_info_display=""
                
                table_col_main='<td class="Schedule_Table_ROW{0}_COL{1} MainID">{2}</td>'.format(cur_row_idx,day_idx+1,mt_info_display)
  
                progress_table_contents_html=progress_table_contents_html+table_col_main


            elif day_idx==1:
                table_col_sub='<td class="Schedule_Table_ROW{0}_COL{1} SubID">{2}</td>'.format(cur_row_idx,day_idx+1,main_task_list[mt_idx]["sub_task_list"][st_idx]["sub_task_name"])
      
                progress_table_contents_html=progress_table_contents_html+table_col_sub

            elif day_idx>=2:
                cal_day=datetime.today()+timedelta(days=day_idx-2)
                task_bg_color=viewer_config.basic_bar_color

                # check1 deadline
                if "deadline" in main_task_list[mt_idx]["sub_task_list"][st_idx]:
                        
                    # task deadline
                    deadline_dateformed=datetime.strptime(main_task_list[mt_idx]["sub_task_list"][st_idx]["deadline"],viewer_config.logView_date_format)

                    date_diff=deadline_dateformed-cal_day

                    # Decide cell color

                    if sub_task_info["status"]=="DOING":

                        if (date_diff.days>=0):
                            task_bg_color=logseq_func.get_progress_color(mt_idx,st_idx)
                                

                    elif sub_task_info["status"]=="TODO":
                        if (date_diff.days==0):
                            task_bg_color=logseq_func.get_progress_color(mt_idx,st_idx)
             

                table_col_day='<td class="Schedule_Table_ROW{0}_COL{1} {2} " bgcolor="{3}"></td>'.format(cur_row_idx,day_idx+1,cal_day,task_bg_color)
                progress_table_contents_html=progress_table_contents_html+table_col_day
         

        # close <tr> tag
        progress_table_contents_html=progress_table_contents_html+'</tr>'



# Create Progress Task Table
html_func.create_Html("""
<table class="Schedule_Table">
    <tr class="Schedule_Table__header">
        {0}
    </tr>
        {1}            
</table>
""".format(progress_table_header_html,
           progress_table_contents_html
           ))



''' --------------- [TASK SCHEDULE TABLE end] --------------- '''


progress_page_list=[]


for mt in main_task_list:
    progress_page_list.append(mt["main_task"]+".md")

deadline_tasklist, normal_tasklist=logseq_func.get_todo_list(progress_page_list)




''' --------------- [TODO WITH DEADLINE TABLE begin] --------------- '''
# [1] Create Task with Deadline Table

task_dead_table_header="""
    
    <div>
        <h3 style="color: blue;" class="Todo_List">Todo List With Deadline</h3>
    </div>

    <table class="Deadline_Todo_Table">
       <tr class="Deadline_Todo_Header">               
    
"""

for idx in range(viewer_config.logView_Date_Range+1):

    if idx==0: # Main Task Name Col
        table_header_line='<th class="Deadline_Todo">Task</th>'
    else:      # Day
        idx_date=now+timedelta(days=idx-1) # from today    
        table_header_line='<th class="Deadline_Todo__day{0}">{1}</th>'.format(idx,str(idx_date.month)+"/"+str(idx_date.day)+"\n"+calaner_func.convert_weekday(idx_date.weekday()))

    task_dead_table_header=task_dead_table_header+table_header_line+"\n"

task_dead_table_header=task_dead_table_header+'</tr>\n'
html_func.create_Html(task_dead_table_header)


# [2] Create Deadline Table Row and Col
deadline_task_row_info=''

for dead_td_idx in range(len(deadline_tasklist)):
    # (2-1) Create Row
    dead_td_row_start='<tr class="Dead_Todo_ROW{0} {1} {2} {3}">'.format(dead_td_idx+1,
                                                                             deadline_tasklist[dead_td_idx]["sub_task_name"],
                                                                             deadline_tasklist[dead_td_idx]["status"],
                                                                             deadline_tasklist[dead_td_idx]["priority"]
                                                                             )

    deadline_task_row_info=deadline_task_row_info+dead_td_row_start

    # Delay Check
    tsk_deadline=datetime.strptime(deadline_tasklist[dead_td_idx]["deadline"],viewer_config.logView_date_format)
    
    tsk_delay=(datetime.today()-tsk_deadline).days


    # (2-2) Create Col
    for dead_day_idx in range(viewer_config.logView_Date_Range+1):
        if dead_day_idx==0:

            # text color setting
            if tsk_delay>=0: # Delay Situation
                task_txt_color=viewer_config.delayed_text_color
            else:
                task_txt_color=viewer_config.basic_text_color


            td_dead_col='<td class="Dead_Todo_ROW{0}_COL{1}" style="color:{2}">{3}</td>'.format(dead_td_idx+1,
                                                                                                dead_day_idx+1,
                                                                                                task_txt_color,
                                                                                                deadline_tasklist[dead_td_idx]["sub_task_name"])

            deadline_task_row_info=deadline_task_row_info+td_dead_col

        else:
            
            cal_day=datetime.today()+timedelta(days=dead_day_idx-1)

            date_diff=tsk_deadline-cal_day

            if deadline_tasklist[dead_td_idx]["status"]=="DOING":
                    
                if (date_diff.days>=0): # Valid Deadline
                    task_bg_color=logseq_func.get_progress_color(dead_td_idx,3) # 3 ->color setting [tbd]
                    
                else:
                    task_bg_color=viewer_config.basic_bar_color

            elif deadline_tasklist[dead_td_idx]["status"]=="TODO":
                if (date_diff.days==0):
                    task_bg_color=logseq_func.get_progress_color(mt_idx,st_idx)
                else:
                    task_bg_color=viewer_config.basic_bar_color


            # Today Setting
            if cal_day==datetime.today(): # Today
                if tsk_delay>=0:
                    today_info_txt="+"+str(tsk_delay)
                else:
                    today_info_txt=""
            else:
                today_info_txt=""
                
            td_dead_col='<td class="Dead_Todo_ROW{0}_COL{1} {2}" bgcolor="{3}">{4}</td>'.format(dead_td_idx+1,
                                                                                                 dead_day_idx+1,
                                                                                                 datetime.today()+timedelta(days=dead_day_idx-1),
                                                                                                 task_bg_color,
                                                                                                 today_info_txt)

            deadline_task_row_info=deadline_task_row_info+td_dead_col


    deadline_task_row_info=deadline_task_row_info+'</tr>'
html_func.create_Html(deadline_task_row_info)

html_func.create_Html("</table>")
''' --------------- [TODO WITH DEADLINE TABLE end] --------------- '''




''' --------------- [NORMAL TODO TABLE begin] --------------- '''

A_Todo_list=[] # priority A todo list
B_Todo_list=[] # priority B todo list
C_Todo_list=[] # priority C todo list

X_Todo_list=[] # None priority todo list

A_div="""
    <div class="A_Todo_List" {0}>
        <h4> Priority A </h4>
""".format(viewer_config.priority_todo_align_CSS)

B_div="""
    <div class="B_Todo_List" {0}>
        <h4> Priority B </h4>
""".format(viewer_config.priority_todo_align_CSS)

C_div="""
    <div class="C_Todo_List" {0}>
        <h4> Priority C </h4>
""".format(viewer_config.priority_todo_align_CSS)

X_div="""
    <div class="D_Todo_List" {0}>
        <h4> Priority X </h4>
""".format(viewer_config.priority_todo_align_CSS)

for nor_todo in normal_tasklist:
    if nor_todo["priority"]=="A":
        A_Todo_list.append(nor_todo)
        A_div=A_div+"\n <span> - "+nor_todo["sub_task_name"] +"</span>"

    elif nor_todo["priority"]=="B":
        B_Todo_list.append(nor_todo)
        B_div=B_div+"\n <span> - "+nor_todo["sub_task_name"] +"</span>"

    elif nor_todo["priority"]=="C":
        C_Todo_list.append(nor_todo)
        C_div=C_div+"\n <span> - "+nor_todo["sub_task_name"] +"</span>"
    else:
        X_Todo_list.append(nor_todo)
        X_div=X_div+"\n <span> - "+nor_todo["sub_task_name"] +"</span>"


A_div=A_div+"</div>"
B_div=B_div+"</div>"
C_div=C_div+"</div>"
X_div=X_div+"</div>"


# Normal Todo Header

html_func.create_Html("""
                    <div>
                        <h3 style="color: blue;" class="Todo_List">Todo List Without Deadline</h3>
                    </div>
                    
                    <div style="display: flex;">
                      {0} {1} {2}
                    </div>
                      
                    <div>
                      {3}
                    </div>
                      """.format(A_div,B_div,C_div,X_div))

''' --------------- [NORMAL TODO TABLE end] --------------- '''



html_func.create_Html("""
</body>
</html>
""")


