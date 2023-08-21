import streamlit as st
import pandas as pd
import plotly.express as px


if __name__ == "__main__":

    st.title('Model Results')

    input_tab, view_tab = st.tabs(["Input", "Plots"])

    if "rows" not in st.session_state:
        st.session_state.rows = []

    with input_tab.form(key='results'):
        name = st.text_input(label='Model Name', key='name')
        notes = st.text_input(label='Model Description')
        recall = st.number_input('Recall', min_value=0., max_value=1., step=0.001)
        precision = st.number_input('Precision', min_value=0., max_value=1., step=0.001)
        f1 = st.number_input('F1 Score', min_value=0., max_value=1., step=0.001)
        cm = st.file_uploader('Confusion Matrix')
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.session_state.rows.append({
            'name': name,
            'notes': notes,
            'recall': recall,
            'precision': precision,
            'f1': f1,
            'Recall': recall,
            'Precision': precision,
            'F1': f1,
            'cm': cm
            })

    st.session_state.df = pd.DataFrame(st.session_state.rows)

    if len(st.session_state.df) > 0:
        view_tab.dataframe(
            st.session_state.df[['name', 'notes', 'F1', 'Precision', 'Recall']].style.highlight_max(
                axis=0, subset=['F1', 'Precision', 'Recall']
            )
        )
        view_tab.plotly_chart(
            px.strip(
                st.session_state.df,
                y=['f1', 'precision', 'recall'],
                color='name',
                hover_data={
                    'name': True,
                    'variable': False,
                    'value': False,
                    'F1': True,
                    'Precision': True,
                    'Recall': True
                },
                range_y=[-0.1, 1.1]
            )
        )

        cm_select = view_tab.selectbox(
            'Model Version',
            options=st.session_state.df.index,
            format_func=lambda choice: st.session_state.rows[choice]['name']
        )
        im_data = st.session_state.rows[cm_select]['cm']
        view_tab.image(im_data)
