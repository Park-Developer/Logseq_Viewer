import viewer_config
import os

# task info get
def get_task_status(task_detail):
    def get_task_priority(line):
        if 'A' in line:
            return ('A',line.index('A'))
        elif 'B' in line:
            return ('B',line.index('B'))
        elif 'C' in line:
            return ('C',line.index('C'))
        else:
            return ("None",-1)

    for status in ["TODO","DOING","NOW","DONE","WAITING"]:
        if status in task_detail:
            if get_task_priority(task_detail):
                priority, prior_idx=get_task_priority(task_detail)
            
            if priority=="None":
                sub_task_name=task_detail[task_detail.index(status)+1:].strip()
                return (True,status,"None",sub_task_name)
            else:
                sub_task_name=task_detail[prior_idx+1:].strip()
                return (True,status,priority,sub_task_name)



    return (False,"none",False,False)

# Main Task List
def get_maintask_list(page_address,page_name):
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
                subtask_file=open(page_address+main_task_name+".md",'r',encoding="utf-8")
            except FileNotFoundError:
                print("file not found!")
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

    return viewer_config.progress_bar_color[main_task_idx][sub_task_idx]


def get_directory_todo_list(progress_page_list,directory):
        # [1] Searching 'pages' directory
    pages_addr=viewer_config.logseq_address+"\\"+directory #"\\pages"
    
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
        td_page_addr=viewer_config.logseq_address+"\\"+directory+"\\"+td_page

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




def get_todo_list(progress_page_list):
    # [1] Searching 'pages' directory
    pages_todo_list=get_directory_todo_list(progress_page_list,"pages")


    # [2] Searching 'journals' directory
    journals_todo_list=get_directory_todo_list(progress_page_list,"journals")

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


