import streamlit as st
import pandas as pd
from db_fxn import create_table,add_task,view_all_task,view_unique_task,get_task,edit_task_data,delete_task
import plotly.express as px
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
from git import Repo


teams = ['CAD','SOFTWARE','HARDWARE','GESTIONE']
usernames = ['CAD_team','SFTW_team','HRDW_team','ADMIN']

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(teams,usernames,hashed_passwords,"FT_WebApp","abcdef",cookie_expiry_days=1)

st.title('Sapienza Flight Team WebApp ✈️')
team,authentication_state,username = authenticator.login("Login","main")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<style>",unsafe_allow_html=True)

local_css("style/style.css")


if authentication_state == False:
    st.error("Username o Password errati")

if authentication_state == None:
    st.warning("Perfavore, inserisci username e password")

if authentication_state:
    if team in ['CAD','SOFTWARE','HARDWARE']:


        def main():
            menu = ["Crea Task","Visualizza Task","Aggiorna Task","Elimina Task","Invia Email"]
            choice = st.sidebar.selectbox("Menu",menu)
            authenticator.logout("Logout","sidebar")
            st.sidebar.title(f"Benvenuto {team}")
            if st.sidebar.button("Aggiorna Database"):
                pass





            create_table(team)

            if choice == "Crea Task":
                st.subheader("Aggiungi le task che il team deve svolgere 📝")

                # Layout
                col1,col2 = st.columns(2)

                with col1:
                    task = st.text_area("Task da fare")

                with col2:
                    task_status = st.selectbox("Status",["Da fare","In corso","Terminata"])
                    task_due_date = st.date_input("Data di scadenza")

                if st.button("Aggiungi"):
                    add_task(team,task,task_status,task_due_date)
                    st.success("Task aggiunta correttamente!")


            elif choice == "Visualizza Task":
                st.subheader("Visualizza le Task inserite 📊")
                result = view_all_task(team)
                df = pd.DataFrame(result, columns=["Task", "Status", "Data di scadenza"])
                with st.expander("Visualizza tutti i task"):
                    st.dataframe(df)

                with st.expander("Status dei task"):
                    task_df = df['Status'].value_counts().to_frame()
                    task_df = task_df.reset_index()
                    pl = px.pie(task_df,names='index',values='Status')
                    st.plotly_chart(pl)



            elif choice == "Aggiorna Task":
                st.subheader("Modifica o Aggiorna le Task 🛠")

                result = view_all_task(team)
                df = pd.DataFrame(result, columns=["Task", "Status", "Data di scadenza"])
                with st.expander("Task correnti"):
                    st.dataframe(df)

                list_of_task = [i[0] for i in view_unique_task(team)]

                selected_task = st.selectbox("Task da Modificare",list_of_task)
                selected_result = get_task(team,selected_task)

                if selected_result:
                    task = selected_result[0][0]
                    task_status = selected_result[0][1]
                    task_due_date = selected_result[0][2]

                    col1, col2 = st.columns(2)

                    with col1:
                        new_task = st.text_area("Task da fare",task)

                    with col2:
                        new_task_status = st.selectbox(task_status, ["Da fare", "In corso", "Terminata"])
                        new_task_due_date = st.date_input(task_due_date)

                    if st.button("Modifica"):
                        edit_task_data(team,new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
                        st.success("Task modificata correttamente!")

                result2 = view_all_task(team)
                df = pd.DataFrame(result2, columns=["Task", "Status", "Data di scadenza"])
                with st.expander("Task aggiornate"):
                    st.dataframe(df)




            elif choice == "Elimina Task":
                st.subheader("Elimina le task 🗑")

                result = view_all_task(team)
                df = pd.DataFrame(result, columns=["Task", "Status", "Data di scadenza"])
                with st.expander("Task correnti"):
                    st.dataframe(df)

                list_of_task = [i[0] for i in view_unique_task(team)]

                selected_task = st.selectbox("Task da eliminare", list_of_task)
                st.warning("Sei sicuro di voler eliminare: {}?".format(selected_task))

                if st.button("Elimina"):
                    delete_task(team,selected_task)
                    st.success("La task è stata eliminata!")

                result2 = view_all_task(team)
                df = pd.DataFrame(result2, columns=["Task", "Status", "Data di scadenza"])
                with st.expander("Task aggiornate"):
                    st.dataframe(df)

            elif choice == "Invia Email":
                st.subheader("Invia email al PM 📩")
                contact_form = """
                <form action="https://formsubmit.co/sabatini.1834805@studenti.uniroma1.it" method="POST">
                  <input type="hidden" name="_captcha" value = "false">
                  <input type="text" name="name" placeholder="Nome e Team" required>
                  <input type="email" name="email" placeholder ="Tua email" required>
                  <textarea name="Messaggio" placeholder="Inserisci qui il tuo messaggio" required></textarea>
                  <button type="submit">Send</button>
                </form>
                """
                left_column,right_column = st.columns(2)
                with left_column:
                    st.markdown(contact_form, unsafe_allow_html=True)
                with right_column:
                    st.empty()



        if __name__ == '__main__':
            main()

    elif team == 'GESTIONE':

        def main():
            menu = ['Situazione dei team']
            choice = st.sidebar.selectbox("Menu",menu)
            authenticator.logout("Logout","sidebar")
            st.sidebar.title(f"Benvenuto {team}")

            if choice == 'Situazione dei team':
                st.subheader("Situazione task dei team")
                selected_team = st.selectbox('Team',['CAD','SOFTWARE','HARDWARE'],)
                result = view_all_task(selected_team)
                df = pd.DataFrame(result, columns=["Task", "Status", "Data di scadenza"])
                with st.expander("Visualizza tutti i task"):
                    st.dataframe(df)

                with st.expander("Status dei task"):
                    df_cad = pd.DataFrame(view_all_task('CAD'), columns=["Task", "Status", "Data di scadenza"])
                    df_cad['TEAM'] = 'CAD'
                    df_sftw = pd.DataFrame(view_all_task('SOFTWARE'), columns=["Task", "Status", "Data di scadenza"])
                    df_sftw['TEAM'] = 'SFTW'
                    df_hrdw = pd.DataFrame(view_all_task('HARDWARE'), columns=["Task", "Status", "Data di scadenza"])
                    df_hrdw['TEAM'] = 'HRDW'
                    frames = [df_cad, df_sftw, df_hrdw]
                    df_final = pd.concat(frames)
                    pl = px.bar(df_final,x='TEAM',color='Status')
                    st.plotly_chart(pl)



        if __name__ == '__main__':
            main()





# Header Section

