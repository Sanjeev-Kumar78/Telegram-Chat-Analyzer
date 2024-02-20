# Libraries Imported
import streamlit as st
from PIL import Image
from custom_modules import Json_To_text as jtt
from custom_modules import func_use_extract_data as func
from custom_modules import func_analysis as analysis
import io
import time
import sys
import csv


# ------------------------------------------------
image = Image.open('assets/favicon.ico')
# Webpage Title
st.set_page_config(page_title="Telegram Chat Analyzer",
                   page_icon=image, layout="centered", initial_sidebar_state="auto")

# Title of the app
st.header("Telegram Chat Analyzer")

# ------------------------------------------------

# Sidebar
st.sidebar.title("Telegram Chat Analyzer")

# Date Format
st.sidebar.markdown("### Date Format")
date_format = st.sidebar.selectbox('Please select the date format of your file:',
                                   ('mm/dd/yyyy', 'mm/dd/yy',
                                    'dd/mm/yyyy', 'dd/mm/yy',
                                    'yyyy/mm/dd', 'yy/mm/dd'), key='0')
# Upload the file
# to disable warning by file_uploader going to convert into io.TextIOWrapper
st.set_option('deprecation.showfileUploaderEncoding', False)
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['json'])


st.sidebar.markdown('<b>Sanjeev kumar</b>\
                <a href = "https://github.com/Sanjeev-Kumar78" >\
                <a/>', unsafe_allow_html=True)

st.sidebar.markdown("**Don't worry your data is not stored!**")
st.sidebar.markdown("**feel free to use 😊.**")

# paragraph explaining the app
st.write("**Export data from telegram desktop application. The data should be exported in the form of a .json file there will be a option to select extract format. Upload the .json file here and the analysis will be done on the chat history.**")
st.info("In pop menu there's no need for any media files for this analysis.")
st.text("""Steps: 
        1. Open Telegram Desktop Application.
        2. Go to Individual Chat or Group Chat.
        3. Click on the three dots on the top right corner.
        4. Click on Export Chat History.
        5. Select the format in which you want to export the data.
        6. Upload the file here.
    """)
st.warning("**Note: The data should be exported in the form of a .json file there will be a option to select extract format.**")
if uploaded_file is not None:

    converted = jtt.convert_json_to_text(uploaded_file)
    filename = io.StringIO(converted)

    # ------------------------------------------------

    @st.cache_data
    def load_data(date_format=date_format):

        file_contents = []

        if filename is not None:

            content = filename.read()

            # Use StringIO object to create a file-like object
            with io.StringIO(content) as f:
                reader = csv.reader(f, delimiter='\n')
                for each in reader:
                    if len(each) > 0:
                        file_contents.append(each[0])
                    else:
                        file_contents.append('')
        else:
            st.error("Please upload the Telegram chat dataset!")

        return func.read_data(file_contents, date_format)

    try:
        data = load_data()

        if data.empty:
            st.error("Please upload the Telegram chat dataset!")

        if st.sidebar.checkbox("Show raw data", False):
            st.write(data)
        # ------------------------------------------------

        # Members name involve in Chart
        st.sidebar.markdown("### To Analyze select")
        names = analysis.authors_name(data)
        names.append('All')
        member = st.sidebar.selectbox("Member Name", names, key='1')

        if not st.sidebar.checkbox("Hide", True):
            try:
                if member == "All":
                    st.markdown(
                        "### Analyze {} members together:".format(member))
                    st.markdown(analysis.stats(data), unsafe_allow_html=True)

                    st.write("**Top 10 frequent use emoji:**")
                    emoji = analysis.popular_emoji(data)
                    for e in emoji[:10]:
                        st.markdown('**{}** : {}'.format(e[0], e[1]))

                    st.write('**Visualize emoji distribution in pie chart:**')
                    st.plotly_chart(analysis.visualize_emoji(data))

                    st.markdown('**Word Cloud:**')
                    st.text(
                        "This will show the cloud of words which you use, larger the word size most often you use.")
                    st.pyplot(analysis.word_cloud(data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.write('**Most active date:**')
                    st.pyplot(analysis.active_date(data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.write('**Most active time for chat:**')
                    st.pyplot(analysis.active_time(data))
                    # st.pyplot()

                    st.write(
                        '**Day wise distribution of messages for {}:**'.format(member))
                    st.plotly_chart(analysis.day_wise_count(data))

                    st.write('**Number of messages as times move on**')
                    st.plotly_chart(analysis.num_messages(data))

                    st.write('**Chatter:**')
                    st.plotly_chart(analysis.chatter(data))

                else:
                    member_data = data[data['Author'] == member]
                    st.markdown("### Analyze {} chat:".format(member))
                    st.markdown(analysis.stats(member_data),
                                unsafe_allow_html=False)

                    st.write("**Top 10 Popular emoji:**")
                    emoji = analysis.popular_emoji(member_data)
                    for e in emoji[:10]:
                        st.markdown('**{}** : {}'.format(e[0], e[1]))

                    st.write('**Visualize emoji distribution in pie chart:**')
                    st.plotly_chart(analysis.visualize_emoji(member_data))

                    st.markdown('**Word Cloud:**')
                    st.text(
                        "This will show the cloud of words which you use, larger the word size most often you use.")
                    st.pyplot(analysis.word_cloud(member_data))

                    time.sleep(0.2)

                    st.write(
                        '**Most active date of {} on Telegram:**'.format(member))
                    st.pyplot(analysis.active_date(member_data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.write('**When {} is active for chat:**'.format(member))
                    st.pyplot(analysis.active_time(member_data))
                    # st.pyplot()

                    st.write(
                        '**Day wise distribution of messages for {}:**'.format(member))
                    st.plotly_chart(analysis.day_wise_count(member_data))

                    st.write('**Number of messages as times move on**')
                    st.plotly_chart(analysis.num_messages(member_data))

            except:
                e = sys.exc_info()[0]
                st.error("It seems that something is wrong! Try Again. Error Type: {}".format(
                    e.__name__))
        
# --------------------------------------------------

    except:
        e = sys.exc_info()
        st.error(
            "Something is wrong in loading the data! Please select the correct date format or Try again. Error Type: {}.\n \n **For Detail Error Info: {}**".format(e[0].__name__, e[1]))
    # Debugging
    # e = sys.exc_info()
    # st.error("Something is wrong! Try Again. Error Type: {}".format(e))

st.sidebar.markdown(
    "[![built with love](https://forthebadge.com/images/badges/built-with-love.svg)](https://www.linkedin.com/in/sanjeev-kumar78/)")
st.sidebar.markdown(
    "[![smile please](https://forthebadge.com/images/badges/makes-people-smile.svg)](https://www.linkedin.com/in/sanjeev-kumar78/)")