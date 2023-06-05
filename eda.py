import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go


video_file = open('video ipl.mp4', 'rb')
video_bytes = video_file.read()

matches = pd.read_csv('IPL_Matches_2022_2008.csv')
delivery = pd.read_csv('IPL_Ball_by_Ball_2022_2008.csv')
df = matches.merge(delivery , on ='ID')



col1, col2 = st.columns(2)
with col1:
    st.image('ipl logo.jpg', width=300)
with col2:
    st.video(data=video_bytes)

st.sidebar.title('IPL ANALYSIS (2008-2022)')


option = st.sidebar.selectbox('Select One', ['Title Holders','Batsman', 'Bowler', 'Sixes', 'Fours', 'Extra Info' ])

# ******************************************************************************************************************
if option == 'Title Holders':
    btn1 = st.sidebar.button('Click to Know')
    if btn1:
        col1, col2 = st.columns(2)
        # winners of ipl
        with col1:
            st.subheader('IPL Trophy Holder')
            st.dataframe(matches[matches['MatchNumber'] == 'Final'][['Season', 'WinningTeam']].set_index('Season'))

        # Number of Times Trophy Holder
        with col2:
            st.subheader('Number of Times Trophy Holder')
            IPL_winners = matches[matches['MatchNumber'] == 'Final'][['Season', 'WinningTeam']].set_index('Season')
            st.dataframe(IPL_winners.value_counts())



        col3, col4 = st.columns(2)

        # Orange cap holder
        with col3:
            st.subheader('Orange Cap Holder')
            Orange_Cap_Holder = df.groupby(['Season', 'batter'])['batsman_run'].sum().reset_index().sort_values(
                by=['Season', 'batsman_run'], ascending=False)
            st.dataframe(Orange_Cap_Holder.groupby('Season').head(1).set_index('Season'))

        # Purple Cap Holder
        with col4:

            delivery['kind'].value_counts()
            dismissal = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled',
                         'hit wicket']  # only in these cases the wicket credit is given to bowler
            out = df[df['kind'].isin(dismissal)]
            Purple_Cap_Holder = out.groupby(['Season', 'bowler'])['kind'].count().reset_index().sort_values(
                by=['Season', 'kind'], ascending=False)
            Purple_Cap_Holder = Purple_Cap_Holder.groupby('Season').head(1).set_index('Season')

            st.subheader('Purple Cap Holder')
            st.dataframe(Purple_Cap_Holder.rename(columns={'kind': 'number_of_wickets'}))

        # player of match in final match in each season
        st.subheader('Player of match in finals in each season')
        st.dataframe(
            matches[matches['MatchNumber']== 'Final'].reset_index()[['Season','Player_of_Match']].set_index('Season')
        )

# ******************************************************************************************************************

elif option == 'Sixes':

    # Most 6's hit by player

    st.subheader("Most 6's hit by player")
    st.dataframe(
        df[df['batsman_run'] == 6].groupby('batter').count()['batsman_run'].sort_values(
            ascending=False)[:20]
    )

    col1, col2 = st.columns(2)

    # Most 6's in death overs
    with col1:
        st.subheader("Most 6's in death overs")
        st.dataframe(
            df[(df['batsman_run'] == 6) & (df['overs'] >= 16)].groupby('batter').count()['batsman_run'].sort_values(
                ascending=False)[:10]
        )
    # Most 6's in powerplay
    with col2:
        st.subheader("Most 6's in powerplay")
        st.dataframe(df[(df['batsman_run'] == 6) & (df['overs'] <= 6)].groupby('batter').count()['batsman_run'].sort_values(
            ascending=False)[:10]
            )

    col3, col4 = st.columns(2)

    # Most 6's in last over
    with col3:
        st.subheader("Most 6's in last over")
        st.dataframe(
            df[(df['batsman_run'] == 6) & (df['overs'] == 20)].groupby('batter').count()['batsman_run'].sort_values(
                ascending=False)[:10]
        )
    # Most 6's in 1st over
    with col4:
        st.subheader("Most 6's in 1st over")
        st.dataframe(
            df[(df['batsman_run'] == 6) & (df['overs'] == 1)].groupby('batter').count()['batsman_run'].sort_values(
                ascending=False)[:10]
            )

# ******************************************************************************************************************

elif option == 'Fours':

    # Most 4's hit by player

    st.subheader("Most 4's hit by player")
    st.dataframe(
        df[df['batsman_run'] == 4].groupby('batter').count()['batsman_run'].sort_values(
            ascending=False)[:20]
    )


    col1, col2 = st.columns(2)

    # Most 4's in death overs
    with col1:
        st.subheader("Most 4's in death overs")
        st.dataframe(
            df[(df['batsman_run'] == 4) & (df['overs'] >= 16)].groupby('batter').count()['batsman_run'].sort_values(
                ascending=False)[:10]
        )

    # Most 4's in powerplay
    with col2:
        st.subheader("Most 4's in powerplay")
        st.dataframe(
            df[(df['batsman_run'] == 4) & (df['overs'] <= 6)].groupby('batter').count()['batsman_run'].sort_values(
                ascending=False)[:10]
            )

    col3, col4 = st.columns(2)

    # Most 4's in last over
    with col3:
        st.subheader("Most 4's in last over")
        st.dataframe(
            df[(df['batsman_run'] == 4) & (df['overs'] == 20)].groupby('batter').count()['batsman_run'].sort_values(
                ascending=False).head(10)
        )
    # Most 4's in 1st over
    with col4:
        st.subheader("Most 4's in 1st over")
        st.dataframe(
            df[(df['batsman_run'] == 4) & (df['overs'] == 1)].groupby('batter').count()['batsman_run'].sort_values(
                ascending=False)[:10]
        )
# *********************************************************************************************************************

#  Batsman Analysis
elif option == 'Batsman':
    selected_player = st.sidebar.selectbox('Select Batsman', sorted(df['batter'].unique().tolist()))

    btn2 = st.sidebar.button('Click')

    if btn2:


        # Add a selectbox to the app to select a player
        st.subheader('Batsman Analysis:')


        # Filter the dataset to get the stats for the selected player
        selected_player_stats = df[df['batter'] == selected_player]

        # If the selected player is found in the dataset, display his total runs
        if not selected_player_stats.empty:
            total_runs = selected_player_stats['batsman_run'].sum()
            total_runs_season = selected_player_stats.groupby('Season')['batsman_run'].sum().sort_values(ascending=False)

            # Total Runs in IPL
            st.write("Total Runs:")
            st.write(total_runs)


            # Create a line chart trace
            trace = go.Scatter(
                x=selected_player_stats.groupby('Season')['batsman_run'].sum().index,
                y=selected_player_stats.groupby('Season')['batsman_run'].sum().values,
                mode='lines+markers',  # set line and marker style
                line=dict(color='rgb(63, 72, 204)'),  # set line color
                marker=dict(symbol='circle', size=8, color='rgb(63, 72, 204)')  # set marker style and color
            )

            # Set chart layout
            layout = go.Layout(
                title='Total Runs Scored by Season',
                xaxis=dict(title='Season'),
                yaxis=dict(title='Total Runs Scored')
            )

            # Create figure object and add trace and layout
            fig = go.Figure(data=[trace], layout=layout)

            # Display the chart
            st.plotly_chart(fig)

            col1, col2 = st.columns(2)
            grouped_df = selected_player_stats.groupby(['ID', 'batter'])['batsman_run'].sum().sort_values(
                ascending=False)
            df_result = grouped_df.to_frame()
            centuries_hit = df_result[df_result['batsman_run'] >= 100].groupby('batter').count()['batsman_run'].sort_values(ascending=False)

            half_centuries_hit = df_result[(df_result['batsman_run'] >= 50) & (df_result['batsman_run'] < 100)].groupby('batter').count()['batsman_run'].sort_values(ascending=False)
            with col1:
                # Number of Centuries Hit by Batsman
                st.subheader("Number of Centuries Hit by Batsman:")
                st.write(centuries_hit)
            with col2:
                # Number of Half Centuries Hit by Batsman
                st.subheader("Number of Half Centuries Hit by Batsman:")
                st.write(half_centuries_hit)

            st.write('Note: if there is empty then it means batman has not scored century or half century ')


            col3, col4 = st.columns(2)
            with col3:
                total_sixes = selected_player_stats[selected_player_stats['batsman_run'] == 6].groupby('Season').count()[
                    'batsman_run'].sort_values(ascending=False)
                st.subheader("Total 6's Season-Wise:")
                st.write(total_sixes)
            with col4:
                total_fours = selected_player_stats[selected_player_stats['batsman_run'] == 4].groupby('Season').count()[
                    'batsman_run'].sort_values(ascending=False)
                st.subheader("Total 4's Season-Wise:")
                st.write(total_fours)
        else:
            st.write("Selected player is not found in the dataset.")


# ******************************************************************************************************************

#  Bowler Analysis
elif option == 'Bowler':
    selected_player = st.sidebar.selectbox('Select Bowler', sorted(df['bowler'].unique().tolist()))

    btn3 = st.sidebar.button('Click')

    if btn3:
        # Add a selectbox to the app to select a player
        st.subheader('Bowler Analysis:')

        # Filter the dataset to get the stats for the selected player
        selected_player_stats = df[df['bowler'] == selected_player]

        delivery['kind'].value_counts()
        dismissal = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled','hit wicket']  # only in these cases the wicket credit is given to bowler
        total_wickets = df[df['kind'].isin(dismissal)]
        total_wickets.groupby('bowler')['kind'].count().sort_values(ascending=False)

        # If the selected player is found in the dataset, display his total runs
        if not selected_player_stats.empty:
            total_wickets = selected_player_stats['kind'].count()
            total_wickets_season = selected_player_stats.groupby('Season')['kind'].count().sort_values(
                ascending=False)

            # Total Wickets in IPL
            st.write("Total_wickets:")
            st.write(total_wickets)

            # Most number of Dot Balls
            delivery_dot = selected_player_stats[selected_player_stats['total_run'] == 0]
            delivery_dot = delivery_dot.groupby('bowler')['total_run'].count().sort_values(ascending=False)
            st.write('Most number of Dot Balls')
            st.write(delivery_dot)

            col1, col2 = st.columns(2)

            with col1:
                #  wickets taken in Death Over
                out_death_over = selected_player_stats[selected_player_stats['kind'].isin(dismissal)]
                out_death_over = out_death_over[df['overs'] >= 16]

                wickets_death_over = out_death_over.groupby('bowler')['kind'].count().sort_values(ascending=False)
                st.write('Wickets taken in Death Over')
                st.write(wickets_death_over)

            with col2:
                # wickets taken in PowerPlay
                out_powerplay = selected_player_stats[selected_player_stats['kind'].isin(dismissal)]
                out_powerplay = out_powerplay[df['overs'] <= 6]

                wickets_powerplay = out_powerplay.groupby('bowler')['kind'].count().sort_values(ascending=False)
                st.write('Wickets taken in PowerPlay')
                st.write(wickets_powerplay)

            # Create a line chart trace
            trace = go.Scatter(
                x=selected_player_stats.groupby('Season')['kind'].count().index,
                y=selected_player_stats.groupby('Season')['kind'].count().values,
                mode='lines+markers',  # set line and marker style
                line=dict(color='rgb(63, 72, 204)'),  # set line color
                marker=dict(symbol='circle', size=8, color='rgb(63, 72, 204)')  # set marker style and color
            )

            # Set chart layout
            layout = go.Layout(
                title='Total Wickets taken by Season',
                xaxis=dict(title='Season'),
                yaxis=dict(title='Total Wickets taken')
            )

            # Create figure object and add trace and layout
            fig = go.Figure(data=[trace], layout=layout)

            # Display the chart
            st.plotly_chart(fig)




# ********************************************************************************************************************************

else:
    num_of_matches_played = matches['Team1'].value_counts() + matches['Team2'].value_counts()
    num_of_matches_played = num_of_matches_played.sort_values(ascending=False)
    num_of_matches_won = matches['WinningTeam'].value_counts()
    winning_percentage = round((num_of_matches_won / num_of_matches_played) * 100, 2).sort_values(ascending=False)

    col1, col2 = st.columns(2)
    # num_of_matches_played
    with col1:
        st.subheader('Number of Matches Played by Team')
        st.dataframe(num_of_matches_played)

    # num_of_matches_won
    with col2:
        st.subheader('Number of Matches Won by Team')
        st.dataframe(num_of_matches_won)

    col3, col4 = st.columns(2)
    # Top 25 players  with most player of the match
    with col3:
        st.subheader('Top 25 players  with most player of the match')
        st.dataframe(matches['Player_of_Match'].value_counts()[0:25])

    # Top 20  highest Team score  in IPL history
    with col4:
        st.subheader('Top 20  highest Team score  in IPL history')
        st.dataframe(df.groupby(['Season', 'ID', 'BattingTeam']).sum()['total_run'].sort_values(ascending=False)[
                    :20].reset_index().set_index('Season').drop('ID', axis=1)
                     )

    col5, col6 = st.columns(2)
    # stadium with most matches played
    with col5:
        stadium_matches = matches['Venue'].value_counts()
        st.subheader('Stadium with Most Matches Played')
        st.dataframe(stadium_matches)

    # Individual highest score in IPL history
    with col6:
        st.subheader('Individual highest score in IPL history')
        st.dataframe(df.groupby(['ID', 'batter'])['batsman_run'].sum().sort_values(ascending=False).reset_index().set_index(
            'batter').drop('ID', axis=1))



    # how many 6's have hit by team in each over
    sixes = delivery[delivery['batsman_run'] == 6]
    sixes_in_overs= sixes.pivot_table(index=['BattingTeam'], columns=['overs'], values='batsman_run', aggfunc='count')
    st.subheader("Number of 6's hit in each over by team")
    st.dataframe(sixes_in_overs)






