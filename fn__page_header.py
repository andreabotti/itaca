# IMPORT LIBRARIES
from fn__import_py_libs import *
#
#
#
#
#
def create_page_header():

    st.markdown(
        """<style>.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 3rem; padding-right: 3rem;}</style>""",
        unsafe_allow_html=True)
    #
    # TOP CONTAINER
    TopColA, TopColB = st.columns([6,2])
    with TopColA:
        st.markdown("# ITA.C.A")
        st.markdown("#### Analisi di dati meteorologici ITAliani per facilitare l'Adattamento ai Cambiamenti Climatici")
        st.caption('Developed by AB.S.RD - https://absrd.xyz/')
    #
    with TopColB:
        # Introduce vertical spaces
        st.markdown('<div style="margin: 35px;"></div>', unsafe_allow_html=True)  # 20px vertical space

        # with st.container(border=True):
        with st.container():
            # Your content here
            st.markdown('###### Scegli colore dei markers')
            TopColB1, TopColB2, TopColB3, TopColB4 = st.columns([1,1,1,1])
            with TopColB1:
                color_marker_CTI = st.color_picker(
                    'CTI', '#C4C5C4', help='**CTI = Comitato Termotecnico Italiano** : dati climatici rappresentativi (*anno tipo*) del recente passato',
                    )
            with TopColB2:
                color_marker_COB = st.color_picker(
                    'COB', '#E2966D', help='**COB = climate.onebuilding.org** : dati climatici rappresentativi (*anno tipo*) del presente',
                    )
            with TopColB3:
                color_marker_MSTAT = st.color_picker(
                    'MSTAT', '#85A46E', help='**MSTAT = Meteostat** : dati climatici (*anni reali*) del recente passato e presente',
                    )
            with TopColB4:
                color_marker_FWG = st.color_picker(
                    'FWG', '#6C90AF', help='**FWG = Future Weather Generator** : dati climatici (*anno tipo*) rappresentativi di proiezioni future in linea con gli scenari IPCC',
                    )

    st.markdown('---')
    return color_marker_CTI, color_marker_COB, color_marker_MSTAT, color_marker_FWG