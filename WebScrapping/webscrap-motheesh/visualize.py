import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
class visualize:
    def create_plot_graph(self,plot):
        data = plot
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON

    def prepareData(self,dataPrep):
        dataPrep.replace('',np.nan,inplace=True)
        dataPrep=dataPrep.dropna(how='any',axis=0)
        dataPrep["rating"]=dataPrep["rating"].astype(str).astype('int')
        dataPrep["price"]=dataPrep["price"].str.replace(r'\D+', '',regex=True).astype('int')
        dataPrep=dataPrep.sort_values(by="rating",ascending=False)
        dataPrep["review_length"]= dataPrep["ShortComments"].apply(lambda x:len(x))
        return dataPrep
    def getGraphData(self,gData):
        tf=gData.groupby("ProductName").mean().sort_values(by="price",ascending=False)
        ttf=pd.DataFrame([tf.index,tf.price,tf.rating],index=["product","price","rating"]).T
        return ttf

    def getProductWiseRatingsAndItsPrice(self,ttf):
        prepData=self.prepareData(ttf)
        self.prepData=prepData
        get_xy=self.getGraphData(prepData)
        #fig = go.Bar( x=get_xy["product"], y=get_xy["price"],showlegend=True)
        fig = px.bar(get_xy, x="product", y="price",height=600,labels={"product":"Products","price":"price"}, color="rating",hover_data=["product","price"], title="Product wise Price and its overall ratings")
        plot=self.create_plot_graph(fig)
        #plot = fig.to_html(full_html=False)
        #plot=fig.to_plotly_json()
        #print(plot)
        return plot
    def RatingDistributionForAllProducts(self,df):
        ratings=df['rating'].value_counts()
        fig = px.funnel_area(names=ratings.index,
                            values=ratings.values,height=600,
                            title='Distribution of user Ratings for all products')
        plot=self.create_plot_graph(fig)
        return plot
    def getReviewLengthDistribution(self):
        fig = px.bar(self.prepData, x="rating", y="review_length",color="rating",title="Distribution of Length of Reviews by rating") 
        plot=self.create_plot_graph(fig)
        return plot        