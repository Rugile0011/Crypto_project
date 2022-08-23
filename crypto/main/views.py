import io

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm
from .strategy import get_moving_average, get_date_range
import seaborn as sns
from io import BytesIO
import base64
import matplotlib as plt
from django.shortcuts import render
import pandas as pd
from matplotlib.pyplot import figure



def home(request):
	return render(request, 'home.html')


def about(request):
	return render(request, 'about.html')


def register(request):
	""" Function allows to register a new user """
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()

			messages.success(request, f'Your account has been created. You can log in now!')
			return redirect('login')
	else:
		form = UserRegistrationForm()

	context = {'form': form}
	return render(request, 'register.html', context)


def graph_view(request):
	""" A curve is drawn based on the cryptocurrency moving average and the selected date """

	date_range = get_date_range(numdays=20)
	ma50_list = []
	ma100_list = []
	ma200_list = []
	for day in date_range:
		ma = get_moving_average(date=day, numdays=50, crypto="BTC", currency="EUR")
		ma100 = get_moving_average(date=day, numdays=100, crypto="BTC", currency="EUR")
		ma200 = get_moving_average(date=day, numdays=200, crypto="BTC", currency="EUR")
		ma50_list.append(ma)
		ma100_list.append(ma100)
		ma200_list.append(ma200)

	df = pd.DataFrame({'ma50': ma50_list,
					   'ma100': ma100_list,
					   'ma200': ma200_list,
					   "day": date_range})
	
	df.set_index('day', inplace=True)
	figure(dpi=50)
	df = df
	fig, ax = plt.pyplot.subplots()
	fig.set_size_inches(15, 12)
	ax.tick_params(axis='both', labelrotation=35, labelsize=10)
	ax.set_xlabel('day', fontsize=13)
	ax.set_ylabel('ma', fontsize=13)
	sns.lineplot(data=df)
	recoil_file = BytesIO() 
	fig.savefig(recoil_file, format='png')
	encoded_file = base64.b64encode(recoil_file.getvalue())

	context = {'url': encoded_file.decode('utf-8')}
	return render(request, 'graph.html', context)
