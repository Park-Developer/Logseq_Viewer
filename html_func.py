import viewer_config
def create_Html(html_text):
        
    if "<!DOCTYPE html>" in html_text:
        file_mode='w'
    else:
        file_mode='a'

    log_view_file = open(viewer_config.logseq_view_address, file_mode,encoding='utf8')
    log_view_file.write(html_text)
    log_view_file.close()


def set_html_config():

    create_Html("""
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
                    - Logseq Directory : ?
                </div>
            </div>

            
            <div class="Button_Part">
                
            </div>

            <div>
                <h3 style="color: blue;" class="TASK_LIST__title">Task Schedule</h3>
            </div>
    """)

