import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings 
warnings.filterwarnings('ignore')

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.expand_frame_repr',False)
pd.set_option('max_colwidth',None)

ipl_df = pd.read_csv(r"C:\Users\ANAIKUTTY\Documents\Cricket analysis\data files\ipl_2008_2024_ball_by_ball_data.csv")

df = ipl_df.copy()

df['isdot'] = df['runs_off_bat'].apply(lambda x: 1 if x == 0 else 0)
df['isone'] = df['runs_off_bat'].apply(lambda x: 1 if x == 1 else 0)
df['istwo'] = df['runs_off_bat'].apply(lambda x: 1 if x == 2 else 0)
df['isthree'] = df['runs_off_bat'].apply(lambda x: 1 if x == 3 else 0)
df['isfour'] = df['runs_off_bat'].apply(lambda x: 1 if x == 4 else 0)
df['issix'] = df['runs_off_bat'].apply(lambda x: 1 if x == 6 else 0)

df[df['runs_off_bat'].isin([4,6])]['runs_off_bat'].count() / df['runs_off_bat'].count()

df['phase'] = df['ball'].apply(lambda x:'powerplay' if x < 6 else ( 'middle' if x < 15 else 'death over'))

striker = list(df['striker'].unique())
non_striker = list(df['non_striker'].unique())
batting_team= list(df['batting_team'].unique())
bowling_team= list(df['bowling_team'].unique())
bowler= list(df['bowler'].unique())
venue= list(df['venue'].unique())
season= list(df['season'].unique())
phase = ['powerplay','middle','death over']
innings =[1,2]

def filter_batting_analysis(bdf,
                     batsman=striker,
                     batsman1 = non_striker,
                     bowler = bowler,
                     batting_team = batting_team,
                     bowling_team = bowling_team,
                     venue = venue,
                     phase = phase,
                     season = season,
                     innings = innings
                     ):
    bdf = bdf[bdf['striker'].isin(batsman)]
        
    bdf = bdf[bdf['non_striker'].isin(batsman1)]
    bdf = bdf[bdf['bowler'].isin(bowler)]
    bdf = bdf[bdf['batting_team'].isin(batting_team)]
    bdf = bdf[bdf['bowling_team'].isin(bowling_team)]
    bdf = bdf[bdf['venue'].isin(venue)]
    bdf = bdf[bdf['phase'].isin(phase)]
    bdf = bdf[bdf['season'].isin(season)]
    bdf = bdf[bdf['innings'].isin(innings)]

    def filter_batsman_overall_performance():

        bat_bdf = pd.DataFrame(bdf.groupby('striker').agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()
        bat_bdf = bat_bdf.rename(columns= {'match_id':'innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})


        bat_bdf['RPI'] = bat_bdf['runs'] / bat_bdf['innings']
        bat_bdf['Average'] = np.where(bat_bdf['outs'] == 0,bat_bdf['runs'],bat_bdf['runs'] / bat_bdf['outs'])
        bat_bdf['StrikeRate'] = 100*bat_bdf['runs'] / bat_bdf['ball']
        bat_bdf['boundary_%'] = 100*((bat_bdf['four']*4)+(bat_bdf['six']*6) )/ bat_bdf['runs']
        bat_bdf['dot_%'] = 100*bat_bdf['dots'] / bat_bdf['ball']

        print('Overall Batsman Stats')
        print(bat_bdf)
        print('\n-----------\n')

        if len(batsman) >= 2:
            #Comparing Runs Barplot
            plt.figure(figsize=(8,4))
            sns.barplot(data=bat_bdf, x='striker' ,y='runs', width=.25)
            plt.title('Comapring Batsman by Runs')
            plt.xlabel(None)
            plt.ylabel('Runs')
            plt.show()

            #Comparing Strikerate Barplot

            plt.figure(figsize=(8,4))
            sns.barplot(data=bat_bdf, x='striker' ,y='StrikeRate', width=.25)
            plt.title('Comapring Batsman by StrikeRate')
            plt.xlabel(None)
            plt.show()

            #Comparing RPI and Average Barplot

            plt.figure(figsize=(4,4))
            bat_bdf_melted = bat_bdf.melt(id_vars='striker',value_vars=['RPI','Average'],var_name='Metric',value_name='Value')
            sns.barplot(data=bat_bdf_melted, x='striker', y='Value',hue='Metric',width=.25)
            plt.title('Comparing Batsman by Average')
            plt.legend()
            plt.show()

            #Comparing Boundary and Dot Scatter

            sns.scatterplot(data=bat_bdf, x='boundary_%',y='dot_%')
            for i in range(len(bat_bdf)):
                plt.text(bat_bdf['boundary_%'][i] ,bat_bdf['dot_%'][i] , bat_bdf['striker'][i])
            plt.title('Boundary % and Dot % by Batsman')
            plt.axvline(17,ls='--',color='grey')
            plt.axhline(40,ls='--',color='grey')
            plt.ylabel('Dot %')
            plt.xlabel('Boundary %')
            plt.show()

            #compare Four and Six Bar plot

            plt.figure(figsize=(4,4))
            bat_bdf_melted = bat_bdf.melt(id_vars='striker',value_vars=['four','six'],var_name='Metric',value_name='Value')
            sns.barplot(data=bat_bdf_melted, x='striker', y='Value',hue='Metric',width=.25)
            plt.title('Comparing Batsman by Four and Six')
            plt.xlabel(None)
            plt.ylabel(None)
            plt.show()



    
        
    def filter_batsman_innings_1():


        ing_1 = pd.DataFrame(bdf[bdf['innings'] == 1].groupby('striker').agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()
  

        ing_1 = ing_1.rename(columns= {'match_id':'innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})

        ing_1['RPI'] = ing_1['runs'] / ing_1['innings']
        ing_1['Average'] = np.where(ing_1['outs'] == 0,ing_1['runs'],ing_1['runs'] / ing_1['outs'])
        ing_1['StrikeRate'] = 100*ing_1['runs'] / ing_1['ball']
        ing_1['boundary_%'] = 100*((ing_1['four']*4)+(ing_1['six']*6) )/ ing_1['runs']
        ing_1['dot_%'] = 100*ing_1['dots'] / ing_1['ball']

        print('Innings 1\n',ing_1)
        print('\n-----------\n')  

        if len(batsman) >= 2:
            #Comparing Runs Barplot
            
            sns.barplot(data=ing_1, x='striker' ,y='runs', width=.25)
            plt.title('Comapring Batsman by Runs Innings 1')
            plt.xlabel(None)
            plt.ylabel('Runs')
            plt.show()

            #Comparing Strikerate Barplot

            
            sns.barplot(data=ing_1, x='striker' ,y='StrikeRate', width=.25)
            plt.title('Comapring Batsman by StrikeRate Innings 1')
            plt.xlabel(None)
            plt.show()

            #Comparing RPI and Average Barplot

            
            ing_1_melted = ing_1.melt(id_vars='striker',value_vars=['RPI','Average'],var_name='Metric',value_name='Value')
            sns.barplot(data=ing_1_melted, x='striker', y='Value',hue='Metric',width=.25)
            plt.title('Comparing Batsman by Average Innings 1')
            plt.show()

            #Comparing Boundary and Dot Scatter

            sns.scatterplot(data=ing_1, x='boundary_%',y='dot_%')
            for i in range(len(ing_1)):
                plt.text(ing_1['boundary_%'][i] ,ing_1['dot_%'][i] , ing_1['striker'][i])
            plt.title('Boundary % and Dot % by Batsman Innings 1')
            plt.ylabel('Dot %')
            plt.xlabel('Boundary %')
            plt.axvline(17,ls='--',color='grey')
            plt.axhline(40,ls='--',color='grey')
            plt.show()

            #compare Four and Six Bar plot

            
            ing_1_melted = ing_1.melt(id_vars='striker',value_vars=['four','six'],var_name='Metric',value_name='Value')
            sns.barplot(data=ing_1_melted, x='striker', y='Value',hue='Metric',width=.25)
            plt.title('Comparing Batsman by Four and Six Innings 1')
            plt.xlabel(None)
            plt.ylabel(None)
            plt.show()


    def filter_batsman_innings_2():

        ing_2 = pd.DataFrame(bdf[bdf['innings'] == 2].groupby('striker').agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()
        
      
        
        ing_2 = ing_2.rename(columns= {'match_id':'innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})

        ing_2['RPI'] = ing_2['runs'] / ing_2['innings']
        ing_2['Average'] = np.where(ing_2['outs'] == 0,ing_2['runs'],ing_2['runs'] / ing_2['outs'])
        ing_2['StrikeRate'] = 100*ing_2['runs'] / ing_2['ball']
        ing_2['boundary_%'] = 100*((ing_2['four']*4)+(ing_2['six']*6) )/ ing_2['runs']
        ing_2['dot_%'] = 100*ing_2['dots'] / ing_2['ball']

        print('Innings 2\n',ing_2)
        print('\n-----------\n')

        if len(batsman) >= 2:
            #Comparing Runs Barplot
            
            sns.barplot(data=ing_2, x='striker' ,y='runs', width=.25)
            plt.title('Comapring Batsman by Runs Innings 2')
            plt.xlabel(None)
            plt.ylabel('Runs')
            plt.show()

            #Comparing Strikerate Barplot

            
            sns.barplot(data=ing_2, x='striker' ,y='StrikeRate', width=.25)
            plt.title('Comapring Batsman by StrikeRate Innings 2')
            plt.xlabel(None)
            plt.show()

            #Comparing RPI and Average Barplot

            
            ing_2_melted = ing_2.melt(id_vars='striker',value_vars=['RPI','Average'],var_name='Metric',value_name='Value')
            sns.barplot(data=ing_2_melted, x='striker', y='Value',hue='Metric',width=.25)
            plt.title('Comparing Batsman by Average Innings 2')
            plt.show()

            #Comparing Boundary and Dot Scatter

            sns.scatterplot(data=ing_2, x='boundary_%',y='dot_%')
            for i in range(len(ing_2)):
                plt.text(ing_2['boundary_%'][i] ,ing_2['dot_%'][i] , ing_2['striker'][i])
            plt.title('Boundary % and Dot % by Batsman Innings 2')
            plt.ylabel('Dot %')
            plt.xlabel('Boundary %')
            plt.axvline(17,ls='--',color='grey')
            plt.axhline(40,ls='--',color='grey')
            plt.show()

            #compare Four and Six Bar plot

            
            ing_2_melted = ing_2.melt(id_vars='striker',value_vars=['four','six'],var_name='Metric',value_name='Value')
            sns.barplot(data=ing_2_melted, x='striker', y='Value',hue='Metric',width=.25)
            plt.title('Comparing Batsman by Four and Six Innings 2')
            plt.xlabel(None)
            plt.ylabel(None)
            plt.show()

    def filter_batsman_phases():
        
            phase_bdf = pd.DataFrame(bdf.groupby('phase').agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()
            
        

            phase_bdf = phase_bdf.rename(columns= {'match_id':'innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})
            phase_bdf = phase_bdf.sort_values(by='phase',ascending=False)

            phase_bdf['RPI'] = phase_bdf['runs'] / phase_bdf['innings']
            phase_bdf['Average'] = np.where(phase_bdf['outs'] == 0,phase_bdf['runs'],phase_bdf['runs'] / phase_bdf['outs'])
            phase_bdf['StrikeRate'] = 100*phase_bdf['runs'] / phase_bdf['ball']
            phase_bdf['boundary_%'] = 100*((phase_bdf['four']*4)+(phase_bdf['six']*6) )/ phase_bdf['runs']
            phase_bdf['dot_%'] = 100*phase_bdf['dots'] / phase_bdf['ball']

            phase_bdf = phase_bdf.sort_values(by='phase',ascending=False)
            print('phases\n',phase_bdf)
            print('\n-----------\n')

            if len(batsman) == 1:

                #Comparing Runs Barplot

                
                sns.barplot(data=phase_bdf, x='phase' ,y='runs', width=.25)
                plt.title('Runs by Phases ')
                plt.xlabel(None)
                plt.ylabel('Runs')
                plt.show()

                  #Comparing Strikerate Barplot

                
                sns.barplot(data=phase_bdf, x='phase' ,y='StrikeRate', width=.25)
                plt.title('Comapring Batsman by Phases')
                plt.xlabel(None)
                plt.show()

                #Comparing RPI and Average Barplot
                    
                
                phase_bdf_melted = phase_bdf.melt(id_vars='phase',value_vars=['RPI','Average'],var_name='Metric',value_name='Value')
                sns.barplot(data=phase_bdf_melted, x='phase', y='Value',hue='Metric')
                plt.title('RPI and Average by Phases')
                plt.show()

                #Comparing Boundary and Dot Scatter


                sns.scatterplot(data=phase_bdf, x='StrikeRate',y='dot_%')
                for i in range(len(phase_bdf)):
                    plt.text(phase_bdf['StrikeRate'][i] +1,phase_bdf['dot_%'][i] -1, phase_bdf['phase'][i])
                plt.title('Strike Rate and Dot\%\ by Phases')
                plt.show()

                #compare Four and Six Bar plot

                
                phases_bdf_melted = phase_bdf.melt(id_vars='phase',value_vars=['four','six'],var_name='Metric',value_name='Value')
                sns.barplot(data=phase_bdf_melted, x='phase', y='Value',hue='Metric',width=.25)
                plt.title('Comparing Batsman by Four and Six Phases')
                plt.xlabel(None)
                plt.ylabel(None)
                plt.show()
            
    def filter_batsman_innings_phases():
        
            ing_phase_bdf = pd.DataFrame(bdf.groupby(['innings','phase']).agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()

            
            ing_phase_bdf = ing_phase_bdf.rename(columns= {'match_id':'no_of_innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})


            ing_phase_bdf['RPI'] = ing_phase_bdf['runs'] / ing_phase_bdf['no_of_innings']
            ing_phase_bdf['Average'] = np.where(ing_phase_bdf['outs'] == 0,ing_phase_bdf['runs'],ing_phase_bdf['runs'] / ing_phase_bdf['outs'])
            ing_phase_bdf['StrikeRate'] = 100*ing_phase_bdf['runs'] / ing_phase_bdf['ball']
            ing_phase_bdf['boundary_%'] = 100*((ing_phase_bdf['four']*4)+(ing_phase_bdf['six']*6) )/ ing_phase_bdf['runs']
            ing_phase_bdf['dot_%'] = 100*ing_phase_bdf['dots'] / ing_phase_bdf['ball']

            

            ing_phase_bdf_1 = ing_phase_bdf[ing_phase_bdf['innings'] == 1]
            ing_phase_bdf_2 = ing_phase_bdf[ing_phase_bdf['innings'] == 2]
            ing_phase_bdf_1 = ing_phase_bdf_1.sort_values(by='phase',ascending=False)
            ing_phase_bdf_2 = ing_phase_bdf_2.sort_values(by='phase',ascending=False)

            
            print('\n-----------\n')
            print('InningsPhases First Innings\n',ing_phase_bdf_1.sort_values(by='phase',ascending=False))
            print('\n-----------\n')


            if len(batsman) == 1:

                #Comparing Runs Barplot

                
                sns.barplot(data=ing_phase_bdf_1, x='phase' ,y='runs', width=.25)
                plt.title('Runs by Phases (Innings 1) ')
                plt.xlabel(None)
                plt.ylabel('Runs')
                plt.show()

                  #Comparing Strikerate Barplot

                
                sns.barplot(data=ing_phase_bdf_1, x='phase' ,y='StrikeRate', width=.25)
                plt.title('Comapring Batsman by Phases (Innings 1)')
                plt.xlabel(None)
                plt.show()

                #Comparing RPI and Average Barplot
                    
                
                ing_phase_bdf_1_melted = ing_phase_bdf_1.melt(id_vars='phase',value_vars=['RPI','Average'],var_name='Metric',value_name='Value')
                sns.barplot(data=ing_phase_bdf_1_melted, x='phase', y='Value',hue='Metric')
                plt.title('RPI and Average by Phases (Innings 1)')
                plt.show()

                #Comparing Boundary and Dot Scatter


                sns.scatterplot(data=ing_phase_bdf_1, x='StrikeRate',y='dot_%')
                for i in range(len(ing_phase_bdf_1)):
                    plt.text(ing_phase_bdf_1['StrikeRate'][i] +1,ing_phase_bdf_1['dot_%'][i] -1, ing_phase_bdf_1['phase'][i])
                plt.title('Strike Rate and Dot\%\ by Phases (Innings 1)')
                plt.show()

                ''' sns.scatterplot(data=ing_phase_bdf_2, x='StrikeRate',y='dot_%')
                for i in range(len(ing_phase_bdf_2)):
                    plt.text(ing_phase_bdf_2['StrikeRate'][i] ,ing_phase_bdf_2['dot_%'][i] , ing_phase_bdf_2['phase'][i])
                plt.title('Strike Rate and Dot\%\ by Phases (Innings 2)')
                plt.show() '''


                #compare Four and Six Bar plot

                ing_phase_bdf_melted = ing_phase_bdf_1.melt(id_vars='phase',value_vars=['four','six'],var_name='Metric',value_name='Value')
                sns.barplot(data=ing_phase_bdf_1_melted, x='phase', y='Value',hue='Metric',width=.25)
                plt.title('Comparing Batsman by Four and Six Phases (Innings 1)')
                plt.xlabel(None)
                plt.ylabel(None)
                plt.show()

            
            print('InningsPhases Second Innings\n',ing_phase_bdf_2.sort_values(by='phase',ascending=False))
            print('\n-----------\n')

            if len(batsman) == 1:

                #Comparing Runs Barplot

                
                sns.barplot(data=ing_phase_bdf_2, x='phase' ,y='runs', width=.25)
                plt.title('Runs by Phases (Innings 2) ')
                plt.xlabel(None)
                plt.ylabel('Runs')
                plt.show()

                  #Comparing Strikerate Barplot

                
                sns.barplot(data=ing_phase_bdf_2, x='phase' ,y='StrikeRate', width=.25)
                plt.title('Comapring Batsman by Phases (Innings 2)')
                plt.xlabel(None)
                plt.show()

                #Comparing RPI and Average Barplot
                    
                
                ing_phase_bdf_2_melted = ing_phase_bdf_2.melt(id_vars='phase',value_vars=['RPI','Average'],var_name='Metric',value_name='Value')
                sns.barplot(data=ing_phase_bdf_2_melted, x='phase', y='Value',hue='Metric')
                plt.title('RPI and Average by Phases (Innings 2)')
                plt.show()

                #Comparing Boundary and Dot Scatter


                sns.scatterplot(data=ing_phase_bdf_2, x='StrikeRate',y='dot_%')
                plt.title('Strike Rate and Dot\%\ by Phases (Innings 2)')
                for i in range(len(ing_phase_bdf_2)):
                    plt.text(ing_phase_bdf_2['StrikeRate'].iloc[i] ,ing_phase_bdf_2['dot_%'].iloc[i] , ing_phase_bdf_2['phase'].iloc[i])
                
                plt.show()

                #compare Four and Six Bar plot

                
                ing_phase_bdf_melted = ing_phase_bdf_2.melt(id_vars='phase',value_vars=['four','six'],var_name='Metric',value_name='Value')
                sns.barplot(data=ing_phase_bdf_2_melted, x='phase', y='Value',hue='Metric',width=.25)
                plt.title('Comparing Batsman by Four and Six Phases (Innings 2)')
                plt.xlabel(None)
                plt.ylabel(None)
                plt.show()



    def filter_batsman_bowler():

        bowler_bdf = pd.DataFrame(bdf.groupby('bowler').agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()
        
    
        
        bowler_bdf = bowler_bdf.rename(columns= {'match_id':'innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})
      
        bowler_bdf['RPI'] = bowler_bdf['runs'] / bowler_bdf['innings']
        bowler_bdf['Average'] = np.where(bowler_bdf['outs'] == 0,bowler_bdf['runs'],bowler_bdf['runs'] / bowler_bdf['outs'])
        bowler_bdf['StrikeRate'] = 100*bowler_bdf['runs'] / bowler_bdf['ball']
        bowler_bdf['boundary_%'] = 100*((bowler_bdf['four']*4)+(bowler_bdf['six']*6) )/ bowler_bdf['runs']
        bowler_bdf['dot_%'] = 100*bowler_bdf['dots'] / bowler_bdf['ball']

        bowler_bdf['bowl_average'] = np.where(bowler_bdf['outs']==0,bowler_bdf['runs'],bowler_bdf['runs'] / bowler_bdf['outs'])
        bowler_bdf['bowl_strikerate'] = np.where(bowler_bdf['outs']==0,bowler_bdf['ball'],bowler_bdf['runs'] / bowler_bdf['outs'])
        bowler_bdf['economy'] = 6*bowler_bdf['runs'] / bowler_bdf['ball']


        
        
        print('Bowlers\n',bowler_bdf)
        print('\n-----------\n')

    def filter_batsman_innings_bowler():


        

        ing_bowler_bdf = pd.DataFrame(bdf.groupby(['innings','bowler']).agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()
        ing_bowler_bdf = ing_bowler_bdf.rename(columns= {'match_id':'no_of_innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})
        ing_bowler_bdf = ing_bowler_bdf.sort_values(by=['innings','outs'],ascending=[1,0])

        ing_bowler_bdf['RPI'] = ing_bowler_bdf['runs'] / ing_bowler_bdf['no_of_innings']
        ing_bowler_bdf['Average'] = np.where(ing_bowler_bdf['outs'] == 0,ing_bowler_bdf['runs'],ing_bowler_bdf['runs'] / ing_bowler_bdf['outs'])
        ing_bowler_bdf['StrikeRate'] = 100*ing_bowler_bdf['runs'] / ing_bowler_bdf['ball']
        ing_bowler_bdf['boundary_%'] = 100*((ing_bowler_bdf['four']*4)+(ing_bowler_bdf['six']*6) )/ ing_bowler_bdf['runs']
        ing_bowler_bdf['dot_%'] = 100*ing_bowler_bdf['dots'] / ing_bowler_bdf['ball']

        ing_bowler_bdf['bowl_average'] = np.where(ing_bowler_bdf['outs']==0,ing_bowler_bdf['runs'],ing_bowler_bdf['runs'] / ing_bowler_bdf['outs'])
        ing_bowler_bdf['bowl_strikerate'] = np.where(ing_bowler_bdf['outs']==0,ing_bowler_bdf['ball'],ing_bowler_bdf['runs'] / ing_bowler_bdf['outs'])
        ing_bowler_bdf['economy'] = 6*ing_bowler_bdf['runs'] / ing_bowler_bdf['ball']

        ing_bowler_bdf_1 = ing_bowler_bdf[ing_bowler_bdf['innings'] == 1]
        ing_bowler_bdf_2 = ing_bowler_bdf[ing_bowler_bdf['innings'] == 2]

        print('\n-----------\n')
        print('Innings Wise Bowlers First Innings\n',ing_bowler_bdf_1)
        print('\n-----------\n')
        print('Innings Wise Bowlers Second Innings\n',ing_bowler_bdf_2)
        print('\n-----------\n')

    def filter_batsman_phase_bowler():


    

        bowler_phase_bdf = pd.DataFrame(bdf.groupby(['bowler','phase']).agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()
        bowler_phase_bdf = bowler_phase_bdf.rename(columns= {'match_id':'no_of_innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})
        

        bowler_phase_bdf['RPI'] = bowler_phase_bdf['runs'] / bowler_phase_bdf['no_of_innings']
        bowler_phase_bdf['Average'] = np.where(bowler_phase_bdf['outs'] == 0,bowler_phase_bdf['runs'],bowler_phase_bdf['runs'] / bowler_phase_bdf['outs'])
        bowler_phase_bdf['StrikeRate'] = 100*bowler_phase_bdf['runs'] / bowler_phase_bdf['ball']
        bowler_phase_bdf['boundary_%'] = 100*((bowler_phase_bdf['four']*4)+(bowler_phase_bdf['six']*6) )/ bowler_phase_bdf['runs']
        bowler_phase_bdf['dot_%'] = 100*bowler_phase_bdf['dots'] / bowler_phase_bdf['ball']

        bowler_phase_bdf['bowl_average'] = np.where(bowler_phase_bdf['outs']==0,bowler_phase_bdf['runs'],bowler_phase_bdf['runs'] / bowler_phase_bdf['outs'])
        bowler_phase_bdf['bowl_strikerate'] = np.where(bowler_phase_bdf['outs']==0,bowler_phase_bdf['ball'],bowler_phase_bdf['runs'] / bowler_phase_bdf['outs'])
        bowler_phase_bdf['economy'] = 6*bowler_phase_bdf['runs'] / bowler_phase_bdf['ball']

        print('Bowler Phase Wise\n',bowler_phase_bdf.sort_values(by=['bowler','phase'],ascending=False))
        print('\n-----------\n')



            
    def filter_batsman_opposition():



        opposition_bdf = pd.DataFrame(bdf.groupby('bowling_team').agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()
        opposition_bdf = opposition_bdf.rename(columns= {'match_id':'innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})

        opposition_bdf['RPI'] = opposition_bdf['runs'] / opposition_bdf['innings']
        opposition_bdf['Average'] = np.where(opposition_bdf['outs'] == 0,opposition_bdf['runs'],opposition_bdf['runs'] / opposition_bdf['outs'])
        opposition_bdf['StrikeRate'] = 100*opposition_bdf['runs'] / opposition_bdf['ball']
        opposition_bdf['boundary_%'] = 100*((opposition_bdf['four']*4)+(opposition_bdf['six']*6) )/ opposition_bdf['runs']
        opposition_bdf['dot_%'] = 100*opposition_bdf['dots'] / opposition_bdf['ball']
        print('Opposition\n',opposition_bdf)
        print('\n-----------\n')

    def filter_batsman_venue():

        venue_bdf = pd.DataFrame(bdf.groupby('venue').agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()
        venue_bdf = venue_bdf.rename(columns= {'match_id':'innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})

        venue_bdf['RPI'] = venue_bdf['runs'] / venue_bdf['innings']
        venue_bdf['Average'] = np.where(venue_bdf['outs'] == 0,venue_bdf['runs'],venue_bdf['runs'] / venue_bdf['outs'])
        venue_bdf['StrikeRate'] = 100*venue_bdf['runs'] / venue_bdf['ball']
        venue_bdf['boundary_%'] = 100*((venue_bdf['four']*4)+(venue_bdf['six']*6) )/ venue_bdf['runs']
        venue_bdf['dot_%'] = 100*venue_bdf['dots'] / venue_bdf['ball']
        print('Venue\n',venue_bdf.sort_values(by='runs',ascending=False))
        print('\n-----------\n')

    def filter_batsman_innings_venue():

        ing_venue_bdf = pd.DataFrame(bdf.groupby(['innings','venue']).agg({'match_id':'nunique','runs_off_bat':'sum','ball':'count','player_dismissed':'count','isfour':'sum','issix':'sum','isdot':'sum'})).reset_index()
        ing_venue_bdf = ing_venue_bdf.rename(columns= {'match_id':'no_of_innings','runs_off_bat':'runs','player_dismissed':'outs','isfour':'four','issix':'six','isdot':'dots'})


        ing_venue_bdf['RPI'] = ing_venue_bdf['runs'] / ing_venue_bdf['no_of_innings']
        ing_venue_bdf['Average'] = np.where(ing_venue_bdf['outs'] == 0,ing_venue_bdf['runs'],ing_venue_bdf['runs'] / ing_venue_bdf['outs'])
        ing_venue_bdf['StrikeRate'] = 100*ing_venue_bdf['runs'] / ing_venue_bdf['ball']
        ing_venue_bdf['boundary_%'] = 100*((ing_venue_bdf['four']*4)+(ing_venue_bdf['six']*6) )/ ing_venue_bdf['runs']
        ing_venue_bdf['dot_%'] = 100*ing_venue_bdf['dots'] / ing_venue_bdf['ball']


        ing_venue_bdf_1= ing_venue_bdf[ing_venue_bdf['innings'] == 1]
        ing_venue_bdf_2 = ing_venue_bdf[ing_venue_bdf['innings'] == 2]

        print('\n-----------\n')
        print('Innings Wise Venue First Innings\n',ing_venue_bdf_1)
        print('\n-----------\n')
        print('Innings Wise Venue Second Innings\n',ing_venue_bdf_2)
        print('\n-----------\n')
    
    filter_batsman_overall_performance()
    filter_batsman_innings_1()
    filter_batsman_innings_2()
    filter_batsman_phases()
    filter_batsman_innings_phases()
    filter_batsman_bowler()
    filter_batsman_innings_bowler()
    filter_batsman_phase_bowler()
    filter_batsman_opposition()
    filter_batsman_venue()
    filter_batsman_innings_venue()

print('MS Dhoni Performance against Five Bowlers')
filter_batting_analysis(df,batsman=['MS Dhoni'],bowler=['JJ Bumrah','SL Malinga','DW Steyn','B Kumar','TA Boult'])

print('Batting Performance Analysis')
filter_batting_analysis(df,batsman=['MS Dhoni','V Kohli','KL Rahul','AB de Villiers','S Dhawan'])

print('Five batsman Performance Against R Khan)
filter_batting_analysis(df,batsman=['MS Dhoni','V Kohli','KL Rahul','AB de Villiers','S Dhawan'],bowler=['Rashid Khan'])
