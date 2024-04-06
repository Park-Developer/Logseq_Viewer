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

                
            <title>Logseq Viewer</title>
        </head>

        <style>
            .Program_Info__font{
                font-size:50%;
            }
            
            .Contents_Header{
                margin-top:5%;
                margin-bottom:0;
            }
            .Button_SubInfo__font{
                font-size:70%;
            }
                
            .Schedule_Table {
                border-collapse: separated;
                table-layout:fixed;
                border-spacing: 0em 0.3em;
                width:100%;

            }
                

            .Table_Header__Main{
                border: 1px solid black;
                width: 10%;
                
                white-space: nowrap; /* Prevent text from wrapping */
                overflow: hidden; /* Hide overflow content */
                text-overflow: ellipsis; /* Show ellipsis (...) for overflow text */
            }
            .Table_Header__Sub{
                border: 1px solid black;
                width: 10%;

                white-space: nowrap; /* Prevent text from wrapping */
                overflow: hidden; /* Hide overflow content */
                text-overflow: ellipsis; /* Show ellipsis (...) for overflow text */
               
            }
            .Table_Header__Day{
                font-size:70%;
                border: 1px solid black;
            }
            

            .MainID {
                width: 10%;
                border: 1px solid black;

                
                white-space: nowrap; /* Prevent text from wrapping */
                overflow: hidden; /* Hide overflow content */
                text-overflow: ellipsis; /* Show ellipsis (...) for overflow text */
            }
                
            .SubID {
                width: 10%;
                border: 1px dotted gray;

                white-space: nowrap; /* Prevent text from wrapping */
                overflow: hidden; /* Hide overflow content */
                text-overflow: ellipsis; /* Show ellipsis (...) for overflow text */
            }
            
            .Table_Day{
                font-size:70%;
                font-style: italic;
            }
     
            .Deadline_Todo_Table{
                border-collapse: collapse;

                table-layout:fixed;
                width:100%;
            }   
                
            .Deadline_Todo__Task{
                width: 20%;
                border: 1px solid black;
            }
            .Deadline_Todo__Day{
                font-size:70%;
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
                
                <div class="Program_Info__font">
                    - Version : V0.1(Proto)
                </div>

                <div class="Program_Info__font">
                    - Logseq Directory : {0}
                </div>

                <div class="Program_Info__font">
                   - Created Time : {1}
                </div>
            </div>

            
    """.format(doc_addr, created_time))


# Javascript Code
def set_js(doc_addr):

    initial_setting="""
    /* Developer Setting */

    PERIOD_MODIFICATION=10;

    """

    # Schedule Table Javascript
    inprogress_task_func="""
    /* [Schedule Table Function]  */

    // Variable Setting
    schedule_table=document.querySelector(".Schedule_Table");
    schedule_table__row_num=schedule_table.rows.length;
    schedule_table__cell_num=schedule_table.rows[0].cells.length;

    /* [Function Definition] */

    // Combo Box Filtering
    function task_combo_filtering(e){
        reset_btn_click(); // reset flitering

        const selected_task=e.value;
      
        if (selected_task=="-- ALL --"){
            reset_btn_click(); // reset

        }else{
            selected_tr_cls='MAIN_' + selected_task + '_';

            for (var i = 1; i < schedule_table__row_num; i++) { // header remain
                if(schedule_table.rows[i].classList.contains(selected_tr_cls)){
                    
                }else{
                    schedule_table.rows[i].style.display= 'none';
                }
            }

        }

    }

    
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
                
                    // Add Main Taskname
                    var new_cell = schedule_table.rows[new_cell_idx].insertCell(0);
                    new_cell.innerHTML=main_tsk_name;

                    // Add temporary Class
                    schedule_table.rows[new_cell_idx].classList.add("Temp_Main");
                }
                    
                // Resize Row Span
                if(prior_list.length!=0){
                   
                    schedule_table.rows[prior_list[0]].cells[0].rowSpan=prior_list.length;
                }
            }
        }

    }


    // A Priority Filtering
    function Pri_A_btn_click(){
        reset_btn_click();
        Priority_btn_click("Priority_A");
    }

    // B Priority Filtering
    function Pri_B_btn_click(){
        reset_btn_click();
        Priority_btn_click("Priority_B");
    }

    // C Priority Filtering
    function Pri_C_btn_click(){
        reset_btn_click();
        Priority_btn_click("Priority_C");
    }

    // None Priority Filtering
    function Pri_X_btn_click(){
        reset_btn_click();
        Priority_btn_click("Priority_None");
    }

    // Reset Filtering    
    function reset_btn_click() {

        for (var i = 0; i < schedule_table__row_num; i++) {
            if (schedule_table.rows[i].style.display == 'none') {
                schedule_table.rows[i].style.display = '';
            }
                
            // Identify Temp Main Task
            if(schedule_table.rows[i].classList.contains('Temp_Main')){
                schedule_table.rows[i].deleteCell(0);
                schedule_table.rows[i].classList.remove('Temp_Main');
            }


            // Task Start
            if(schedule_table.rows[i].cells[0].classList.contains('MainID')){
                
                schedule_table.rows[i].cells[0].rowSpan=parseInt(schedule_table.rows[i].cells[0].dataset.subnum);
            }else{
                schedule_table.rows[i].cells[0].rowSpan=1;
            }
                
        }  
    }

    // Period Button
    function Period_btn_click(){
        var col_num;
        var period_cut;

        for (var i = 0; i < schedule_table__row_num; i++) {

            if(schedule_table__cell_num==schedule_table.rows[i].cells.length){
                col_num=schedule_table__cell_num;
                period_cut=PERIOD_MODIFICATION+2;
            }else{
                col_num=schedule_table.rows[i].cells.length;
                period_cut=PERIOD_MODIFICATION+1;
            }


            for(var j=0;j<col_num;j++){
                if(j>=period_cut){
             
                    schedule_table.rows[i].cells[j].style.display= 'none';
                }
                
            }
        }
    }
    """

    # Deadline Todolist Javascript
    todo_dead_func="""
        dead_table=document.querySelector(".Deadline_Todo_Table");
        dead_table_cell_num=dead_table.rows[0].cells.length;
        

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

        // A Priority Filtering
        function todo_Pri_A_btn_click(){
            dead_pri_reset();
            dead_pri_btn_click("Priority_A");
        }

        // B Priority Filtering
        function todo_Pri_B_btn_click(){
            dead_pri_reset();
            dead_pri_btn_click("Priority_B");
        }

        // C Priority Filtering
        function todo_Pri_C_btn_click(){
            dead_pri_reset();
            dead_pri_btn_click("Priority_C");
        }

        // X Priority Filtering
        function todo_Pri_X_btn_click(){
            dead_pri_reset();
            dead_pri_btn_click("Priority_None");
        }

        
        // Period Modification
        function todo_Period_btn_click(){
            for (var i = 0; i < dead_table.rows.length; i++) {
                for(var j=0;j<dead_table_cell_num;j++){
                    if(j>=PERIOD_MODIFICATION+1){
                        dead_table.rows[i].cells[j].style.display= 'none';
                    }
                    
                }
            }
        }
"""

    create_Html(doc_addr, """
    <script>
    
    {0}
    {1}
    {2}
       
    </script>

    """.format(initial_setting,
          inprogress_task_func,
                todo_dead_func)
               )



def close_html_code(doc_addr):
    
    create_Html(doc_addr,"""
        </body>
        </html>
    """)
