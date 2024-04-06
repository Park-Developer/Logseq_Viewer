# Initial Directory Parameter
page_name="\\pages\\[진행중인 업무].md"
logseq_doc_name="logseq_view.html"
#page_address=logseq_address+"\\pages\\"
#logseq_view_address=logseq_address+"\\logseq_view.html"


# Debugging Setting
DEBUGGING_ADDRESS="C:\\Users\\gnvid\\OneDrive\\바탕 화면\\logseq" # test address


# - System Information
logView_date_format="%Y-%m-%d"
logView_Date_Range=30


# UI Setting

# Background Color
basic_bar_color="#FFFFFF" # white
color_order_rise=False

# Task Ghant Chart Color
progress_bar_color=[
    ["#D6E4FF","#ADC8FF","#84A9FF","#6690FF","#3366FF","#254EDB","#1939B7","#102693","#091A7A"], # Blue
    ["#F4FDCD","#E7FC9C","#D2F669","#BDED44","#9EE20B","#81C208","#66A205","#4E8303","#3D6C02"], # light Green
    ["#D7FDF3","#B0FCED","#88F8EB","#69F1EC","#3ADFE8","#2AB2C7","#1D88A7","#126386","#0B486F"],  # Light Blue
    ["#FEF5DB","#FEE8B8","#FED894","#FDC87A","#FCAE4E","#D88939","#B56827","#924B18","#78360E"],  # Brown
    ["#FFE7D9","#FFC9B3","#FFA48D","#FF8171","#FF4842","#DB3039","#B72136","#931531","#7A0C2E"]  # Red
    
]

# Set Color Order
if color_order_rise==False:
    for color_bar in progress_bar_color:
        color_bar.reverse()


# Text Color
basic_text_color="#000000" # black
delayed_text_color= "#FF0000" # red

weekend_text_color="#FF0000" # red

# Todo List CSS
priority_todo_align_CSS='style="display: flex; flex-direction:column; flex:1"'
