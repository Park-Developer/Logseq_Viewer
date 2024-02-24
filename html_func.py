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

        <body>
            <div>
                <h1>
                    <b>
                        <i>
                            Logseq Viewer
                        </i>
                    </b>
                </h1>
                
                <span>
                    - Version : V1.0
                </span>
            </div>

            
            <div>
                <h3 style="color: blue;" class="TASK_LIST__title">Task Schedule</h3>
            </div>
    """)

