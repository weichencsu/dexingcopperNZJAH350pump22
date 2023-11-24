import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date
import plotly.graph_objects as go
import pandas as pd
import pytz
import requests
#import pyecharts.options as opts
#from pyecharts.charts import Gauge
# mapbox_access_token = open(".mapbox_token").read()
#def SMOOTH_CURVE(data, window):
#    yhat = savgol_filter(data, window, 3)
#    return yhat

@st.cache(persist=True)
def read_file_from_url(url):
    return requests.get(url).content


def serieschart_plot(df):
    # plot time sereis chart
    #dtm = []
    #wl = []

    #for df in sensorSeri:
    #    dtm_tmp, wl_tmp = WEAR_DATA_PARSE(df)
    #    dtm.append(dtm_tmp)
    #    wl.append(wl_tmp)

    # wl = SMOOTH_CURVE(wl, 21)
    #np.savetxt("wearData.csv", wl, delimiter=",")
    fig2 = go.Figure()
    config = {'displayModeBar': False}
    fig2.add_trace(
        go.Scatter(x=df["Date"], y=df["Sensor1"],
                   line=dict(color='royalblue', width=5),
                   name="#1 Row Sensor Current Thickness - [mm]"
                   )
    )

    fig2.add_trace(
        go.Scatter(x=df["Date"], y=df["Sensor2"],
                   line=dict(color='coral', width=5),
                   name="#2 Row Sensor Current Thickness - [mm]"
                   )
    )

    fig2.add_trace(
        go.Scatter(x=df["Date"], y=df["Sensor3"],
                   line=dict(color='green', width=5),
                   name="#3 Row Sensor Current Thickness - [mm]"
                   )
    )
    #margin=dict(l=5, r=5, t=5, b=5),

    fig2.update_xaxes(showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True)

    fig2.update_yaxes(showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True)

    fig2.update_layout(
        xaxis_title="Date",
        yaxis_title="Current Sensor Thickness - [mm]",
        yaxis_range=[0, 50],
        autosize=False,
        #width=1600,
        height=600,
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(
            family="sans serif, regular",
            size=14,
            color="Black"
        )
    )
    #fig2.write_html("timeSeriesSensor.html", config=config)
    return fig2

def WEAR_DATA_PARSE(wf):
    date = wf.split('.txt')[0].split('/')[-1].split('_')[0]
    # hours, minutes, secends = wf.split('.txt')[0].split('_')[1].split('-')
    hours, minutes, secends = wf.split('.txt')[0].split(date)[1].split('_')[1].split('-')
    dtm_obj = date + ' ' + hours + ':' + minutes + ':' + secends
    with open(wf) as f:
        lines = f.readlines()
    wl_obj = int(lines[9].split('\n')[0]) - 2
    ss_obj = int(lines[4].split('\n')[0])
    return dtm_obj, wl_obj, ss_obj

#@st.cache(persist=True)
#def local_pvModel(file_name):
#    st.markdown(
#            f'<iframe src=' + file_name + ' height = "600" width = "100%"></iframe>',
#            unsafe_allow_html=True,
#    )


def main():
    st.set_page_config(page_title="Oresome IoT", layout="wide", initial_sidebar_state='auto')
    st.markdown(
            f"""
            <style>
                .reportview-container .main .block-container{{
                    max-width: 1600px;
                    padding-top: 1rem;
                    padding-right: 1rem;
                    padding-left: 1rem;
                    padding-bottom: 1rem;
                }}

                .fullScreenFrame > div {{
                    display: flex;
                    justify-content: left;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    #page = st.markdown(
    ##            f"""
    #            <style>
    #            .stApp {{
    #                background: url("https://kycg.s3.ap-east-1.amazonaws.com/sidebarBG.png");
    #                background-size: cover
    #            }}
    #            </style>
    #            """,
    #            unsafe_allow_html=True,
    #)

    # define files dir for all inputs
    #     cwd = os.getcwd()
    #cwd = "E:\\2项目资料\\耐普云平台demo"
    #sensorDataDir = 'UDP/'
    

    #sensorName = sensorDataDir + '*.txt'
    #sorted(glob.glob(sensorName))
    #sorted(glob.glob(sensorName), key=os.path.getmtime)
    #sensorSeri = glob.glob(sensorName)
    ##sensorSeri.sort(key=os.path.getmtime)
    #sensen1_data = []
    #sensen2_data = []
    #sensen3_data = []

    #sensen1_dt = []
    #sensen2_dt = []
    #sensen3_dt = []
    #for sss in sensorSeri:
    #    if sss != 'tmp.txt':
    #        latestDate, latestRead, sensor_label = WEAR_DATA_PARSE(sss)
    #        if sensor_label == 1:
    #            sensen1_dt.append(latestDate)
    #            sensen1_data.append(latestRead)
    #        elif sensor_label == 2:
    #            sensen2_dt.append(latestDate)
    #            sensen2_data.append(latestRead)
    #        elif sensor_label == 3:
    #            sensen3_dt.append(latestDate)
    #            sensen3_data.append(latestRead)

    #serieschart_plot(sensen1_dt, sensen1_data, sensen2_dt, sensen2_data, sensen3_dt, sensen3_data)
    #indicator_plot(latestRead)

    #df1 = pd.read_csv("https://raw.githubusercontent.com/oresome/dexing34ftsag/main/sensorThickness.csv")
    df1 = pd.read_csv("sensordata.csv")
    today = date(2022, 7, 10)

    df1['Date'] = pd.to_datetime(df1['Date'], format="%d/%m/%Y")
    mask = df1['Date'].dt.date == today
    filterDF = df1.loc[mask]

    sensen1_data = int(filterDF["Sensor1"].iloc[0])
    sensen2_data = int(filterDF["Sensor2"].iloc[0])
    sensen3_data = int(filterDF["Sensor3"].iloc[0])
    #sensen4_data = 0
    datindex = filterDF.index
    #filterDF_plot = df1.loc[:datindex[0]]
    filterDF_plot = df1.loc[:]


    ###  第一部分  模型展示  ###
    top = st.container()
    with top:
        colll1, colll3 = st.columns([5,1])
        with colll1:
            st.title("DEXING COPPER Intelligent Monitoring System")
            st.header("Dashan Mine - Comminution Circ 5# - NZJAH350 Slurry Pump")
            #st.title("云南驰宏锌锗-会泽矿业")
            #st.subheader("当前状态（在运行） ")
            components.html(
                    """
                        <head>
                            <title> Blinking feature using JavaScript </title>
                            <style>
                                #blink {
                                    font-size: 20px;
                                    font-weight: bold;
                                    font-family: Microsoft Yahei;
                                    color: #6495ED;
                                    transition: 0.05s;
                                }
                            </style>
                        </head>

                        <body>
                            <p id="blink"> Current State [Campaign Completed!]</p>
                            <script type="text/javascript">
                                var blink = document.getElementById('blink');
                                setInterval(function() {
                                    blink.style.opacity = (blink.style.opacity == 0 ? 1 : 0);
                                }, 1000);
                            </script>
                        </body>
                    """,
                    height = 50
                )
        with colll3:
            st.markdown("###")
            st.image("logo.png")



    #st.markdown("###")
    st.markdown("----------------------------------")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("#1 Wear Sensor Reading")
        current_thickness1 = str(sensen1_data) + " mm"
        delta_thickness1 = str(sensen1_data-44) + " mm"
        hktimez = pytz.timezone("Asia/Hong_Kong") 
        #timenowhk = datetime.now(hktimez)
        lastDate = date(2022, 7, 10)
        st.markdown("Latest Sensor Reporing Time: " + lastDate.strftime('%Y-%m-%d'))
        st.metric(label="Current State:", value=current_thickness1, delta=delta_thickness1)
    with col2:
        st.subheader("#2 Wear Sensor Reading")
        current_thickness2 = str(sensen2_data) + " mm"
        delta_thickness2 = str(sensen2_data-44) + " mm"
        hktimez = pytz.timezone("Asia/Hong_Kong") 
        #timenowhk = datetime.now(hktimez)
        lastDate = date(2022, 7, 10)
        st.markdown("Latest Sensor Reporing Time: " + lastDate.strftime('%Y-%m-%d'))
        st.metric(label="Current State:", value=current_thickness2, delta=delta_thickness2)
    with col3:
        st.subheader("#3 Wear Sensor Reading")
        current_thickness3 = str(sensen3_data) + " mm"
        delta_thickness3 = str(sensen3_data-44) + " mm"
        hktimez = pytz.timezone("Asia/Hong_Kong") 
        #timenowhk = datetime.now(hktimez)
        lastDate = date(2022, 7, 10)
        st.markdown("Latest Sensor Reporing Time: " + lastDate.strftime('%Y-%m-%d'))
        st.metric(label="Current State:", value=current_thickness3, delta=delta_thickness3)


        #with col4:
    #with col3:
    #    # echats
    #    PLOT_GAUGE(3.4)
    #    HtmlFile = open("gauge_base.html", "r", encoding='utf-8')
    #    source_code_2 = HtmlFile.read()
    #    components.html(source_code_2, height=400)
        
    
    
    installDate = date(2022, 4, 7)
    currentDate = date(2022, 7, 10)
    deltaDays = (currentDate - installDate).days
    st.subheader("Installed Date: " + installDate.strftime('%Y-%m-%d'))
    st.subheader("Completed Date: " + currentDate.strftime('%Y-%m-%d'))
    st.subheader("Total Campaign Days: " + str(deltaDays) + " Days")
    st.markdown("_______________________________________________________________________")
    #pyLogo = Image.open("install.png")
    st.subheader("Sensor Installation Interactive 3D Model")
    #st.info("如果您正在使用微软EDGE浏览器或谷歌Chrome浏览器，浏览器的设置可能会导致您无法预览三维模型。如需预览，请更换为火狐浏览器，或者请在当前浏览器：设置->Cookie和网站权限->Cookie 和已存储数据/ Cookie 和网站数据->阻止第三方 Cookie ，选项关闭，并刷新页面！")
    #HtmlFile_tSS1 = open("dexxxing.html", 'r', encoding='utf-8').read()
    #components.html(HtmlFile_tSS1, height=500)
    #imgcol1, imgcol2, imgcol3 = st.columns(3)
    #with imgcol1:
    ##im1 = Image.open("install.png")
    #st.image(im1)
    #with imgcol2:
    #    im2 = Image.open("photos/image2.jpg")
    #    st.image(im2)
    #with imgcol3:
    #    im3 = Image.open("photos/image3.jpg")
    #    st.image(im3)
    #@st.cache
    #st.markdown("建设中，敬请期待！")
    #iframeLINK = "https://dexing-pump-nzjah350-7b9d991d6fe-1306024390.tcloudbaseapp.com/DEXING34FTSAG.html"
    #local_pvModel(iframeLINK)
    #pvOBJ = read_file_from_url(iframeLINK)
    #components.html(pvOBJ, height=800)
    
    HtmlFile_tSS1 = open("dexxxing.html", 'r', encoding='utf-8').read()
    components.html(HtmlFile_tSS1, height=1000)

    #st.write(
    #        f'<iframe src=' + iframeLINK + ' height = "1000" width = "100%"></iframe>',
    #        unsafe_allow_html=True,
    #)
    st.markdown("_______________________________________________________________________")

    ###  第三部分  磨损趋势  ###
    st.subheader("Wear Data History")
    #df = pd.read_csv("sensorThickness.csv")
    plotlyfig = serieschart_plot(filterDF_plot)

    st.plotly_chart(plotlyfig, theme="streamlit", use_container_width=True)

    #st.subheader("Time Series Wear History")
    #HtmlFile_tSS = open("timeSeriesSensor.html", 'r', encoding='utf-8').read()
    #components.html(HtmlFile_tSS, height=800)


    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


    footer = """  
            <style>
                .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #50575b;
                color: white;
                text-align: center;
                }
            </style>

            <div class="footer">
                <p>All company names, logos, product names, and identifying marks used throughout this website are the property of their respective trademark owners. Visit us @ www.oresome.com.cn<br></p>
            </div>
        """

    st.markdown(footer,unsafe_allow_html=True)



if __name__ == "__main__":
    main()











