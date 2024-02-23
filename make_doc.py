from datetime import datetime, timedelta
import time
import logseq_func
import calaner_func
import viewer_config
import html_func

main_task_list=logseq_func.get_maintask_list(viewer_config.page_address, viewer_config.page_name)



html_start="""
<!DOCTYPE html>


<html lang="kr">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Log View</title>
</head>

<body>
<div>
  <h1>Logseq View</h1>
</div>


<div>
  <h3 class="TASK_LIST__title">Task Schedule</h3>
</div>
"""
html_func.create_Html(html_start)



# Table

'''
table start
'''


table_start='<table class="Schedule_Table">'
html_func.create_Html(table_start)

table_header_start="""
<tr class="Schedule_Table__header">
"""
html_func.create_Html(table_header_start)

# Create Table Header

now=datetime.now() # View from today

for idx in range(viewer_config.logView_Date_Range+2):

    if idx==0: # Main Task Name Col
        table_header_line='<th class="Schedule_Table__tasklist">Main Task</th>'
    elif idx==1: # Sub Task
        table_header_line='<th class="Schedule_Table__tasklist">Sub Task</th>'
    else:      # Day
        idx_date=now+timedelta(days=idx-2) # from today    
        table_header_line='<th class="Schedule_Table__day{0}">{1}</th>'.format(idx,str(idx_date.month)+"/"+str(idx_date.day)+calaner_func.convert_weekday(idx_date.weekday()))
        
    html_func.create_Html(table_header_line)



table_header_end='</tr>'
html_func.create_Html(table_header_end)

# Create Table Contents
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


        table_row_start='<tr class="Schedule_Table_ROW{0} {1} {2} {3} {4}">'.format(cur_row_idx,
                                                                                    logseq_func.get_maintask_name(main_task_list,mt_idx),
                                                                                    sub_task_info["sub_task_name"],
                                                                                    sub_task_info["status"],
                                                                                    sub_task_info["priority"])
        html_func.create_Html(table_row_start)

        for day_idx in range(viewer_config.logView_Date_Range+2):
            if day_idx==0:
                    #and cur_row_idx-1 in task_start_point:

                if cur_row_idx-1 in task_start_point:
                    table_col_main='<td class="Schedule_Table_ROW{0}_COL{1} MainID">{2}</td>'.format(cur_row_idx,day_idx+1,main_task_list[mt_idx]["main_task"])
                    html_func.create_Html(table_col_main)

                else:
                    table_col_main='<td class="Schedule_Table_ROW{0}_COL{1} MainID"></td>'.format(cur_row_idx,day_idx+1)
                    html_func.create_Html(table_col_main)

            elif day_idx==1:
                    table_col_sub='<td class="Schedule_Table_ROW{0}_COL{1} SubID">{2}</td>'.format(cur_row_idx,day_idx+1,main_task_list[mt_idx]["sub_task_list"][st_idx]["sub_task_name"])
                    html_func.create_Html(table_col_sub)
            elif day_idx>=2:
                cal_day=datetime.today()+timedelta(days=day_idx-2)


                # check1 deadline
                if "deadline" in main_task_list[mt_idx]["sub_task_list"][st_idx]:
                        
                        
                    # task deadline
                    deadline_dateformed=datetime.strptime(main_task_list[mt_idx]["sub_task_list"][st_idx]["deadline"],viewer_config.logView_date_format)

                    date_diff=deadline_dateformed-cal_day

                    # Decide cell color

                    if sub_task_info["status"]=="DOING":

                        if (date_diff.days>=0):
                            task_bg_color=logseq_func.get_progress_color(mt_idx,st_idx)
                        else:
                            task_bg_color=viewer_config.basic_bar_color
                                

                    elif sub_task_info["status"]=="TODO":
                        if (date_diff.days==0):
                            task_bg_color=logseq_func.get_progress_color(mt_idx,st_idx)
                        else:
                            task_bg_color=viewer_config.basic_bar_color

                    table_col_day='<td class="Schedule_Table_ROW{0}_COL{1} {2} " bgcolor="{3}"></td>'.format(cur_row_idx,day_idx+1,cal_day,task_bg_color)
                    html_func.create_Html(table_col_day)

                else:
            
                    table_col_day='<td class="Schedule_Table_ROW{0}_COL{1} {2} " bgcolor="{3}"></td>'.format(cur_row_idx,day_idx+1,cal_day,viewer_config.basic_bar_color)
                    html_func.create_Html(table_col_day)

        table_row_end='</tr>'
        html_func.create_Html(table_row_end)

table_end='</table>'
html_func.create_Html(table_end)




'''
table end
'''




todo_header="""

<div>
  <h3 class="Todo_List">Todo List</h3>
</div>

"""
html_func.create_Html(todo_header)


html_end="""
</body>
</html>
"""

html_func.create_Html(html_end)


