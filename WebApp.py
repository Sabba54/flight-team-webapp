import ssl

import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import requests
from db_fxn import create_table,add_task,view_all_task,view_unique_task,get_task,edit_task_data,delete_task
import plotly.express as px
import plotly.figure_factory as ff
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
from datetime import date

def send_email(team):
    to_addr = 'sabatini.1834805@studenti.uniroma1.it'
    from_addr = 'matteo-sabatini@live.it'
    subject = f'Updated DB da {team}'
    content = '...'
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    body = MIMEText(content,'plain')
    msg.attach(body)
    filename = 'database_tasks.csv'
    with open(filename,'r') as f:
        attachment = MIMEApplication(f.read(),Name=basename(filename))
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
    msg.attach(attachment)
    server = smtplib.SMTP('smtp-mail.outlook.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(from_addr,'okfwillbzcwfacdf')
    server.send_message(msg,from_addr=from_addr,to_addrs=[to_addr])
    server.quit()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<style>",unsafe_allow_html=True)
        
local_css("style/style.css")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

maintenance = 'no'

if maintenance == 'no':
    st.title('Sapienza Flight Team WebApp ✈️')

    teams = ['CAD', 'SOFTWARE', 'HARDWARE', 'ADMIN', 'VISION', 'GESTIONE']
    usernames = ['CAD_team', 'SFTW_team', 'HRDW_team', 'Admin', 'VISION_team', 'GST_team']

    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)

    authenticator = stauth.Authenticate(teams,usernames,hashed_passwords,"FT_WebApp","abcdef",cookie_expiry_days=1)
    team,authentication_state,username = authenticator.login("Login","main")

    if authentication_state == False:
        st.error("Username o Password errati")

    if authentication_state == None:
        st.warning("Perfavore, inserisci username e password")

    if authentication_state:
        if team in ['CAD','SOFTWARE','HARDWARE','VISION','GESTIONE']:


            def main():
                menu = ["Crea Task","Visualizza Task","Aggiorna Task","Elimina Task","Invia Email"]
                choice = st.sidebar.selectbox("Menu",menu)
                authenticator.logout("Logout","sidebar")
                st.sidebar.title(f"Benvenuto {team}")

                create_table(team)
                today = date.today()


                if choice == "Crea Task":
                    start_date = today.strftime("%Y-%m-%d")
                    st.subheader("Aggiungi le task che il team deve svolgere 📝")

                    # Layout
                    col1,col2 = st.columns(2)

                    with col1:
                        task = st.text_area("Task da fare")
                        task_av = st.selectbox("Percentuale di avanzamento",["0","10","20","30","40","50","60","70","80","90","100"])


                    with col2:
                        task_status = st.selectbox("Status",["Da fare","In corso","Terminata"])
                        task_due_date = st.date_input("Data di scadenza")

                    if st.button("Aggiungi"):
                        add_task(team,task,task_status,start_date,task_due_date,task_av,team)
                        st.success("Task aggiunta correttamente!")


                elif choice == "Visualizza Task":
                    st.subheader("Visualizza le Task inserite 📊")
                    result = view_all_task(team)
                    df = pd.DataFrame(result, columns=["Task", "Status","Data di Inizio", "Data di Scadenza","Percentuale di Avanzamento","Team"])
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
                    df = pd.DataFrame(result, columns=["Task", "Status","Data di Inizio", "Data di scadenza","Percentuale di Avanzamento","Team"])
                    with st.expander("Task correnti"):
                        st.dataframe(df)

                    list_of_task = [i[0] for i in view_unique_task(team)]

                    selected_task = st.selectbox("Task da Modificare",list_of_task)
                    selected_result = get_task(team,selected_task)

                    if selected_result:
                        task = selected_result[0][0]
                        task_status = selected_result[0][1]
                        start_date = selected_result[0][2]
                        task_due_date = selected_result[0][3]
                        task_av = selected_result[0][4]

                        col1, col2 = st.columns(2)

                        with col1:
                            new_task = st.text_area("Task da fare",task)
                            new_task_av = st.selectbox("Percentuale di Avanzamento",
                                                   ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"])

                        with col2:
                            new_task_status = st.selectbox("Status", ["Da fare", "In corso", "Terminata"])
                            new_start_date = today.strftime("%Y-%m-%d")
                            new_task_due_date = st.date_input("Data di Scadenza")

                        if st.button("Modifica"):
                            edit_task_data(team,new_task, new_task_status,new_start_date, new_task_due_date,new_task_av, task, task_status,start_date, task_due_date,task_av)
                            st.success("Task modificata correttamente!")

                    result2 = view_all_task(team)
                    df = pd.DataFrame(result2, columns=["Task", "Status","Data di Inizio", "Data di scadenza","Percentuale di Avanzamento","Team"])
                    with st.expander("Task aggiornate"):
                        st.dataframe(df)




                elif choice == "Elimina Task":
                    st.subheader("Elimina le task 🗑")

                    result = view_all_task(team)
                    df = pd.DataFrame(result, columns=["Task", "Status","Data di Inizio", "Data di scadenza","Percentuale di Avanzamento","Team"])
                    with st.expander("Task correnti"):
                        st.dataframe(df)

                    list_of_task = [i[0] for i in view_unique_task(team)]

                    selected_task = st.selectbox("Task da eliminare", list_of_task)
                    st.warning("Sei sicuro di voler eliminare: {}?".format(selected_task))

                    if st.button("Elimina"):
                        delete_task(team,selected_task)
                        st.success("La task è stata eliminata!")

                    result2 = view_all_task(team)
                    df = pd.DataFrame(result2, columns=["Task", "Status","Data di Inizio", "Data di scadenza","Percentuale di Avanzamento","Team"])
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

                if st.sidebar.button("Esporta database"):
                    database_tasks = pd.DataFrame(view_all_task(team), columns=["Task", "Status","Data di Inizio", "Data_scadenza","Percentuale di Avanzamento","Team"])
                    database_tasks.to_csv('database_tasks.csv',index=False)
                    send_email(team)
                    st.success("Database esportato correttamente")






            if __name__ == '__main__':
                main()

        elif team == 'ADMIN':

            def main():
                menu = ['Situazione dei team']
                choice = st.sidebar.selectbox("Menu",menu)
                authenticator.logout("Logout","sidebar")
                st.sidebar.title(f"Benvenuto {team}")

                if choice == 'Situazione dei team':
                    st.subheader("Status dei task")
                    selected_team = st.selectbox('Team',['CAD','SOFTWARE','HARDWARE','VISION','GESTIONE'])
                    result = view_all_task(selected_team)
                    df = pd.DataFrame(result, columns=["Task", "Status","Data di Inizio", "Data di Scadenza","Percentuale di Avanzamento","Team"])
                    with st.expander("Status dei task del singolo team"):
                        st.dataframe(df)

                    df_cad = pd.DataFrame(view_all_task('CAD'), columns=["Task", "Status","Data di Inizio", "Data di Scadenza","Percentuale di Avanzamento","Team"])
                    df_sftw = pd.DataFrame(view_all_task('SOFTWARE'), columns=["Task", "Status","Data di Inizio", "Data di Scadenza","Percentuale di Avanzamento","Team"])
                    df_hrdw = pd.DataFrame(view_all_task('HARDWARE'), columns=["Task", "Status","Data di Inizio", "Data di Scadenza","Percentuale di Avanzamento","Team"])
                    df_vision = pd.DataFrame(view_all_task('VISION'), columns=["Task", "Status","Data di Inizio", "Data di Scadenza","Percentuale di Avanzamento","Team"])
                    df_gst = pd.DataFrame(view_all_task('GESTIONE'), columns=["Task", "Status","Data di Inizio", "Data di Scadenza","Percentuale di Avanzamento","Team"])
                    frames = [df_cad, df_sftw, df_hrdw, df_vision, df_gst]
                    database_tasks = pd.concat(frames)

                    with st.expander("Status dei task di tutti i team"):
                        df_gantt = pd.DataFrame(result,
                                          columns=["Task", "Status","Start", "Finish", "Complete",
                                                   "Team"])
                        df_gantt = df_gantt[(df_gantt['Status']=='In corso') | (df_gantt['Status']=='Da fare') ]
                        df_gantt = df_gantt.drop('Status',axis=1)
                        df_gantt = df_gantt.drop('Team',axis=1)
                        df_gantt['Complete'] = df_gantt['Complete'].astype(int)
                        fig = ff.create_gantt(df_gantt, index_col='Complete', show_colorbar=True)
                        st.plotly_chart(fig)

                if st.sidebar.button("Esporta database"):
                    database_tasks.to_csv('database_tasks.csv',index=False)
                    send_email(team)
                    st.success("Database esportato correttamente")



            if __name__ == '__main__':
                main()

elif maintenance == 'yes':
    st.title('Siamo in Manutenzione. Riprovare più tardi! ✈️')
    lottie = load_lottieurl('https://assets9.lottiefiles.com/private_files/lf30_y9czxcb9.json')
    st_lottie(lottie,height=400,width=400,key='maintenance')






