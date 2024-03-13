import viewer_config
import os
from datetime import datetime, timedelta
import html_func
import calaner_func
# task info get
def get_task_status(task_detail):
    def get_task_priority(line):
        if '[#A]' in line:
            return ('A',line.index('A'))
        elif '[#B]' in line:
            return ('B',line.index('B'))
        elif '[#C]' in line:
            return ('C',line.index('C'))
        else:
            return ("None",-1)

    for status in ["TODO","DOING","NOW","DONE","WAITING"]:
        if status in task_detail:
            if get_task_priority(task_detail):
                priority, prior_idx=get_task_priority(task_detail)
            
            # Get Task Name
            if priority=="None":
                sub_task_name=task_detail[task_detail.index(status)+len(status):].strip()
     
                return (True,status,"None",sub_task_name)
            else:
                sub_task_name=task_detail[task_detail.index(priority)+len(priority)+1:].strip()
         
                return (True,status,priority,sub_task_name)



    return (False,"none",False,False)

# Main Task List
def get_maintask_list(page_address,page_name):
    print("page add" ,page_address, page_name)
    log_file=open(page_address+page_name,'r',encoding="utf-8")
    lines=log_file.readlines()

    main_task_list=[]

    for line in lines:
        # Main Task
        if "#" in line:
            main_task_name=line[line.index('#')+1:].replace('\n','')


            sub_tasklist=[]
            
            # Sub Task Open 
            try:
                subtask_file=open(page_address+"\\pages\\"+main_task_name+".md",'r',encoding="utf-8")
            except FileNotFoundError:
             
                print("[Err1] file not found!")
            else:
                sub_line=subtask_file.readlines()
                
                for sub_detail in sub_line:

                    is_get, status,priority,sub_task_name=get_task_status(sub_detail)
                    if is_get==True:
                        task_detail={}
                        task_detail["sub_task_name"]=sub_task_name
                        task_detail["status"]=status
                        task_detail["priority"]=priority
                        

                        # sub task condition : Doing or Todo
                        if task_detail["status"]=="TODO" or task_detail["status"]=="DOING":
                            sub_tasklist.append(task_detail)
                    
                    else:
                        if len(sub_tasklist)>=1 and "DEADLINE:" in sub_detail:
                            dead_temp=sub_detail[sub_detail.index("DEADLINE:")+11:].replace('>','').split(" ")
        
                            sub_tasklist[-1]["deadline"]=dead_temp[0].strip()
                        
                
                subtask_file.close()

            # Sub Task Close 

            main_task_list.append({"main_task":main_task_name,
                                "sub_task_list":sub_tasklist,
                                "sub_task_num":len(sub_tasklist)
                                })

    return main_task_list


def get_maintask_name(main_task_list,main_task_idx):
    return main_task_list[main_task_idx]["main_task"]

def get_subtask_info(main_task_list,main_task_idx,sub_task_idx):
    return main_task_list[main_task_idx]["sub_task_list"][sub_task_idx]


def get_progress_color(main_task_idx,sub_task_idx)->str:
    color_num= len(viewer_config.progress_bar_color)
    color_bright_num=len(viewer_config.progress_bar_color[0])
    
    return viewer_config.progress_bar_color[main_task_idx % color_num][sub_task_idx % color_bright_num]


def get_directory_todo_list(logseq_folder_addr,progress_page_list,directory):
        # [1] Searching 'pages' directory
    pages_addr=logseq_folder_addr+"\\"+directory #"\\pages"
    
    all_page_list=os.listdir(pages_addr)

    todo_pages_list=[]

    # filtering directory page to exclude progress task pages
    for page in all_page_list:
        if page not in progress_page_list:
            todo_pages_list.append(page)

    all_todolist=[] # todo list with deadline

    # [2] Get Task list
    for td_page in todo_pages_list:
        # [2]-1 Page Open
        td_page_addr=logseq_folder_addr+"\\"+directory+"\\"+td_page

        log_file=open(td_page_addr,'r',encoding="utf-8")
        td_lines=log_file.readlines()
        
        for line in td_lines:
            is_get, status,priority,sub_task_name=get_task_status(line)

            if is_get==True:
                todo_detail={}
                todo_detail["sub_task_name"]=sub_task_name
                todo_detail["status"]=status
                todo_detail["priority"]=priority
                        

                # sub task condition : Doing or Todo
                if todo_detail["status"]=="TODO" or todo_detail["status"]=="DOING":
                    all_todolist.append(todo_detail)
                    
            else:
                if len(all_todolist)>=1 and "DEADLINE:" in line:
                    dead_temp=line[line.index("DEADLINE:")+11:].replace('>','').split(" ")
        
                    all_todolist[-1]["deadline"]=dead_temp[0].strip()
        
        log_file.close()


    return all_todolist




def get_todo_list(logseq_folder_addr,progress_page_list):
    # [1] Searching 'pages' directory
    pages_todo_list=get_directory_todo_list(logseq_folder_addr,progress_page_list,"pages")


    # [2] Searching 'journals' directory
    journals_todo_list=get_directory_todo_list(logseq_folder_addr,progress_page_list,"journals")

    # [3] Sum of both directory's todo list
    all_todolist=pages_todo_list+journals_todo_list

    # [4] Divide Task List
    deadline_tasklist=[]
    normal_tasklist=[]

    for tsk in all_todolist:
        if "deadline" in tsk:
            deadline_tasklist.append(tsk)
        else:
            normal_tasklist.append(tsk)
    
    
    return deadline_tasklist, normal_tasklist


def create_task_Table(doc_address,main_task_list):
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
            
            what_day=calaner_func.convert_weekday(idx_date.weekday())
            if what_day=="(Sat)" or what_day=="(Sun)":
                txt_color=viewer_config.weekend_text_color
            else:
                txt_color=viewer_config.basic_text_color
            

            table_header_line='<th class="Schedule_Table__day Schedule_Table__day{0}" style="color:{1}">{2}</th>'.format(idx,txt_color,str(idx_date.month)+"/"+str(idx_date.day)+"\n"+calaner_func.convert_weekday(idx_date.weekday()))

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
        if mt_idx<len(main_task_list):
            if mt_idx==0:
                task_start_point.append(0)
            else:
                task_start_point.append(task_start_point[-1]+main_task_list[mt_idx-1]["sub_task_num"])

        
    print("start",task_start_point)

    # Create Table Row
    cur_row_idx=0 # current row index

    def calc_rowIdx(mt_idx, st_idx):
        if mt_idx==0:
            return st_idx
        

    for mt_idx in range(len(main_task_list)):
        for st_idx in range(len(main_task_list[mt_idx]["sub_task_list"])):
            
            # (1) Get subtask info
            sub_task_info=get_subtask_info(main_task_list,mt_idx,st_idx)

    
            cur_row_idx=cur_row_idx+1     # row count +1

            # open <tr> tag
            table_row_start='<tr class="Schedule_Table_ROW{0} {1} {2} {3} {4}">'.format(cur_row_idx,
                                                                                        get_maintask_name(main_task_list,mt_idx),
                                                                                        sub_task_info["sub_task_name"],
                                                                                        sub_task_info["status"],
                                                                                        sub_task_info["priority"])
            
            
            progress_table_contents_html=progress_table_contents_html+table_row_start

            for day_idx in range(viewer_config.logView_Date_Range+2):
                if day_idx==0: # main task name

                    if cur_row_idx-1 in task_start_point:
                        mt_info_display=main_task_list[mt_idx]["main_task"] 
                
                        sub_task_num=len(main_task_list[mt_idx]["sub_task_list"])

                        table_col_main='<td class="Schedule_Table_ROW{0}_COL{1} MainID" rowspan="{2}">{3}</td>'.format(cur_row_idx,day_idx+1,sub_task_num,mt_info_display)
        
                        progress_table_contents_html=progress_table_contents_html+table_col_main


                elif day_idx==1: # Sub task Name
                    sub_task_name_color=viewer_config.basic_text_color

                    # deadline check
                    if "deadline" in main_task_list[mt_idx]["sub_task_list"][st_idx]:
                        sub_task_delay=(datetime.today()-datetime.strptime(main_task_list[mt_idx]["sub_task_list"][st_idx]["deadline"],viewer_config.logView_date_format)).days
                        if sub_task_delay>=0: # delay situation
                            sub_task_name_color=viewer_config.delayed_text_color

                    table_col_sub='<td class="Schedule_Table_ROW{0}_COL{1} SubID" style="color:{2}">{3}</td>'.format(cur_row_idx,
                                                                                                                    day_idx+1,
                                                                                                                    sub_task_name_color,
                                                                                                                    main_task_list[mt_idx]["sub_task_list"][st_idx]["sub_task_name"])
        
                    progress_table_contents_html=progress_table_contents_html+table_col_sub

                elif day_idx>=2: # Calander Chart
                    cal_day=datetime.today()+timedelta(days=day_idx-2)
                    task_bg_color=viewer_config.basic_bar_color
                    delay_inf=""

                    # check1 deadline
                    if "deadline" in main_task_list[mt_idx]["sub_task_list"][st_idx]:
                            
                        # task deadline
                        deadline_dateformed=datetime.strptime(main_task_list[mt_idx]["sub_task_list"][st_idx]["deadline"],viewer_config.logView_date_format)

                        date_diff=deadline_dateformed-cal_day
                        
                        # Delay Check
                        delayed_day=(datetime.today()-deadline_dateformed).days
                        if (cal_day==datetime.today() and delayed_day>=0): #delay situation
                            delay_inf="+"+str(delayed_day)
                
                        # Decide cell color
                        if sub_task_info["status"]=="DOING":

                            if (date_diff.days>=0):
                                task_bg_color=get_progress_color(mt_idx,st_idx)
                                    

                        elif sub_task_info["status"]=="TODO":
                            if (date_diff.days==0):
                                task_bg_color=get_progress_color(mt_idx,st_idx)
                

                    table_col_day='<td class="Schedule_Table_ROW{0}_COL{1} {2} " bgcolor="{3}">{4}</td>'.format(cur_row_idx,
                                                                                                                day_idx+1,
                                                                                                                cal_day,
                                                                                                                task_bg_color,
                                                                                                                delay_inf)
                    progress_table_contents_html=progress_table_contents_html+table_col_day
            

            # close <tr> tag
            progress_table_contents_html=progress_table_contents_html+'</tr>'



    # Create Progress Task Table
            
    html_func.create_Html(doc_address,"""
    <table class="Schedule_Table">
        <tr class="Schedule_Table__header">
            {0}
        </tr>
            {1}            
    </table>
    """.format(progress_table_header_html,
            progress_table_contents_html
            ))

def create_deadline_todo_Table(doc_address,deadline_tasklist):

    now=datetime.now() # View from today



    # [1] Create Task with Deadline Table
    deadline_todo_header_html=""

    for idx in range(viewer_config.logView_Date_Range+1):

        if idx==0: # Main Task Name Col
            deadline_todo_header_html=deadline_todo_header_html+'<th class="Deadline_Todo">Task</th>'
        else:      # Day
            idx_date=now+timedelta(days=idx-1) # from today    


            what_day=calaner_func.convert_weekday(idx_date.weekday())
            if what_day=="(Sat)" or what_day=="(Sun)":
                txt_color=viewer_config.weekend_text_color
            else:
                txt_color=viewer_config.basic_text_color


            deadline_todo_header_html=deadline_todo_header_html+'<th class="Deadline_Todo__day Deadline_Todo__day{0}" style="color:{1}">{2}</th>'.format(idx,txt_color,str(idx_date.month)+"/"+str(idx_date.day)+"\n"+calaner_func.convert_weekday(idx_date.weekday()))


    # [2] Create Deadline Table Row and Col

    deadline_todo_contents_html=""


    for dead_td_idx in range(len(deadline_tasklist)):
        # (2-1) Create Row
        dead_td_row_start='<tr class="Dead_Todo_ROW{0} {1} {2} {3}">'.format(dead_td_idx+1,
                                                                                deadline_tasklist[dead_td_idx]["sub_task_name"],
                                                                                deadline_tasklist[dead_td_idx]["status"],
                                                                                deadline_tasklist[dead_td_idx]["priority"]
                                                                                )

        deadline_todo_contents_html=deadline_todo_contents_html+dead_td_row_start

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

                deadline_todo_contents_html=deadline_todo_contents_html+td_dead_col

            else:
                
                cal_day=datetime.today()+timedelta(days=dead_day_idx-1)

                date_diff=tsk_deadline-cal_day

                if deadline_tasklist[dead_td_idx]["status"]=="DOING":
                        
                    if (date_diff.days>=0): # Valid Deadline
                        task_bg_color=get_progress_color(dead_td_idx,3) # 3 ->color setting [tbd]
                        
                    else:
                        task_bg_color=viewer_config.basic_bar_color

                elif deadline_tasklist[dead_td_idx]["status"]=="TODO":
                    if (date_diff.days==0):
                        task_bg_color=get_progress_color(dead_td_idx,3)
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

                deadline_todo_contents_html=deadline_todo_contents_html+td_dead_col


        deadline_todo_contents_html=deadline_todo_contents_html+'</tr>'



    # Create Deadline Todo Table
    html_func.create_Html(doc_address,"""
        
        <div>
            <h3 style="color: blue;" class="Todo_List">Todo List With Deadline</h3>
        </div>

        <table class="Deadline_Todo_Table">
            <tr class="Deadline_Todo_Header">               
                {0}
            </tr>
                {1}
        </table>
    """.format(deadline_todo_header_html,deadline_todo_contents_html))

def create_normal_todo_table(doc_address,normal_tasklist):
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
    html_func.create_Html(doc_address,"""
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



    html_func.create_Html(doc_address,"""
    </body>
    </html>
    """)
