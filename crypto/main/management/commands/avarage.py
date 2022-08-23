from django.core.management.base import BaseCommand
from ...strategy import get_moving_average, get_date_range
import subprocess
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
import seaborn as sns
from io import BytesIO
import base64
import matplotlib as plt
from django.shortcuts import render
import pandas as pd
import openpyxl

class Command(BaseCommand):

	def handle(self, **options):
		""" A curve is drawn based on the cryptocurrency moving average and the selected date """
		date_range = get_date_range(numdays=10)
		ma50_list = []
		ma200_list = []
		for day in date_range:
			ma = get_moving_average(date=day, numdays=50, crypto="BTC", currency="EUR")
			ma200 = get_moving_average(date=day, numdays=200, crypto="BTC", currency="EUR")
			ma50_list.append(ma)
			ma200_list.append(ma200)

		data_1 = {"day": date_range, "ma50": ma50_list}
		data_2 = {"day": date_range, "ma200": ma200_list}

		plot_1 = pd.DataFrame(data_1)
		plot_2 = pd.DataFrame(data_2)

		df = pd.DataFrame({'ma50': ma50_list,
						   'ma200': ma200_list, 
						   "day": date_range})
		print(df)

		plt.use('Agg')
		df = df
		# recoil = sns.scatterplot(data = df, x=plot_1["day"], y=df["ma50"], legend='full')
		# fig = recoil.figure
		# recoil_file = BytesIO() 
		# fig.savefig(recoil_file, format='png')
		# encoded_file = base64.b64encode(recoil_file.getvalue())

		fig, ax = plt.pyplot.subplots()
		sns.scatterplot(data = df, x=plot_1["day"], y=df["ma50"], legend='full')
		ax2 = ax.twinx()
		sns.scatterplot(data = df, x=plot_1["day"], y=df["ma50"], ax=ax2, color='r')
		fig.savefig(format='png')
			

