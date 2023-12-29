# IMPORT LIBRARIES
from fn__import_py_libs import *
from fn__load_data import *

mapbox_access_token = 'pk.eyJ1IjoiYW5kcmVhYm90dGkiLCJhIjoiY2xuNDdybms2MHBvMjJqbm95aDdlZ2owcyJ9.-fs8J1enU5kC3L4mAJ5ToQ'
#
#
#
#
#
# PAGE CONFIG
st.set_page_config(page_title="ITACA Streamlit App",   page_icon=":book:", layout="wide")

st.markdown(
    """<style>.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 3rem; padding-right: 3rem;}</style>""",
    unsafe_allow_html=True)

# TOP CONTAINER
top_col1, top_col2 = st.columns([6,1])
with top_col1:
    st.markdown("# ITA.C.A")
    st.markdown("#### Analisi di dati meteorologici ITAliani per facilitare l'Adattamento ai Cambiamenti Climatici")
    st.caption('Developed by AB.S.RD - https://absrd.xyz/')
#
#
#
#
#
col1, spacing, col2 = st.columns([9,1,12])

with col1:
    # st.markdown('#### Scopo di questa app')
    st.write('Lo scopo di questa app ITA.C.C.A è quello di colmare alcune **lacune** esistenti rispetto alla disponibilità, all\'interno di standards tecnici e normativi italiani \
              di **dati climatici** capaci di descrivere accuratamente gli **impatti presenti e futuri del cambiamento climatico** nelle varie zone del territorio Italiano.')
    st.write('Questo risulta di importanza capitale per informare la progettazione edile ed impiantistica degli edifici di varie destinazioni d\'uso, \
             e per valutarne il comportamento termico **con particolare riguardo al periodo estivo**.')

    st.divider()
    st.markdown('##### Come utilizzare l\'app:')
    st.markdown('1 Scegliere la regione italiana per visualizzare stazioni meteo disponibili rispetto alle banche dati CTI (*Comitato Termotecnico Italiano*) e COB (*climate.onebuilding.org*)')
    st.code('📂 Scelta Regione')
    st.markdown('2 Scegliere, esplorare e confrontare i dati di temperatura secondo i files normativi italiani (CTI) e quelli piu\' recenti, forniti dal dataset COB. \
                Laddove i dati climatici dei due *datasets* per le stesse località indicano discrepanze significative, la progettazione impiantistica e la modellazione energetica \
                elaborate secondo i dati CTI rischiano di non essere adeguate')
    st.code('📂 Confronto Dati Province')




with col2:
    tab1, tab2, tab3 = st.tabs([":file_cabinet: Il Passato Recente", ":world_map: Il Presente", ":thermometer: Il Futuro"])

with tab1:
    st.markdown('##### Il passato: Anni Tipo Climatici del Comitato Termotecnico Italiano \(CTI\)')
    st.write('Gli anni tipo climatici - *Test Reference Years (TRY)* o *Typical Meteorological Year (TMY)* - vengono forniti dal \
             **Comitato Termotecnico Italiano (CTI)** per 110 località di riferimento distribuite sul territorio nazionale e rappresentano i dati standard \
             ai fini del soddisfacimento della normativa energetica \
             L\'anno tipo climatico consiste in 12 mesi caratteristici scelti da un database di dati meteorologici di un periodo preferibilmente ampio almeno 10 anni.')

    # st.divider()
    with st.expander('*Per avere più dettagli sugli anni tipo climatici - banca dati CTI*'):
        st.write('\n'.join(cti_try_descr01))
        st.write('\n'.join(cti_try_descr02))
        st.caption('Fonte: https://try.cti2000.it/')

    st.divider()
    st.markdown('##### Ulteriori informazioni')
    st.markdown("*What is weather data, and how is it collected?*[https://docs.ladybug.tools/ladybug-tools-academy/v/climate-analysis/]",
                unsafe_allow_html=True)



with tab2:
    st.markdown('##### Il presente: anni tipici recenti dalla banca dati di *climate.onebuilding.org* \(COB\)')
    st.write('The weather data - *Typical Meteorological Years TMYx* - provided at https://climate.onebuilding.org/ are derived from a number of public sources, and produced by translating the source data into the EPW format. \
        TMYx files are typical meterological files derived from ISD \(US NOAA\'s Integrated Surface Database\) with hourly data through 2021 using the TMY/ISO 15927-4:2005 methodologies. \
        ISD individual year files are created using the general principles from the IWEC (International Weather for Energy Calculations) Typical Meteorological Years that was published in 2001. \
        The ERA5 data, courtesy of Oikolab, provides a comprehensive, worldwide gridded solar radiation data set based on satellite data.')
    st.write('For each location, the TMYx file structure \'EGY_AN_Aswan.Intl.AP.624140_TMYx.2007-2021\' indicate data collected for the most recent 15 years \(2007-2021\). Not all locations have recent data.')




with tab3:
    st.markdown('#### Il futuro: proiezioni climatiche e *morphing*')
    st.markdown('#### Il *morphing* dei dati climatici')
    with st.expander('*Dettagli sul morphing di dati climatici per ottenere l\'anno climatico tipo per climi futuri*'):
        st.markdown('\n'.join(weather_morphing_descr01), unsafe_allow_html=True)

    st.markdown('#### Lo strumento *Future Weather Generator*')
# st.dataframe( df_COB_DBT.reindex(sorted(df_COB_DBT.columns), axis=1) )