import viewer_config
from datetime import datetime

# #logseq_view_address=logseq_address+"\\logseq_view.html"

def create_Html(doc_addr, html_text):
        
    if "<!DOCTYPE html>" in html_text:
        file_mode='w'
    else:
        file_mode='a'

    log_view_file = open(doc_addr, file_mode,encoding='utf8')
    log_view_file.write(html_text)
    log_view_file.close()


def set_html_config(doc_addr):

    # (1) CSS Part
    create_Html(doc_addr,"""
                
        <!DOCTYPE html>

        <html lang="kr">

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Log View</title>
        </head>

        <style>
            .Schedule_Table {
                border-collapse: collapse;
                table-layout:fixed;
            }
            .Schedule_Table__tasklist {
                border: 1px solid black;
           
            }
            .Schedule_Table__day {
                border: 1px solid black;
            }
            .MainID {
                border: 1px solid black;
            }
            .SubID {
                border: 1px dotted gray;
              
            }
     
            .Deadline_Todo_Table{
                border-collapse: collapse;
            }
            .Deadline_Todo{
                border: 1px solid black;
            }
            .Deadline_Todo__day{
                border: 1px solid black;
            }
                
            .A_Todo_List {

            }
                
            .B_Todo_List {
                
            }
                
            .C_Todo_List {
                
            }
                
            .X_Todo_List {
                
            }
        </style>
    """)

    # (2) HTML Body Part
    created_time=datetime.today().strftime("%Y/%m/%d %H:%M:%S")

    create_Html(doc_addr,"""
        <body>
            <div>
                <h1>
                    <b>
                        <i>
                            Logseq Viewer
                        </i>
                    </b>
                </h1>
                
                <div>
                    - Version : V0.1(Proto)
                </div>

                <div>
                    - Logseq Directory : {0}
                </div>

                <div>
                   - Created Time : {1}
                </div>
            </div>

            
    """.format(doc_addr, created_time))



def set_js(doc_addr):
    # Javascript Code for Button
    initial_setting="""
    // Variable Setting
    schedule_table=document.querySelector(".Schedule_Table");
    schedule_table__row_num=schedule_table.rows.length;
    schedule_table__cell_num=schedule_table.rows[0].cells.length;
    
    dead_table=document.querySelector(".Deadline_Todo_Table");


    // Function Definition
    function Priority_btn_click(selected_Priority){
        var main_tsk_name;
        var sub_tsk_num;
            
        for (var row_line = 1; row_line < schedule_table__row_num; row_line++) {
            if(schedule_table.rows[row_line].cells[0].classList.contains("MainID")){

                // initial setting
                var task_idx=row_line; // tbd
                var prior_list=[];
                var name_reset_flag=false;

                                
                // first main task
                main_tsk_name=schedule_table.rows[task_idx].cells[0].innerHTML;
                sub_tsk_num=schedule_table.rows[task_idx].cells[0].dataset.subnum;


                for(var i=0; i<sub_tsk_num;i++){
                    if(schedule_table.rows[task_idx+i].classList.contains(selected_Priority)){
                        prior_list.push(task_idx+i);                    
                    }else{
                        if(schedule_table.rows[task_idx+i].cells[0].classList.contains("MainID")){
                            name_reset_flag=true;
                        }

                       schedule_table.rows[task_idx+i].style.display= 'none';
                    }
                }


                // Name Reset 
                if(name_reset_flag==true && prior_list.length!=0){
                    new_cell_idx=prior_list[0];
                
                    var new_cell = schedule_table.rows[new_cell_idx].insertCell(0);
                    new_cell.innerHTML=main_tsk_name;
                }
                    
                // Resize Row Span
                if(prior_list.length!=0){
                   
                    schedule_table.rows[prior_list[0]].cells[0].rowSpan=prior_list.length;
                }
            }
        }

    }
                


    """

    pri_A_btn_click="""
        function Pri_A_btn_click(){
            reset_btn_click()
            Priority_btn_click("Priority_A")
        }
    """

    pri_B_btn_click="""
        function Pri_B_btn_click(){
            reset_btn_click()
            Priority_btn_click("Priority_B")
        }
    """

    pri_C_btn_click="""
        function Pri_C_btn_click(){
            reset_btn_click()
            Priority_btn_click("Priority_C")
        }
    """
    reset_btn_click="""
    function reset_btn_click() {

        for (var i = 0; i < schedule_table__row_num; i++) {

            if (schedule_table.rows[i].style.display == 'none') {
                schedule_table.rows[i].style.display = '';
            }else{
                //schedule_table__cell_num
           
            }
              
            // Task Start
            if(schedule_table.rows[i].cells[0].classList.contains('MainID')){
            
                schedule_table.rows[i].cells[0].rowSpan=parseInt(schedule_table.rows[i].cells[0].dataset.subnum);
            }else{

                if(schedule_table.rows[i].cells.length>schedule_table__cell_num){
                    schedule_table.rows[i].deleteCell(0);
                }

                schedule_table.rows[i].cells[0].rowSpan=1;
            }
                
       

        }

    
    }
    """

    todo_dead_func="""
    
        function dead_pri_btn_click(selected_priority){
            for(var i=1; i<dead_table.rows.length;i++){
                if(dead_table.rows[i].classList.contains(selected_priority)==false){
                    dead_table.rows[i].style.display= 'none';
                }
            }
        }   
        function dead_pri_reset(){
            for(var i=0; i<dead_table.rows.length;i++){
 
                    dead_table.rows[i].style.display= '';
           
            }
        }  

        
        function todo_reset_btn_click(){
            dead_pri_reset();
        }

        function todo_Pri_A_btn_click(){
            dead_pri_reset();
            dead_pri_btn_click("Priority_A");
        }

        function todo_Pri_B_btn_click(){
            dead_pri_reset();
            dead_pri_btn_click("Priority_B");
        }

        function todo_Pri_C_btn_click(){
            dead_pri_reset();
            dead_pri_btn_click("Priority_C");
        }

"""

    create_Html(doc_addr, """
    <script>
    

    // Function 
    {0}
    {1}
    {2}
    {3}
    {4}            
    {5}        
    </script>

    """.format(initial_setting,
               reset_btn_click,
                pri_A_btn_click,
                pri_B_btn_click,
                pri_C_btn_click,
                todo_dead_func)
               )



def close_html_code(doc_addr):
    
    create_Html(doc_addr,"""
        </body>
        </html>
    """)
