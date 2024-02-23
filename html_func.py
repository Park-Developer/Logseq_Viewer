import viewer_config
def create_Html(html_text):
        
    if "<!DOCTYPE html>" in html_text:
        file_mode='w'
    else:
        file_mode='a'

    log_view_file = open(viewer_config.logseq_view_address, file_mode,encoding='utf8')
    log_view_file.write(html_text)
    log_view_file.close()